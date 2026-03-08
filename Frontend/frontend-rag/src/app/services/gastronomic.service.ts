import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class GastronomicService {
  private apiUrl: string;

  constructor(private http: HttpClient) {
    // Determinar la URL base dinámicamente
    const hostname = window.location.hostname;
    const protocol = window.location.protocol;
    
    if (hostname === 'localhost' || hostname === '127.0.0.1') {
      // Desarrollo local
      this.apiUrl = 'http://localhost:8000/api/establishments/';
    } else {
      // Codespaces u otro ambiente
      this.apiUrl = `${protocol}//${hostname.replace('-4200.', '-8000.')}:443/api/establishments/`;
      // Alternativa simplificada
      const baseUrl = window.location.origin.replace('-4200.', '-8000.');
      this.apiUrl = `${baseUrl}/api/establishments/`;
    }
  }

  /**
   * Obtiene la lista de todos los establecimientos
   */
  getEstablishments(): Observable<any[]> {
    return this.http.get<any[]>(this.apiUrl);
  }

  /**
   * Obtiene establecimientos filtrados por categoría
   */
  getEstablishmentsByCategory(category: string): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}by_category/`, { 
      params: { category } 
    });
  }

  /**
   * Obtiene establecimientos que están abiertos actualmente
   */
  getOpenEstablishments(): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}open_now/`);
  }

  /**
   * Obtiene todas las categorías disponibles
   */
  getCategories(): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}categories/`);
  }

  /**
   * Obtiene un establecimiento específico por ID
   */
  getEstablishment(id: number): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}${id}/`);
  }
}
