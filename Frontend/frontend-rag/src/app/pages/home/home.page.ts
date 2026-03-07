import { Component } from '@angular/core';
import { RouterLink } from '@angular/router';

interface ActionItem {
  id: string;
  title: string;
  colorClass: string;
}

@Component({
  selector: 'app-home-page',
  imports: [RouterLink],
  templateUrl: './home.page.html',
  styleUrl: './home.page.scss'
})
export class HomePage {
  protected readonly quickActions: ActionItem[] = [
    { id: 'map', title: 'Campus y Ubicación', colorClass: 'blue' },
    { id: 'classrooms', title: 'Aulas Disponibles', colorClass: 'green' },
    { id: 'restaurants', title: 'Restaurantes', colorClass: 'orange' },
    { id: 'events', title: 'Eventos', colorClass: 'purple' },
  ];

  protected readonly newFeatures: ActionItem[] = [
    { id: 'calendar', title: 'Calendario Académico', colorClass: 'indigo' },
    { id: 'directory', title: 'Directorio', colorClass: 'teal' },
    { id: 'groups', title: 'Grupos y Semilleros', colorClass: 'pink' },
  ];

  protected readonly frequentQuestions: string[] = [
    '¿Dónde está el Bloque 38?',
    '¿Horario de la biblioteca?',
    '¿Cómo llegar a la cafetería central?',
    'Próximos eventos académicos'
  ];
}
