import { Component } from '@angular/core';
import { RouterLink, RouterLinkActive } from '@angular/router';

@Component({
  selector: 'app-dock-nav',
  imports: [RouterLink, RouterLinkActive],
  template: `
    <nav class="dock-wrapper">
      <div class="dock-bar">
        <!-- Home -->
        <a routerLink="/" routerLinkActive="active" [routerLinkActiveOptions]="{ exact: true }" class="dock-btn">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
            stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M15 21v-8a1 1 0 0 0-1-1h-4a1 1 0 0 0-1 1v8"/>
            <path d="M3 10a2 2 0 0 1 .709-1.528l7-5.999a2 2 0 0 1 2.582 0l7 5.999A2 2 0 0 1 21 10v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/>
          </svg>
          <span class="dock-tooltip">Inicio</span>
          <span class="dock-dot"></span>
        </a>

        <!-- Chat / Asistente -->
        <a routerLink="/chat" routerLinkActive="active" class="dock-btn">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
            stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M7.9 20A9 9 0 1 0 4 16.1L2 22z"/>
          </svg>
          <span class="dock-tooltip">Asistente</span>
          <span class="dock-dot"></span>
        </a>

        <!-- Map -->
        <a routerLink="/map" routerLinkActive="active" class="dock-btn">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
            stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M20 10c0 4.993-5.539 10.193-7.399 11.799a1 1 0 0 1-1.202 0C9.539 20.193 4 14.993 4 10a8 8 0 0 1 16 0"/>
            <circle cx="12" cy="10" r="3"/>
          </svg>
          <span class="dock-tooltip">Mapa</span>
          <span class="dock-dot"></span>
        </a>

        <!-- Events -->
        <a routerLink="/events" routerLinkActive="active" class="dock-btn">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
            stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M8 2v4"/><path d="M16 2v4"/>
            <rect width="18" height="18" x="3" y="4" rx="2"/>
            <path d="M3 10h18"/>
          </svg>
          <span class="dock-tooltip">Eventos</span>
          <span class="dock-dot"></span>
        </a>

        <!-- Profile -->
        <a routerLink="/profile" routerLinkActive="active" class="dock-btn">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
            stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"/>
            <circle cx="12" cy="7" r="4"/>
          </svg>
          <span class="dock-tooltip">Perfil</span>
          <span class="dock-dot"></span>
        </a>
      </div>
    </nav>
  `,
  styles: [`
    :host { display: block; }

    .dock-wrapper {
      position: fixed;
      bottom: 1rem;
      left: 50%;
      transform: translateX(-50%);
      z-index: 50;
    }

    .dock-bar {
      display: flex;
      align-items: center;
      gap: 0.25rem;
      padding: 0.5rem 1rem;
      border-radius: 1rem;
      backdrop-filter: blur(24px);
      border: 1px solid rgba(255,255,255,0.2);
      background: rgba(255,255,255,0.8);
      box-shadow:
        0 0 6px rgba(0,0,0,0.03),
        0 4px 16px rgba(0,0,0,0.1),
        inset 0 0 0 1px rgba(255,255,255,0.5);
      animation: dock-float 4s ease-in-out infinite;
    }

    .dock-btn {
      position: relative;
      padding: 0.75rem;
      border-radius: 0.75rem;
      color: #6b7280;
      text-decoration: none;
      transition: color 200ms, transform 200ms;
      display: inline-flex;
      align-items: center;
      justify-content: center;
    }

    .dock-btn:hover {
      color: #24306e;
      transform: scale(1.2) translateY(-4px);
    }

    .dock-btn.active {
      color: #FFB800;
    }

    .dock-tooltip {
      position: absolute;
      top: -2rem;
      left: 50%;
      transform: translateX(-50%);
      padding: 0.25rem 0.5rem;
      border-radius: 0.5rem;
      font-size: 0.75rem;
      background: #24306e;
      color: white;
      white-space: nowrap;
      opacity: 0;
      pointer-events: none;
      transition: opacity 200ms;
      box-shadow: 0 2px 8px rgba(0,0,0,0.15);
    }

    .dock-btn:hover .dock-tooltip {
      opacity: 1;
    }

    .dock-dot {
      position: absolute;
      bottom: -0.25rem;
      left: 50%;
      transform: translateX(-50%);
      width: 0.375rem;
      height: 0.375rem;
      background: #FFB800;
      border-radius: 9999px;
      opacity: 0;
    }

    .dock-btn.active .dock-dot {
      opacity: 1;
    }

    @keyframes dock-float {
      0%, 100% { transform: translateY(0); }
      50% { transform: translateY(-2px); }
    }
  `]
})
export class DockNav {}
