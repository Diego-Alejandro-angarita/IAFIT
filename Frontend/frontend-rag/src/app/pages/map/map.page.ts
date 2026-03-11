import {
  Component,
  AfterViewInit,
  OnDestroy,
  signal,
  inject,
  PLATFORM_ID
} from '@angular/core';
import { isPlatformBrowser } from '@angular/common';
import { RouterLink } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { FormsModule } from '@angular/forms';

/* ------------------------------------------------------------------ */
/*  Types                                                              */
/* ------------------------------------------------------------------ */

interface Ubicacion {
  codigo_bloque: string;
  piso: number;
  descripcion_semantica: string;
  metadatos: Record<string, unknown>;
  similarity: number;
}

interface BusquedaResponse {
  resultados: Ubicacion[];
}

interface BlockInfo {
  code: string;
  name: string;
  lat: number;
  lng: number;
  services: string[];
  floors: number;
  accessible: boolean;
}

/* ------------------------------------------------------------------ */
/*  Georeferenced EAFIT blocks — coordinates from OSM tile text labels */
/*  Use the map click handler (console.log) to fine-tune positions.    */
/* ------------------------------------------------------------------ */

const CAMPUS_BLOCKS: BlockInfo[] = [
  {
    code: '20',
    name: 'Bloque 20 — Edificio de Ciencias',
    lat: 6.19846,
    lng: -75.57925,
    services: [
      'Baños en todos los pisos',
      'Centro de Laboratorios (pisos superiores)',
      'Laboratorio de Química',
      'Salas de cómputo (piso 3)',
      'Aulas de clase (piso 3)',
      'Laboratorio de Física (piso 2)',
      'Ascensor (dos en cada extremo del piso 1)',
      'Escaleras (dos en cada extremo del piso 1)',
      'Laboratorio del Café (piso 1)'
    ],
    floors: 8,
    accessible: true
  }
];

/* ------------------------------------------------------------------ */
/*  Component                                                          */
/* ------------------------------------------------------------------ */

@Component({
  selector: 'app-map-page',
  standalone: true,
  imports: [RouterLink, FormsModule],
  templateUrl: './map.page.html',
  styleUrl: './map.page.scss'
})
export class MapPage implements AfterViewInit, OnDestroy {
  private readonly platformId = inject(PLATFORM_ID);
  private readonly http = inject(HttpClient);
  private readonly apiUrl = 'http://127.0.0.1:8001/api/llamaindex/buscar/';

  private map: any;
  private markers: Map<string, any> = new Map();
  private L: any;

  protected searchQuery = '';
  protected readonly loading = signal(false);
  protected readonly selectedBlock = signal<BlockInfo | null>(null);
  protected readonly semanticResults = signal<Ubicacion[]>([]);
  protected readonly notFound = signal(false);
  protected readonly panelOpen = signal(false);

  readonly blocks = CAMPUS_BLOCKS;

  ngAfterViewInit(): void {
    if (isPlatformBrowser(this.platformId)) {
      this.initMap();
    }
  }

  ngOnDestroy(): void {
    if (this.map) {
      this.map.remove();
    }
  }

  private async initMap(): Promise<void> {
    const L = await import('leaflet');
    this.L = L;

    // EAFIT campus bounds (SW corner, NE corner)
    const campusBounds = L.latLngBounds(
      [6.1920, -75.5810],  // SW
      [6.2070, -75.5720]   // NE
    );

    this.map = L.map('campus-map', {
      center: [6.2000, -75.5778],
      zoom: 17,
      minZoom: 16,
      maxZoom: 20,
      maxBounds: campusBounds,
      maxBoundsViscosity: 1.0,
      zoomControl: true,
      attributionControl: true
    });

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 20,
      attribution: '&copy; OpenStreetMap contributors'
    }).addTo(this.map);

    // Custom icon — iconAnchor at bottom-center so pin tip = exact coordinate
    const blockIcon = L.icon({
      iconUrl: 'https://cdn.jsdelivr.net/npm/leaflet@1.9.4/dist/images/marker-icon.png',
      iconRetinaUrl: 'https://cdn.jsdelivr.net/npm/leaflet@1.9.4/dist/images/marker-icon-2x.png',
      shadowUrl: 'https://cdn.jsdelivr.net/npm/leaflet@1.9.4/dist/images/marker-shadow.png',
      iconSize: [25, 41],
      iconAnchor: [12, 41],     // tip of the pin = the coordinate
      popupAnchor: [1, -34],
      shadowSize: [41, 41]
    });

    // Add markers for all blocks
    for (const block of CAMPUS_BLOCKS) {
      const marker = L.marker([block.lat, block.lng], { icon: blockIcon })
        .addTo(this.map)
        .bindPopup(`<strong>Bloque ${block.code}</strong><br>${block.name.split(' — ')[1] || ''}`);

      marker.on('click', () => this.selectBlock(block));
      this.markers.set(block.code, marker);
    }

    // ── Coordinate extractor (dev tool) ──
    // Click anywhere on the map → coordinates printed to browser console (F12)
    this.map.on('click', (e: any) => {
      console.log(`📍 Lat: ${e.latlng.lat.toFixed(5)}, Lng: ${e.latlng.lng.toFixed(5)}`);
    });
  }

  protected search(): void {
    const q = this.searchQuery.trim();
    if (!q) return;

    this.notFound.set(false);
    this.semanticResults.set([]);
    this.selectedBlock.set(null);
    this.panelOpen.set(false);

    // 1. Try exact match by block code
    const exactMatch = CAMPUS_BLOCKS.find(
      (b) => b.code === q || b.code === q.replace(/^bloque\s*/i, '')
    );

    if (exactMatch) {
      this.focusBlock(exactMatch);
      return;
    }

    // 2. Try partial name match
    const normalizedQ = q.toLowerCase();
    const nameMatch = CAMPUS_BLOCKS.find(
      (b) =>
        b.name.toLowerCase().includes(normalizedQ) ||
        b.services.some((s) => s.toLowerCase().includes(normalizedQ))
    );

    if (nameMatch) {
      this.focusBlock(nameMatch);
      return;
    }

    // 3. Semantic search via backend
    this.loading.set(true);
    this.http
      .get<BusquedaResponse>(this.apiUrl, { params: { q } })
      .subscribe({
        next: (data) => {
          const results = data.resultados ?? [];
          this.loading.set(false);

          if (results.length === 0) {
            this.notFound.set(true);
            return;
          }

          this.semanticResults.set(results);

          // Try to focus the top result on the map
          const topCode = results[0].codigo_bloque;
          const mapBlock = CAMPUS_BLOCKS.find((b) => b.code === topCode);
          if (mapBlock) {
            this.focusBlock(mapBlock, false);
          }

          this.panelOpen.set(true);
        },
        error: () => {
          this.loading.set(false);
          this.notFound.set(true);
        }
      });
  }

  protected selectBlock(block: BlockInfo): void {
    this.selectedBlock.set(block);
    this.semanticResults.set([]);
    this.notFound.set(false);
    this.panelOpen.set(true);

    if (this.map) {
      this.map.setView([block.lat, block.lng], 18, { animate: true });
      const marker = this.markers.get(block.code);
      if (marker) marker.openPopup();
    }
  }

  protected closePanel(): void {
    this.panelOpen.set(false);
    this.selectedBlock.set(null);
    this.semanticResults.set([]);
  }

  private focusBlock(block: BlockInfo, openPanel = true): void {
    this.selectedBlock.set(block);
    this.notFound.set(false);

    if (this.map) {
      this.map.setView([block.lat, block.lng], 18, { animate: true });
      const marker = this.markers.get(block.code);
      if (marker) marker.openPopup();
    }

    if (openPanel) {
      this.panelOpen.set(true);
    }
  }

  protected focusBlockByCode(code: string): void {
    const block = CAMPUS_BLOCKS.find((b) => b.code === code);
    if (block) this.focusBlock(block);
  }

  protected clearSearch(): void {
    this.searchQuery = '';
    this.notFound.set(false);
    this.semanticResults.set([]);
    this.selectedBlock.set(null);
    this.panelOpen.set(false);

    if (this.map) {
      this.map.setView([6.2000, -75.5778], 17, { animate: true });
    }
  }
}
