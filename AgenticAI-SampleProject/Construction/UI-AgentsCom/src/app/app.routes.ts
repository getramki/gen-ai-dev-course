import { Routes } from '@angular/router';

export const routes: Routes = [
  {
    path: '',
    redirectTo: 'communication',
    pathMatch: 'full'
  },
  {
    path: 'communication',
    loadComponent: () => import('./features/communication/communication.component').then(m => m.CommunicationComponent)
  },
  {
    path: 'settings',
    loadComponent: () => import('./features/settings/settings.component').then(m => m.SettingsComponent)
  }
];
