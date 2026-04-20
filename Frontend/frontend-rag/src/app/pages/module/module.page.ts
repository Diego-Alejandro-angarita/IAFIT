import { Component, computed, inject, signal, ViewChild, ElementRef, AfterViewChecked } from '@angular/core';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { FormsModule } from '@angular/forms';

type BackendResponse = {
  status: string;
  message_es: string;
  message_en: string;
  ui_modules: string[];
};

type Ubicacion = {
  codigo_bloque: string;
  piso: number;
  descripcion_semantica: string;
  metadatos: Record<string, unknown>;
  similarity: number;
};

type Establishment = {
  id: number;
  name: string;
  establishment_type_display: string;
  location: string;
  current_status: {
    status: string;
    message: string;
  };
};

type BusquedaResponse = {
  resultados: Ubicacion[];
};

export type ChatMessage = {
  role: 'user' | 'bot';
  text: string;
  ubicaciones?: Ubicacion[];
  restaurantes?: Establishment[];
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
export class ModulePage {
  private readonly route = inject(ActivatedRoute);
  private readonly http = inject(HttpClient);
  private readonly apiUrl = 'http://127.0.0.1:8001/api/buscar/';
  private readonly calendarApiUrl = 'http://127.0.0.1:8001/api/calendario/buscar/';

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
      if (!this.isChat()) {
        return;
      }

      const query = params.get('q')?.trim();
      if (query) {
        this.prompt = query;
        this.askBackend();
      }
    });
  }

  protected askBackend(): void {
    if (!this.isChat() || !this.prompt.trim()) {
      return;
    }

    const query = this.prompt.trim();
    this.prompt = '';
    
    // Add user message to UI
    this.messages.update(msgs => [...msgs, { role: 'user', text: query }]);
    this.loading.set(true);

    const qLower = query.toLowerCase();
    const isRestaurantQuery = qLower.includes('restaurant') || qLower.includes('comid') || qLower.includes('desayun') || qLower.includes('hambre') || qLower.includes('comer') || qLower.includes('almuerz');

    if (isRestaurantQuery) {
      this.http.get<Establishment[]>('http://127.0.0.1:8001/api/establishments/').subscribe({
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

    this.http.get<BusquedaResponse>(this.apiUrl, {
      params: { q: query }
    }).subscribe({
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
        this.messages.update(msgs => [...msgs, { 
          role: 'bot', 
          text: 'No se pudo conectar con el backend.', 
          isError: true 
        }]);
        this.loading.set(false);
      }
    });
  }
}
