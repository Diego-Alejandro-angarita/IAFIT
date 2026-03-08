import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { GastronomicService } from '../../services/gastronomic.service';

@Component({
  selector: 'app-gastronomic-offer',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './gastronomic-offer.component.html',
  styleUrls: ['./gastronomic-offer.component.scss']
})
export class GastronomicOfferComponent implements OnInit {
  establishments: any[] = [];
  filteredEstablishments: any[] = [];
  categories: any[] = [];
  selectedCategory: string | null = null;
  loading = true;
  error: string | null = null;

  constructor(private gastronomicService: GastronomicService) {}

  ngOnInit(): void {
    this.loadCategories();
    this.loadEstablishments();
  }

  /**
   * Carga todas las categorías disponibles
   */
  loadCategories(): void {
    this.gastronomicService.getCategories().subscribe({
      next: (categories: any) => {
        this.categories = categories;
      },
      error: (err: any) => {
        console.error('Error cargando categorías', err);
        this.error = 'No se pudieron cargar las categorías';
      }
    });
  }

  /**
   * Carga todos los establecimientos
   */
  loadEstablishments(): void {
    this.loading = true;
    this.gastronomicService.getEstablishments().subscribe({
      next: (data: any) => {
        this.establishments = data;
        this.filteredEstablishments = data;
        this.loading = false;
      },
      error: (err: any) => {
        console.error('Error cargando establecimientos', err);
        this.error = 'No se pudieron cargar los establecimientos';
        this.loading = false;
      }
    });
  }

  /**
   * Filtra establecimientos por categoría
   */
  filterByCategory(category: string | null): void {
    this.selectedCategory = category;

    if (!category) {
      // Mostrar todos
      this.filteredEstablishments = [...this.establishments];
    } else {
      // Filtrar por categoría
      this.filteredEstablishments = this.establishments.filter(est =>
        est.categories.some((cat: any) => cat.name === category)
      );
    }
  }

  /**
   * Obtiene la clase CSS para el badge de estado
   */
  getStatusClass(status: string): string {
    return status === 'Open' ? 'badge-success' : 'badge-danger';
  }

  /**
   * Obtiene el icono para el status
   */
  getStatusIcon(status: string): string {
    return status === 'Open' ? '✓' : '✕';
  }

  /**
   * Devuelve el mensaje del estado vacío para filtros
   */
  getEmptyMessage(): string {
    if (this.selectedCategory) {
      return `No hay restaurantes en la categoría "${this.selectedCategory}" por el momento.`;
    }
    return 'No hay establecimientos disponibles';
  }
}
