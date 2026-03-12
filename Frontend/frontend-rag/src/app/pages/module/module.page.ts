// src/app/pages/module/module.page.ts

import { Component, computed, inject, signal, OnInit } from '@angular/core';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { FormsModule } from '@angular/forms';
import { EventosService, Evento } from '../../services/eventos.service';

type RAGResponse = {
  respuesta: string;
};

type ChatMessage = {
  role: 'user' | 'bot';
  text: string;
};

type ModuleContent = {
  title: string;
  description: string;
};

const MODULE_CONTENT: Record<string, ModuleContent> = {
  map:         { title: 'Campus y Ubicacion',      description: 'Vista para integrar mapa interactivo y navegacion por bloques.' },
  classrooms:  { title: 'Aulas Disponibles',        description: 'Vista para mostrar disponibilidad de aulas en tiempo real.' },
  restaurants: { title: 'Restaurantes',             description: 'Vista para listar menus, horarios y ubicacion de cafeterias.' },
  events:      { title: 'Agenda del Campus',         description: 'Eventos académicos y culturales del campus.' },
  calendar:    { title: 'Calendario Academico',     description: 'Vista para fechas clave, entregas y periodos institucionales.' },
  directory:   { title: 'Directorio',               description: 'Vista para contactos de profesores y personal administrativo.' },
  groups:      { title: 'Grupos y Semilleros',       description: 'Vista para comunidades estudiantiles y semilleros de investigacion.' },
  profile:     { title: 'Perfil',                   description: 'Vista para datos de usuario, rol y configuraciones personales.' },
  chat:        { title: 'Asistente IA',             description: 'Vista para consultas en lenguaje natural sobre servicios IAFIT.' },
};

@Component({
  selector: 'app-module-page',
  imports: [RouterLink, FormsModule],
  templateUrl: './module.page.html',
  styleUrl: './module.page.scss'
})
export class ModulePage implements OnInit {
  private readonly route          = inject(ActivatedRoute);
  private readonly http           = inject(HttpClient);
  private readonly eventosService = inject(EventosService);
  private readonly ragUrl         = 'http://127.0.0.1:8001/api/query';
  private readonly askUrl         = 'http://127.0.0.1:8001/api/ask/';

  // ── Chat ──────────────────────────────────────────────────
  protected prompt                = '';
  protected readonly loading      = signal(false);
  protected readonly errorMessage = signal('');
  protected readonly messages     = signal<ChatMessage[]>([
    { role: 'bot', text: '¡Hola! Soy el Asistente Virtual IAFIT. Puedes preguntarme sobre eventos, servicios o cualquier información del campus.' }
  ]);

  // ── Events ────────────────────────────────────────────────
  protected readonly eventos            = signal<Evento[]>([]);
  protected readonly eventoSeleccionado = signal<Evento | null>(null);
  protected readonly eventosLoading     = signal(false);
  protected readonly eventosError       = signal('');
  protected readonly vistaActiva        = signal<'hoy' | 'semana' | 'todos'>('hoy');
  protected readonly fechaBusqueda      = signal('');

  // Fecha actual en zona horaria de Colombia
  protected readonly today = (() => {
    const now = new Date();
    const bogota = new Date(now.toLocaleString('en-US', { timeZone: 'America/Bogota' }));
    const y = bogota.getFullYear();
    const m = String(bogota.getMonth() + 1).padStart(2, '0');
    const d = String(bogota.getDate()).padStart(2, '0');
    return `${y}-${m}-${d}`;
  })();

  protected readonly eventosPorFecha = computed(() => {
    const mapa = new Map<string, Evento[]>();
    for (const e of this.eventos()) {
      if (!mapa.has(e.event_date)) mapa.set(e.event_date, []);
      mapa.get(e.event_date)!.push(e);
    }
    return Array.from(mapa.entries()).map(([date, events]) => ({ date, events }));
  });

  // ── Computed flags ─────────────────────────────────────────
  protected readonly content = computed(() => {
    const key = this.route.snapshot.data['moduleKey'] as string | undefined;
    return (key && MODULE_CONTENT[key]) || { title: 'Modulo', description: 'Contenido pendiente de configurar.' };
  });

  protected readonly isChat = computed(() =>
    this.route.snapshot.data['moduleKey'] === 'chat'
  );

  protected readonly isEvents = computed(() =>
    this.route.snapshot.data['moduleKey'] === 'events'
  );

  constructor() {
    this.route.queryParamMap.pipe(takeUntilDestroyed()).subscribe((params) => {
      if (!this.isChat()) return;
      const query = params.get('q')?.trim();
      if (query) {
        this.prompt = query;
        this.askBackend();
      }
    });
  }

  ngOnInit(): void {
    if (this.isEvents()) {
      this.cargarEventos('hoy');
    }
  }

  // ── Chat: envía pregunta ────────────────────────────────────
  protected askBackend(): void {
    const pregunta = this.prompt.trim();
    if (!pregunta || this.loading()) return;

    this.messages.update(msgs => [...msgs, { role: 'user', text: pregunta }]);
    this.prompt = '';
    this.loading.set(true);
    this.errorMessage.set('');

    const keywords = ['evento', 'eventos', 'actividad', 'actividades',
                      'hoy', 'mañana', 'semana', 'qué hay', 'que hay',
                      'agenda', 'próximos', 'proximos', 'marzo', 'abril',
                      'disponible', 'campus'];
    const esEventos = keywords.some(k => pregunta.toLowerCase().includes(k));

    if (esEventos) {
      this.eventosService.getAllEventos().subscribe({
        next: (eventos) => {
          this.http.post<{ message_es: string }>(this.askUrl, {
            query: pregunta,
            contexto_eventos: eventos
          }).subscribe({
            next: (data) => {
              this.messages.update(msgs => [...msgs, { role: 'bot', text: data.message_es }]);
              this.loading.set(false);
            },
            error: () => {
              this.messages.update(msgs => [...msgs, { role: 'bot', text: 'Error al consultar la IA de eventos.' }]);
              this.loading.set(false);
            }
          });
        },
        error: () => {
          // Si falla cargar eventos, usa el RAG normal
          this.http.post<RAGResponse>(this.ragUrl, { query: pregunta }).subscribe({
            next: (data) => {
              this.messages.update(msgs => [...msgs, { role: 'bot', text: data.respuesta }]);
              this.loading.set(false);
            },
            error: () => {
              this.messages.update(msgs => [...msgs, { role: 'bot', text: 'No pude conectarme con el servidor.' }]);
              this.loading.set(false);
            }
          });
        }
      });
    } else {
      this.http.post<RAGResponse>(this.ragUrl, { query: pregunta }).subscribe({
        next: (data) => {
          this.messages.update(msgs => [...msgs, { role: 'bot', text: data.respuesta }]);
          this.loading.set(false);
        },
        error: () => {
          this.messages.update(msgs => [...msgs, { role: 'bot', text: 'No pude conectarme con el servidor. Verifica que el backend esté corriendo en http://127.0.0.1:8001/' }]);
          this.loading.set(false);
        }
      });
    }
  }

  // ── Events ─────────────────────────────────────────────────
  protected cargarEventos(vista: 'hoy' | 'semana' | 'todos'): void {
    this.vistaActiva.set(vista);
    this.eventoSeleccionado.set(null);
    this.eventosLoading.set(true);
    this.eventosError.set('');
    this.eventosService.getEventos(vista).subscribe({
      next: (data) => { this.eventos.set(data); this.eventosLoading.set(false); },
      error: () => { this.eventosError.set('No se pudo conectar con el servidor.'); this.eventosLoading.set(false); }
    });
  }

  protected buscarPorFecha(): void {
    const fecha = this.fechaBusqueda();
    if (!fecha) return;
    this.eventoSeleccionado.set(null);
    this.eventosLoading.set(true);
    this.eventosError.set('');
    this.eventosService.getEventos('hoy', fecha).subscribe({
      next: (data) => { this.eventos.set(data); this.eventosLoading.set(false); },
      error: () => { this.eventosError.set('Error al buscar eventos.'); this.eventosLoading.set(false); }
    });
  }

  protected verDetalle(evento: Evento): void { this.eventoSeleccionado.set(evento); }
  protected volverALista(): void             { this.eventoSeleccionado.set(null); }
  protected esHoy(fecha: string): boolean    { return fecha === this.today; }
  protected setFechaBusqueda(valor: string)  { this.fechaBusqueda.set(valor); }

  get todayDisplay(): string { return this.formatearFecha(this.today); }

  protected formatearFecha(fecha: string): string {
    const [y, m, d] = fecha.split('-');
    return `${d}/${m}/${y}`;
  }
}