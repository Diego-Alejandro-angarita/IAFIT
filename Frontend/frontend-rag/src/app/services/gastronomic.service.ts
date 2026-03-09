import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class GastronomicService {
  private apiUrl: string;

  constructor(private http: HttpClient) {
    // Usar URL relativa o determinar dinámicamente
    const hostname = window.location.hostname;
    const protocol = window.location.protocol;
    
    if (hostname === 'localhost' || hostname === '127.0.0.1') {
      // Desarrollo local - usar 8000
      this.apiUrl = 'http://127.0.0.1:8000/api';
    } else {
      // Otros ambientes - usar mismo puerto
      this.apiUrl = `${protocol}//${hostname}:8000/api`;
    }
    
    console.log('API URL configurada:', this.apiUrl);
  }

  /**
   * Obtiene la lista de todos los establecimientos
   */
  getEstablishments(): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/establishments/`);
  }

  /**
   * Obtiene establecimientos filtrados por categoría
   */
  getEstablishmentsByCategory(category: string): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/establishments/by_category/`, { 
      params: { category } 
    });
  }

  /**
   * Obtiene establecimientos que están abiertos actualmente
   */
  getOpenEstablishments(): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/establishments/open_now/`);
  }

  /**
   * Obtiene todas las categorías disponibles
   */
  getCategories(): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/categories/`);
  }

  /**
   * Obtiene un establecimiento específico por ID
   */
  getEstablishment(id: number): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/establishments/${id}/`);
  }
}
