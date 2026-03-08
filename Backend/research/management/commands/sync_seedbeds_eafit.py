import re
import time
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand

from research.models import Seedbed

CATALOG_URL = "https://www.eafit.edu.co/sistema-ciencia-tecnologia-innovacion/investigacion/nuestros-semilleros"

BAD_SNIPPETS = [
    "Habilitar el audio para usuarios con discapacidad visual",
    "cookies",
    "Política de tratamiento de datos",
    "Aviso de privacidad",
    "Accesibilidad",
]

FACULTY_LABELS = [
    "Escuela de Administración",
    "Escuela de Derecho",
    "Escuela de Finanzas, Economía y Gobierno",
    "Escuela de Ciencias Aplicadas e Ingeniería",
    "Escuela de Artes y Humanidades",
    "Escuelas de Artes y Humanidades",
]


def clean_text(value: str) -> str:
    return re.sub(r"\s+", " ", (value or "")).strip()


def extract_catalog_entries(html: str):
    soup = BeautifulSoup(html, "lxml")
    entries = []

    # busca headings + link "Conoce más aquí"
    for link in soup.find_all("a"):
        text = clean_text(link.get_text())
        href = link.get("href") or ""

        if text.lower() != "conoce más aquí":
            continue

        if "/nuestros-semilleros/" not in href:
            continue

        full_url = urljoin("https://www.eafit.edu.co", href)

        # intenta encontrar el título del semillero hacia atrás
        title_tag = link.find_previous(["h2", "h3", "h4"])
        title = clean_text(title_tag.get_text()) if title_tag else "Unnamed Seedbed"

        # intenta encontrar la facultad/escuela hacia atrás
        faculty = "Unknown"
        previous_text = []
        for prev in link.find_all_previous(limit=10):
            t = clean_text(prev.get_text())
            if t:
                previous_text.append(t)
        joined = " | ".join(previous_text)

        for label in FACULTY_LABELS:
            if label in joined:
                faculty = label
                break

        entries.append({
            "name": title[:200],
            "faculty": faculty[:200],
            "url": full_url
        })

    # quitar duplicados por URL
    seen = set()
    unique_entries = []
    for item in entries:
        if item["url"] not in seen:
            unique_entries.append(item)
            seen.add(item["url"])

    return unique_entries


def extract_label_value(page_text: str, label: str):
    lines = [clean_text(x) for x in page_text.split("\n")]
    normalized_label = clean_text(label).lower().rstrip(":")

    for i, line in enumerate(lines):
        if clean_text(line).lower().rstrip(":") == normalized_label:
            for j in range(i + 1, min(i + 10, len(lines))):
                if lines[j] and all(b.lower() not in lines[j].lower() for b in BAD_SNIPPETS):
                    return lines[j]
    return None


def extract_description(soup: BeautifulSoup):
    main = soup.find("main") or soup.find("article") or soup

    heading_keywords = [
        "descripción",
        "descripcion",
        "qué hacemos",
        "que hacemos",
        "el semillero",
        "presentación",
        "presentacion",
        "objetivo general",
    ]

    for h in main.find_all(["h2", "h3", "h4", "h5", "strong"]):
        ht = clean_text(h.get_text()).lower()
        if any(keyword in ht for keyword in heading_keywords):
            parts = []
            for sib in h.find_all_next():
                if sib.name in ["h2", "h3", "h4", "h5"]:
                    break
                if sib.name == "p":
                    t = clean_text(sib.get_text())
                    if len(t) >= 60 and not any(b.lower() in t.lower() for b in BAD_SNIPPETS):
                        parts.append(t)
                if len(" ".join(parts)) >= 250:
                    break

            if parts:
                return " ".join(parts)[:1000]

    # fallback: meta description
    meta_desc = soup.find("meta", attrs={"name": "description"})
    if meta_desc and meta_desc.get("content"):
        text = clean_text(meta_desc["content"])
        if text and not any(b.lower() in text.lower() for b in BAD_SNIPPETS):
            return text[:1000]

    og_desc = soup.find("meta", attrs={"property": "og:description"})
    if og_desc and og_desc.get("content"):
        text = clean_text(og_desc["content"])
        if text and not any(b.lower() in text.lower() for b in BAD_SNIPPETS):
            return text[:1000]

    return "Description not available yet."


def extract_tutor(page_text: str):
    for label in ["Docente Coordinador", "Coordinador", "Profesor", "Docente"]:
        value = extract_label_value(page_text, label)
        if value:
            return value[:200]
    return "TBD"


def extract_faculty(page_text: str, fallback_faculty: str):
    for label in ["Escuela", "Programa"]:
        value = extract_label_value(page_text, label)
        if value:
            return value[:200]
    return fallback_faculty


class Command(BaseCommand):
    help = "Loads EAFIT research seedbeds from the official website."

    def add_arguments(self, parser):
        parser.add_argument("--limit", type=int, default=0)
        parser.add_argument("--sleep", type=float, default=0.4)

    def handle(self, *args, **options):
        limit = options["limit"]
        sleep_seconds = options["sleep"]

        self.stdout.write("Fetching EAFIT catalog...")
        response = requests.get(CATALOG_URL, timeout=30)
        response.raise_for_status()

        entries = extract_catalog_entries(response.text)

        if limit and limit > 0:
            entries = entries[:limit]

        self.stdout.write(f"Found {len(entries)} seedbeds in catalog.")

        created_count = 0
        updated_count = 0

        for index, entry in enumerate(entries, start=1):
            self.stdout.write(f"[{index}/{len(entries)}] {entry['name']}")

            try:
                seedbed_response = requests.get(entry["url"], timeout=30)
                seedbed_response.raise_for_status()
                soup = BeautifulSoup(seedbed_response.text, "lxml")
                page_text = soup.get_text("\n")

                description = extract_description(soup)
                tutor = extract_tutor(page_text)
                faculty = extract_faculty(page_text, entry["faculty"])

                _, created = Seedbed.objects.update_or_create(
                    source_url=entry["url"],
                    defaults={
                        "name": entry["name"],
                        "faculty": faculty,
                        "tutor": tutor,
                        "description": description,
                        "status": "ACTIVE",
                    }
                )

                if created:
                    created_count += 1
                else:
                    updated_count += 1

            except Exception as exc:
                self.stdout.write(self.style.WARNING(f"Skipped {entry['name']}: {exc}"))

            time.sleep(sleep_seconds)

        self.stdout.write(self.style.SUCCESS(
            f"Done. Created: {created_count}, Updated: {updated_count}"
        ))