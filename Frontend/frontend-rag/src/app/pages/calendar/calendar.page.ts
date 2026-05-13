import { Component, OnInit, signal, computed } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { RouterLink } from '@angular/router';
import { DatePipe } from '@angular/common';
import { apiUrl } from '../../core/api-url';

type CalendarEvent = {
  id: string;
  actividad: string;
  descripcion: string;
  dirigido_a: string;
  fecha_inicio: string;
  fecha_fin: string;
  periodo: string;
};

type CalendarResponse = {
  eventos: CalendarEvent[];
};

const CATEGORY_MAP: Record<string, string[]> = {
  'Académico': ['Inicio de clases', 'Evaluaciones finales', 'Registro de materias', 'Solicitud levantamiento de requisitos'],
  'Administrativo': ['Formulario de inscripción pregrado', 'Pago de matrícula estudiantes nuevos'],
  'Extracurricular': []
};

function getCategory(actividad: string): string {
  for (const [cat, acts] of Object.entries(CATEGORY_MAP)) {
    if (acts.some(a => actividad.toLowerCase().includes(a.toLowerCase()))) {
      return cat;
    }
  }
  return 'Académico';
}

const CATEGORY_COLORS: Record<string, string> = {
  'Académico': '#6366f1',
  'Administrativo': '#f59e0b',
  'Extracurricular': '#10b981'
};

@Component({
  selector: 'app-calendar-page',
  imports: [RouterLink, DatePipe],
  templateUrl: './calendar.page.html',
  styleUrl: './calendar.page.scss'
})
export class CalendarPage implements OnInit {
  protected readonly loading = signal(true);
  protected readonly error = signal('');
  protected readonly events = signal<(CalendarEvent & { categoria: string })[]>([]);
  protected readonly activeFilter = signal('Todos');
  protected readonly selectedEvent = signal<(CalendarEvent & { categoria: string }) | null>(null);

  protected readonly categories = ['Todos', 'Académico', 'Administrativo', 'Extracurricular'];

  protected readonly filteredEvents = computed(() => {
    const filter = this.activeFilter();
    const all = this.events();
    if (filter === 'Todos') return all;
    return all.filter(e => e.categoria === filter);
  });

  constructor(private http: HttpClient) {}

  ngOnInit(): void {
    this.http.get<CalendarResponse>(apiUrl('calendario/'))
      .subscribe({
        next: (data) => {
          const enriched = (data.eventos ?? []).map(e => ({
            ...e,
            categoria: getCategory(e.actividad)
          }));
          this.events.set(enriched);
          this.loading.set(false);
        },
        error: () => {
          this.error.set('No se pudo cargar el calendario académico.');
          this.loading.set(false);
        }
      });
  }

  protected setFilter(cat: string): void {
    this.activeFilter.set(cat);
    this.selectedEvent.set(null);
  }

  protected selectEvent(event: (CalendarEvent & { categoria: string }) | null): void {
    this.selectedEvent.set(event);
  }

  protected getCategoryColor(cat: string): string {
    return CATEGORY_COLORS[cat] ?? '#6b7280';
  }

  protected isActive(event: CalendarEvent): boolean {
    const now = new Date();
    return new Date(event.fecha_inicio) <= now && now <= new Date(event.fecha_fin);
  }
}
