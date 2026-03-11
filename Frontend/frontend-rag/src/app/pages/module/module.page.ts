import { Component, computed, inject, signal, DestroyRef } from '@angular/core';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { FormsModule } from '@angular/forms';

export type BackendResponse = {
  respuesta?: string;
  error?: string;
};

export type Professor = {
  nombre: string;
  titulos: string;
};

export type Ubicacion = {
  codigo_bloque: string;
  piso: number;
  descripcion_semantica: string;
  metadatos: Record<string, unknown>;
  similarity: number;
};

export type BusquedaResponse = {
  resultados: Ubicacion[];
};

export type ModuleContent = {
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
  private readonly destroyRef = inject(DestroyRef);
  
  private readonly apiUrl = 'http://127.0.0.1:8001/api/llamaindex/';
  private readonly apiUrlBuscar = 'http://127.0.0.1:8000/api/llamaindex/buscar/';

  protected prompt = '';
  protected readonly lastQuery = signal('');
  protected readonly loading = signal(false);
  protected readonly errorMessage = signal('');
  protected readonly response = signal<BackendResponse | null>(null);
  
  protected readonly chatHistory = signal<{ role: 'user' | 'bot'; text: string }[]>([]);
  protected readonly professorsList = signal<Professor[]>([]);
  protected readonly resultados = signal<Ubicacion[]>([]);
  
  protected readonly searchQuery = signal('');
  protected readonly selectedFilter = signal('');

  protected readonly availableFilters = computed(() => {
    const list = this.professorsList();
    const categories = new Set<string>();
    
    for (const prof of list) {
        const match = prof.titulos.match(/\(([^)]+)\)$/);
        if (match && match[1]) {
            const cats = match[1].split('/').map(c => c.trim());
            cats.forEach(c => categories.add(c));
        }
    }
    return Array.from(categories).sort();
  });

  protected readonly filteredProfessors = computed(() => {
    const query = this.searchQuery().toLowerCase();
    const filter = this.selectedFilter();
    
    return this.professorsList().filter(prof => {
      const matchesText = prof.nombre.toLowerCase().includes(query) || 
                          prof.titulos.toLowerCase().includes(query);
      
      const matchesFilter = filter ? prof.titulos.includes(filter) : true;
      
      return matchesText && matchesFilter;
    });
  });

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

  protected readonly isDirectory = computed(() => {
    const key = this.route.snapshot.data['moduleKey'] as string | undefined;
    return key === 'directory';
  });

  constructor() {
    this.route.queryParamMap.pipe(takeUntilDestroyed()).subscribe((params) => {
      if (this.isChat()) {
        const query = params.get('q')?.trim();
        if (query) {
          this.prompt = query;
          this.askBackend();
        }
      }
    });

    if (this.isDirectory()) {
      this.fetchDirectory();
    }
  }

  protected askBackend(): void {
    if (!this.isChat() || !this.prompt.trim()) {
      return;
    }

    const currentPrompt = this.prompt.trim();
    this.chatHistory.update((h) => [...h, { role: 'user', text: currentPrompt }]);

    this.loading.set(true);
    this.errorMessage.set('');
    this.prompt = '';

    const payload = { query: currentPrompt };

    this.http.post<BackendResponse>(`${this.apiUrl}query/`, payload).pipe(takeUntilDestroyed(this.destroyRef)).subscribe({
      next: (data) => {
        if (data.respuesta) {
          this.chatHistory.update((h) => [...h, { role: 'bot', text: data.respuesta! }]);
        } else if (data.error) {
          this.errorMessage.set(data.error);
        }
        this.loading.set(false);
      },
      error: () => {
        this.errorMessage.set('No se pudo conectar con el backend o ocurrió un error al procesar la solicitud.');
        this.loading.set(false);
      }
    });
  }

  // Se mantuvo la lógica de branchEmmanuel para búsquedas de ubicación separada de chat
  protected buscarUbicacionBackend(query: string): void {
    if (!query.trim()) return;
    
    this.lastQuery.set(query);
    this.loading.set(true);
    this.errorMessage.set('');
    this.resultados.set([]);

    this.http.get<BusquedaResponse>(this.apiUrlBuscar, {
      params: { q: query }
    }).pipe(takeUntilDestroyed(this.destroyRef)).subscribe({
      next: (data) => {
        this.resultados.set(data.resultados ?? []);
        this.loading.set(false);
      },
      error: () => {
        this.errorMessage.set('No se pudo conectar con el backend para buscar ubicación.');
        this.loading.set(false);
      }
    });
  }

  protected fetchDirectory(): void {
    this.loading.set(true);
    this.errorMessage.set('');
    this.http.get<Professor[]>(`${this.apiUrl}directorio/`).pipe(takeUntilDestroyed(this.destroyRef)).subscribe({
      next: (data) => {
        this.professorsList.set(data);
        this.loading.set(false);
      },
      error: () => {
        this.errorMessage.set('No se pudo cargar el directorio de profesores.');
        this.loading.set(false);
      }
    });
  }
}
