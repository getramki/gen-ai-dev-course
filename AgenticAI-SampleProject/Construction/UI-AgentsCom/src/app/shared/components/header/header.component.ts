import { Component } from '@angular/core';
import { RouterModule } from '@angular/router';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';

@Component({
  selector: 'app-header',
  standalone: true,
  imports: [RouterModule, MatToolbarModule, MatButtonModule, MatIconModule],
  template: `
    <mat-toolbar color="primary">
      <span>Agent Communication Dashboard</span>
      <span class="spacer"></span>
      <button mat-button routerLink="/communication" routerLinkActive="active">
        <mat-icon>dashboard</mat-icon>
        Dashboard
      </button>
      <button mat-button routerLink="/settings" routerLinkActive="active">
        <mat-icon>settings</mat-icon>
        Settings
      </button>
    </mat-toolbar>
  `,
  styles: [`
    .spacer {
      flex: 1;
    }
    button.active {
      background: rgba(255, 255, 255, 0.1);
    }
  `]
})
export class HeaderComponent {}
