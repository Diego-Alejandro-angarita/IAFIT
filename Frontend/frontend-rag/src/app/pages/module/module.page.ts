import { Component, computed, inject, signal } from '@angular/core';
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
  private readonly apiUrl = 'http://127.0.0.1:8000/';

  protected prompt = '';
  protected readonly loading = signal(false);
  protected readonly errorMessage = signal('');
  protected readonly response = signal<BackendResponse | null>(null);

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
    if (!this.isChat()) {
      return;
    }

    this.loading.set(true);
    this.errorMessage.set('');

    this.http.get<BackendResponse>(this.apiUrl).pipe(takeUntilDestroyed()).subscribe({
      next: (data) => {
        this.response.set(data);
        this.loading.set(false);
      },
      error: () => {
        this.errorMessage.set('No se pudo conectar con el backend en http://127.0.0.1:8000/.');
        this.loading.set(false);
      }
    });
  }
}
