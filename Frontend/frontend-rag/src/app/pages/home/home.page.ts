import { Component, inject, OnInit } from '@angular/core';
import { Router, RouterLink } from '@angular/router';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import { EventosService } from '../../services/eventos.service';

interface ActionItem {
  id: string;
  title: string;
  colorClass: string;
}

@Component({
  selector: 'app-home-page',
  standalone: true,
  imports: [RouterLink, CommonModule, FormsModule],
  templateUrl: './home.page.html',
  styleUrl: './home.page.scss'
})
export class HomePage implements OnInit {
  // --- Variables para la IA ---
  protected userInput: string = '';
  protected isLoading: boolean = false;
  protected respuestaIA: string | null = null;
  protected eventosHoy: number = 0;

  private http = inject(HttpClient);
  private router = inject(Router);
  private eventosService = inject(EventosService);

  // --- Listas de navegación ---
  protected readonly quickActions: ActionItem[] = [
    { id: 'map',         title: 'Campus y Ubicación',  colorClass: 'blue'   },
    { id: 'classrooms',  title: 'Aulas Disponibles',   colorClass: 'green'  },
    { id: 'restaurants', title: 'Restaurantes',         colorClass: 'orange' },
    { id: 'events',      title: 'Eventos',              colorClass: 'purple' },
  ];

  protected readonly newFeatures: ActionItem[] = [
    { id: 'calendar',  title: 'Calendario Académico', colorClass: 'indigo' },
    { id: 'directory', title: 'Directorio',           colorClass: 'teal'   },
    { id: 'seedbeds',  title: 'Grupos y Semilleros',  colorClass: 'pink'   },
  ];

  protected readonly frequentQuestions: string[] = [
    '¿Dónde está el Bloque 38?',
    '¿Horario de la biblioteca?',
    '¿Cómo llegar a la cafetería central?',
    'Próximos eventos académicos'
  ];

  ngOnInit(): void {
  this.eventosService.getEventos('hoy').subscribe({
    next: (eventos) => {
      console.log('Eventos hoy:', eventos); // ← ver qué llega
      this.eventosHoy = eventos.length;
    },
    error: (err) => {
      console.error('Error eventos:', err); // ← ver si falla
      this.eventosHoy = 0;
    }
  });
}

  // --- Lógica de navegación a Chat ---
  protected navegarAlChat(pregunta: string) {
    if (!pregunta.trim()) return;
    this.router.navigate(['/chat'], { queryParams: { q: pregunta } });
  }
}
