import { Component, computed, inject, signal, ElementRef, ViewChild, AfterViewChecked } from '@angular/core';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { FormsModule } from '@angular/forms';
import { forkJoin } from 'rxjs';

type Ubicacion = {
  codigo_bloque: string;
  piso: number;
  descripcion_semantica: string;
  metadatos: Record<string, unknown>;
  similarity: number;
};

type EventoCalendario = {
  id: string;
  actividad: string;
  descripcion: string;
  dirigido_a: string;
  fecha_inicio: string;
  fecha_fin: string;
  periodo: string;
  similitud: number;
};

type BusquedaResponse = {
  resultados: Ubicacion[];
};

type CalendarioResponse = {
  resultados: EventoCalendario[];
};

type ChatMessage = {
  role: 'user' | 'bot';
  text: string;
  ubicaciones?: Ubicacion[];
  eventos?: EventoCalendario[];
  isError?: boolean;
};

type ModuleContent = {
  title: string;
  description: string;
};

const MODULE_CONTENT: Record<string, ModuleContent> = {
  map: {
    title: 'Campus y Ubicacion',
    description: 'Vista para integrar mapa interactivo y navegacion por bloques.'
  },
  classrooms: {
    title: 'Aulas Disponibles',
    description: 'Vista para mostrar disponibilidad de aulas en tiempo real.'
  },
  restaurants: {
    title: 'Restaurantes',
    description: 'Vista para listar menus, horarios y ubicacion de cafeterias.'
  },
  events: {
    title: 'Eventos',
    description: 'Vista para agenda de eventos academicos y culturales.'
  },
  calendar: {
    title: 'Calendario Academico',
    description: 'Vista para fechas clave, entregas y periodos institucionales.'
  },
  directory: {
    title: 'Directorio',
    description: 'Vista para contactos de profesores y personal administrativo.'
  },
  groups: {
    title: 'Grupos y Semilleros',
    description: 'Vista para comunidades estudiantiles y semilleros de investigacion.'
  },
  profile: {
    title: 'Perfil',
    description: 'Vista para datos de usuario, rol y configuraciones personales.'
  },
  chat: {
    title: 'Asistente IA',
    description: 'Vista para consultas en lenguaje natural sobre servicios IAFIT.'
  }
};

@Component({
  selector: 'app-module-page',
  imports: [RouterLink, FormsModule],
  templateUrl: './module.page.html',
  styleUrl: './module.page.scss'
})
export class ModulePage implements AfterViewChecked {
  private readonly route = inject(ActivatedRoute);
  private readonly http = inject(HttpClient);
  private readonly apiUrl = 'http://127.0.0.1:8000/api/llamaindex/buscar/';
  private readonly calendarApiUrl = 'http://127.0.0.1:8000/api/llamaindex/calendario/buscar/';

  @ViewChild('messagesContainer') private messagesContainer!: ElementRef<HTMLDivElement>;
  private shouldScroll = false;

  protected prompt = '';
  protected readonly loading = signal(false);
  protected readonly messages = signal<ChatMessage[]>([
    { role: 'bot', text: '¡Hola! Soy el Asistente Virtual IAFIT. ¿En qué puedo ayudarte hoy?' }
  ]);

  protected readonly content = computed(() => {
    const key = this.route.snapshot.data['moduleKey'] as string | undefined;
    return (key && MODULE_CONTENT[key]) || {
      title: 'Modulo',
      description: 'Contenido pendiente de configurar.'
    };
  });

  protected readonly isChat = computed(() => {
    const key = this.route.snapshot.data['moduleKey'] as string | undefined;
    return key === 'chat';
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
  }

  ngAfterViewChecked(): void {
    if (this.shouldScroll) {
      this.scrollToBottom();
      this.shouldScroll = false;
    }
  }

  private scrollToBottom(): void {
    const el = this.messagesContainer?.nativeElement;
    if (el) {
      el.scrollTop = el.scrollHeight;
    }
  }

  protected askBackend(): void {
    if (!this.isChat() || !this.prompt.trim()) return;

    const query = this.prompt.trim();
    this.prompt = '';

    // Add user message to history
    this.messages.update(msgs => [...msgs, { role: 'user', text: query }]);
    this.loading.set(true);
    this.shouldScroll = true;

    forkJoin({
      campus: this.http.get<BusquedaResponse>(this.apiUrl, { params: { q: query } }),
      calendario: this.http.get<CalendarioResponse>(this.calendarApiUrl, { params: { q: query } })
    }).subscribe({
      next: ({ campus, calendario }) => {
        const campusResults = campus.resultados ?? [];
        const calendarResults = calendario.resultados ?? [];

        const bestCampus = campusResults.length ? Math.max(...campusResults.map(r => r.similarity)) : 0;
        const bestCalendar = calendarResults.length ? Math.max(...calendarResults.map(r => r.similitud)) : 0;

        if (bestCalendar >= bestCampus && calendarResults.length) {
          this.messages.update(msgs => [...msgs, {
            role: 'bot',
            text: '📅 Calendario Académico',
            eventos: calendarResults
          }]);
        } else if (campusResults.length) {
          this.messages.update(msgs => [...msgs, {
            role: 'bot',
            text: '',
            ubicaciones: campusResults
          }]);
        } else {
          this.messages.update(msgs => [...msgs, {
            role: 'bot',
            text: 'No encontré resultados para tu consulta. Intenta reformular tu pregunta.'
          }]);
        }
        this.loading.set(false);
        this.shouldScroll = true;
      },
      error: () => {
        this.messages.update(msgs => [...msgs, {
          role: 'bot',
          text: 'No se pudo conectar con el backend.',
          isError: true
        }]);
        this.loading.set(false);
        this.shouldScroll = true;
      }
    });
  }
}
