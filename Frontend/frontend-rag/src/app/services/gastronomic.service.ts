import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { getApiBaseUrl } from '../core/api-url';

@Injectable({
  providedIn: 'root'
})
export class GastronomicService {
  private apiUrl: string;

  constructor(private http: HttpClient) {
    this.apiUrl = getApiBaseUrl();
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
