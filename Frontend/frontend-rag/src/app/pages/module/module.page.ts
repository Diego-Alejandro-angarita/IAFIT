import { Component, computed, inject, signal, OnInit, DestroyRef, ElementRef, ViewChild, AfterViewChecked } from '@angular/core';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { FormsModule } from '@angular/forms';
import { forkJoin } from 'rxjs';
import { EventosService, Evento } from '../../services/eventos.service';
import { apiUrl } from '../../core/api-url';

export type RAGResponse = {
  respuesta: string;
  fuente?: string;
};

export type Ubicacion = {
  codigo_bloque: string;
  piso: number;
  descripcion_semantica: string;
  metadatos: Record<string, unknown>;
  similarity: number;
};

export type EventoCalendario = {
  id: string;
  actividad: string;
  descripcion: string;
  dirigido_a: string;
  fecha_inicio: string;
  fecha_fin: string;
  periodo: string;
  similitud: number;
};

export type BusquedaResponse = {
  resultados: Ubicacion[];
};

export type CalendarioResponse = {
  resultados: EventoCalendario[];
};

export type Establishment = {
  id: number;
  name: string;
  establishment_type_display: string;
  location: string;
  current_status: {
    status: string;
    message: string;
  };
};

export type ChatMessage = {
  role: 'user' | 'bot';
  text: string;
  ubicaciones?: Ubicacion[];
  eventos?: EventoCalendario[];
  restaurantes?: Establishment[];
  isError?: boolean;
};

export type BackendResponse = {
  respuesta?: string;
  error?: string;
};

export type Professor = {
  nombre: string;
  titulos: string;
};

export type ModuleContent = {
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
export class ModulePage {
  private readonly route = inject(ActivatedRoute);
  private readonly http = inject(HttpClient);
  private readonly destroyRef = inject(DestroyRef);
  private readonly eventosService = inject(EventosService);

  private readonly directoryUrl = apiUrl('directorio/');
  private readonly askUrl = apiUrl('ask/');
  private readonly ragUrl = apiUrl('query/');
  private readonly apiUrlBuscar = apiUrl('buscar/');
  private readonly calendarApiUrl = apiUrl('calendario/buscar/');
  private readonly establishmentsUrl = apiUrl('establishments/');

  @ViewChild('messagesContainer') private messagesContainer!: ElementRef<HTMLDivElement>;
  private shouldScroll = false;

  protected prompt = '';
  protected readonly loading = signal(false);
  protected readonly errorMessage = signal('');
  protected readonly response = signal<BackendResponse | null>(null);

  // Chat state
  protected readonly messages = signal<ChatMessage[]>([
    { role: 'bot', text: '¡Hola! Soy el Asistente Virtual IAFIT. ¿En qué puedo ayudarte hoy?' }
  ]);

  // Directory state
  protected readonly professorsList = signal<Professor[]>([]);
  protected readonly searchQuery = signal('');
  protected readonly selectedFilter = signal('');

  // Location/Map state
  protected readonly lastQuery = signal('');
  protected readonly resultados = signal<Ubicacion[]>([]);

  // Events state
  protected readonly vistaActiva = signal<'hoy' | 'semana' | 'todos'>('hoy');
  protected readonly eventoSeleccionado = signal<Evento | null>(null);
  protected readonly eventosLoading = signal(false);
  protected readonly eventosError = signal('');
  protected readonly eventos = signal<Evento[]>([]);
  protected readonly fechaBusqueda = signal('');
  
  protected readonly today = new Date().toISOString().split('T')[0];

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

  protected readonly isDirectory = computed(() => {
    const key = this.route.snapshot.data['moduleKey'] as string | undefined;
    return key === 'directory';
  });

  protected readonly availableFilters = computed(() => {
    const list = this.professorsList();
    const domains = list.map(p => {
      const match = p.titulos.match(/\(([^)]+)\)$/);
      return match ? match[1].trim() : '';
    }).filter(d => Boolean(d));
    return Array.from(new Set(domains)).sort();
  });

  protected readonly filteredProfessors = computed(() => {
    let list = this.professorsList();
    const query = this.searchQuery().toLowerCase().trim();
    if (query) {
      list = list.filter(p => p.nombre.toLowerCase().includes(query) || p.titulos.toLowerCase().includes(query));
    }
    const filter = this.selectedFilter();
    if (filter) {
      list = list.filter(p => p.titulos.includes(`(${filter})`));
    }
    return list;
  });

  protected readonly eventosPorFecha = computed(() => {
    const evs = this.eventos();
    const grouped = evs.reduce((acc, ev) => {
      if (!acc[ev.event_date]) acc[ev.event_date] = [];
      acc[ev.event_date].push(ev);
      return acc;
    }, {} as Record<string, Evento[]>);
    return Object.keys(grouped).sort().map(date => ({
      date,
      events: grouped[date]
    }));
  });

  constructor() {
    this.route.queryParamMap.pipe(takeUntilDestroyed()).subscribe((params) => {
      if (!this.isChat()) return;
      const query = params.get('q')?.trim();
      if (query) {
        this.prompt = query;
        this.askBackend();
      }
    });

    if (this.isDirectory()) {
      this.fetchDirectory();
    }
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

    const queryLower = pregunta.toLowerCase();
    
    // Categorías de palabras clave
    const kwEventos = ['evento', 'eventos', 'actividad', 'actividades', 'agenda', 'conferencia', 'taller'];
    const kwUbicacion = ['bloque', 'piso', 'aula', 'ubicacion', 'ubicación', 'llegar a', 'campus', 'restaurante'];
    const kwCalendario = ['calendario', 'parcial', 'parciales', 'clase', 'clases', 'matrícula', 'matricula', 'semestre', 'requisito'];

    const kwRestaurantes = ['restaurant', 'comid', 'desayun', 'hambre', 'comer', 'almuerz'];

    const esEventos = kwEventos.some(k => queryLower.includes(k));
    const esUbicacion = kwUbicacion.some(k => queryLower.includes(k));
    const esCalendario = kwCalendario.some(k => queryLower.includes(k));
    const esRestaurante = kwRestaurantes.some(k => queryLower.includes(k));

    if (esEventos) {
      this.eventosService.getAllEventos().subscribe({
        next: (eventos) => {
          this.http.post<{ message_es: string }>(this.askUrl, {
            query: pregunta,
            contexto_eventos: eventos
          }).pipe(takeUntilDestroyed(this.destroyRef)).subscribe({
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
        error: () => this.fallBackToRag(pregunta)
      });
    } else if (esRestaurante) {
      this.http.get<Establishment[]>(this.establishmentsUrl).pipe(takeUntilDestroyed(this.destroyRef)).subscribe({
        next: (data) => {
          if (data.length > 0) {
            this.messages.update(msgs => [...msgs, { role: 'bot', text: 'Aquí tienes los restaurantes disponibles en el campus:', restaurantes: data }]);
          } else {
            this.messages.update(msgs => [...msgs, { role: 'bot', text: 'No encontré restaurantes registrados.' }]);
          }
          this.loading.set(false);
        },
        error: () => this.fallBackToRag(pregunta)
      });
    } else if (esUbicacion) {
      this.http.get<BusquedaResponse>(this.apiUrlBuscar, { params: { q: pregunta } })
        .pipe(takeUntilDestroyed(this.destroyRef)).subscribe({
          next: (data) => {
            const res = data.resultados ?? [];
            if (res.length > 0) {
              this.messages.update(msgs => [...msgs, { role: 'bot', text: 'Aquí tienes los resultados de ubicaciones:', ubicaciones: res }]);
            } else {
              // Si la búsqueda espacial no da resultados, enviar a RAG general
              this.fallBackToRag(pregunta);
            }
            this.loading.set(false);
          },
          error: () => this.fallBackToRag(pregunta)
        });
    } else if (esCalendario) {
      this.http.get<CalendarioResponse>(this.calendarApiUrl, { params: { q: pregunta } })
        .pipe(takeUntilDestroyed(this.destroyRef)).subscribe({
          next: (data) => {
            const contexto = JSON.stringify(data.resultados);
            this.fallBackToRag(pregunta, contexto);
          },
          error: () => this.fallBackToRag(pregunta)
        });
    } else {
      // Pregunta general o de profesores
      this.fallBackToRag(pregunta);
    }
  }

  private fallBackToRag(pregunta: string, contexto: string = ''): void {
    this.http.post<RAGResponse>(this.ragUrl, { query: pregunta, contexto: contexto })
      .pipe(takeUntilDestroyed(this.destroyRef)).subscribe({
        next: (data) => {
          this.messages.update(msgs => [...msgs, { role: 'bot', text: data.respuesta }]);
          this.loading.set(false);
        },
        error: () => {
          this.messages.update(msgs => [...msgs, { role: 'bot', text: 'No pude conectarme con el servidor. Verifica que el backend esté corriendo.' }]);
          this.loading.set(false);
        }
      });
  }

  // ── Búsqueda de Ubicación ────────────────────────────────────
  protected buscarUbicacionBackend(query: string): void {
    if (!query.trim()) return;
    
    this.lastQuery.set(query);
    this.messages.update(msgs => [...msgs, { role: 'user', text: query }]);
    this.loading.set(true);

    const qLower = query.toLowerCase();
    const isRestaurantQuery = qLower.includes('restaurant') || qLower.includes('comid') || qLower.includes('desayun') || qLower.includes('hambre') || qLower.includes('comer') || qLower.includes('almuerz');

    if (isRestaurantQuery) {
      this.http.get<Establishment[]>(this.establishmentsUrl).subscribe({
        next: (data) => {
          if (data.length > 0) {
            this.messages.update(msgs => [...msgs, { role: 'bot', text: 'Aquí tienes los restaurantes disponibles en el campus:', restaurantes: data }]);
          } else {
            this.messages.update(msgs => [...msgs, { role: 'bot', text: 'No encontré restaurantes registrados.' }]);
          }
          this.loading.set(false);
        },
        error: () => {
          this.messages.update(msgs => [...msgs, { role: 'bot', text: 'Error al obtener la lista de restaurantes.', isError: true }]);
          this.loading.set(false);
        }
      });
      return;
    }

    this.http.get<BusquedaResponse>(this.apiUrlBuscar, {
      params: { q: query }
    }).pipe(takeUntilDestroyed(this.destroyRef)).subscribe({
      next: (data) => {
        const res = data.resultados ?? [];
        if (res.length > 0) {
          this.messages.update(msgs => [...msgs, { role: 'bot', text: 'Aquí tienes los resultados de ubicaciones:', ubicaciones: res }]);
        } else {
          this.messages.update(msgs => [...msgs, { role: 'bot', text: 'No encontré ubicaciones relacionadas con tu búsqueda.' }]);
        }
        this.loading.set(false);
      },
      error: () => {
        this.errorMessage.set('No se pudo conectar con el backend para buscar ubicación.');
        this.messages.update(msgs => [...msgs, { 
          role: 'bot', 
          text: 'No se pudo conectar con el backend.', 
          isError: true 
        }]);
        this.loading.set(false);
      }
    });
  }

  // ── Directorio ─────────────────────────────────────────────
  protected fetchDirectory(): void {
    this.loading.set(true);
    this.errorMessage.set('');
    this.http.get<Professor[]>(this.directoryUrl).pipe(takeUntilDestroyed(this.destroyRef)).subscribe({
      next: (data) => {
        this.professorsList.set(data);
        this.loading.set(false);
      },
      error: () => {
        this.errorMessage.set('No se pudo cargar el directorio de profesores.');
        this.messages.update(msgs => [...msgs, {
          role: 'bot',
          text: 'No se pudo conectar con el backend.',
          isError: true
        }]);
        this.loading.set(false);
      }
    });
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
