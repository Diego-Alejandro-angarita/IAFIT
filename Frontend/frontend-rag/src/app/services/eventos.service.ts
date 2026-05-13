// src/app/services/eventos.service.ts

import { Injectable, inject } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { apiUrl } from '../core/api-url';

export interface Evento {
  id: number;
  title: string;
  description: string;
  location: string;
  event_date: string;  // 'YYYY-MM-DD'
  event_time: string;  // 'HH:MM'
}

@Injectable({ providedIn: 'root' })
export class EventosService {
  private readonly http = inject(HttpClient);
  private readonly apiUrl = apiUrl('events/');

  // Mantenemos tu lógica original para vistas
  getEventos(vista: 'hoy' | 'semana' | 'todos' = 'hoy', fecha?: string): Observable<Evento[]> {
    let params = new HttpParams();
    if (fecha) {
      params = params.set('fecha', fecha);
    } else {
      params = params.set('vista', vista);
    }
    return this.http.get<Evento[]>(this.apiUrl, { params });
  }

  // AGREGADO: Método para obtener contexto completo para la IA
  getAllEventos(): Observable<Evento[]> {
    return this.http.get<Evento[]>(this.apiUrl, { params: new HttpParams().set('vista', 'todos') });
  }

  getEventoById(id: number): Observable<Evento> {
    return this.http.get<Evento>(`${this.apiUrl}${id}/`);
  }
}
