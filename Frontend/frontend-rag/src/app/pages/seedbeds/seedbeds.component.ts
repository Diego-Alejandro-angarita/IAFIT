import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterModule } from '@angular/router';
import { SeedbedsService } from '../../services/seedbeds.service';
import { Seedbed } from '../../models/seedbed.model';
import { LucideAngularModule } from 'lucide-angular';
import { Title } from '@angular/platform-browser';

@Component({
  selector: 'app-seedbeds',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterModule, LucideAngularModule],
  templateUrl: './seedbeds.component.html',
  styleUrl: './seedbeds.component.scss'
})
export class SeedbedsComponent implements OnInit {
  seedbeds: Seedbed[] = [];
  faculties: string[] = [];
  selectedFaculty = '';
  search = '';

  constructor(
  private seedbedsService: SeedbedsService,
  private cdr: ChangeDetectorRef,
  private titleService: Title
) {}

  ngOnInit(): void {
    this.titleService.setTitle('IAFIT - Semilleros de Investigación');
    this.loadSeedbeds();
    this.loadAllFaculties();
  }

  loadSeedbeds(): void {
    this.seedbedsService.getSeedbeds(this.selectedFaculty, this.search).subscribe({
      next: (data) => {
        this.seedbeds = data;
        this.cdr.detectChanges();
      },
      error: (error) => {
        console.error('Error loading seedbeds:', error);
        this.cdr.detectChanges();
      }
    });
  }

  loadAllFaculties(): void {
    this.seedbedsService.getSeedbeds().subscribe({
      next: (data) => {
        this.faculties = [...new Set(data.map(s => s.faculty))].sort();
        this.cdr.detectChanges();
      },
      error: (error) => {
        console.error('Error loading faculties:', error);
        this.cdr.detectChanges();
      }
    });
  }

  onSearch(): void {
    this.loadSeedbeds();
  }

  clearFilters(): void {
    this.selectedFaculty = '';
    this.search = '';
    this.loadSeedbeds();
  }
  getFacultyColor(faculty: string): string {
    const colors: Record<string, string> = {
      'Escuela de Ciencias Aplicadas e Ingeniería': '#3B82F6',
      'Escuela de Administración': '#10B981',
      'Escuela de Derecho': '#F59E0B',
      'Escuela de Finanzas, Economía y Gobierno': '#8B5CF6',
      'Escuela de Artes y Humanidades': '#EC4899',
      'Escuelas de Artes y Humanidades': '#EC4899'
   };

    return colors[faculty] || '#64748B';
  };
}
  