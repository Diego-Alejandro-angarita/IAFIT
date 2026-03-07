import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { DockNav } from './components/dock-nav/dock-nav.component';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet, DockNav],
  templateUrl: './app.html',
  styleUrl: './app.scss'
})
export class App {}
