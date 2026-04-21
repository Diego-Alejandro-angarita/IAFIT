import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, RouterModule } from '@angular/router';
import { Title } from '@angular/platform-browser';
import { SeedbedsService } from '../../services/seedbeds.service';
import { Seedbed } from '../../models/seedbed.model';

@Component({
  selector: 'app-seedbed-detail',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './seedbed-detail.component.html',
  styleUrl: './seedbed-detail.component.scss'
})
export class SeedbedDetailComponent implements OnInit {
  seedbed?: Seedbed;
  loading = true;
  errorMessage = '';

  constructor(
    private route: ActivatedRoute,
    private seedbedsService: SeedbedsService,
    private cdr: ChangeDetectorRef,
    private titleService: Title
  ) {}

  ngOnInit(): void {
    const id = Number(this.route.snapshot.paramMap.get('id'));

    if (!id || isNaN(id)) {
      this.loading = false;
      this.errorMessage = 'ID de semillero inválido.';
      this.titleService.setTitle('IAFIT - Error');
      this.cdr.detectChanges();
      return;
    }

    this.seedbedsService.getSeedbed(id).subscribe({
      next: (data) => {
        this.seedbed = data;
        this.loading = false;
        this.errorMessage = '';
        this.titleService.setTitle(`IAFIT - ${data.name}`);
        this.cdr.detectChanges();
      },
      error: (error) => {
        console.error('Error loading seedbed detail:', error);
        this.seedbed = undefined;
        this.loading = false;
        this.errorMessage = 'No se pudo cargar la información del semillero.';
        this.titleService.setTitle('IAFIT - Error');
        this.cdr.detectChanges();
      }
    });
  }
}