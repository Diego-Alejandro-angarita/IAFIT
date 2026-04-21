import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { HttpClientModule } from '@angular/common/http';
import { DockNav } from './components/dock-nav/dock-nav.component';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet, DockNav, HttpClientModule],
  templateUrl: './app.html',
  styleUrl: './app.scss'
})
export class App {}
