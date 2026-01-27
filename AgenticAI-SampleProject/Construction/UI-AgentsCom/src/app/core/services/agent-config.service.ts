import { Injectable, signal } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, of, catchError, map } from 'rxjs';
import { Agent } from '../models/agent.model';

@Injectable({
  providedIn: 'root'
})
export class AgentConfigService {
  private readonly STORAGE_KEY = 'agent_configs';
  private readonly VERSION_KEY = 'agent_configs_version';
  private readonly CURRENT_VERSION = '2';
  private agents = signal<Agent[]>([]);

  constructor(private http: HttpClient) {
    this.loadFromStorage();
  }

  getAgents(): Agent[] {
    return this.agents();
  }

  getAgentsSignal() {
    return this.agents.asReadonly();
  }

  saveAgent(agent: Agent): void {
    const current = this.agents();
    const index = current.findIndex(a => a.id === agent.id);
    
    if (index >= 0) {
      current[index] = agent;
      this.agents.set([...current]);
    } else {
      this.agents.set([...current, agent]);
    }
    
    this.saveToStorage();
  }

  deleteAgent(id: string): void {
    this.agents.set(this.agents().filter(a => a.id !== id));
    this.saveToStorage();
  }

  testConnection(agent: Agent): Observable<boolean> {
    const url = `${agent.url}:${agent.port}/health`;
    return this.http.get(url, { observe: 'response' }).pipe(
      map(() => true),
      catchError(() => of(false))
    );
  }

  private loadFromStorage(): void {
    const version = localStorage.getItem(this.VERSION_KEY);
    const stored = localStorage.getItem(this.STORAGE_KEY);
    
    if (version !== this.CURRENT_VERSION || !stored) {
      // Version mismatch or no data - reset to defaults
      this.setDefaultAgents();
      localStorage.setItem(this.VERSION_KEY, this.CURRENT_VERSION);
    } else {
      this.agents.set(JSON.parse(stored));
    }
  }

  private saveToStorage(): void {
    localStorage.setItem(this.STORAGE_KEY, JSON.stringify(this.agents()));
  }

  private setDefaultAgents(): void {
    const defaults: Agent[] = [
      { id: '1', name: 'Purchase Agent', type: 'purchase', url: 'http://localhost', port: 10001, status: 'offline' },
      { id: '2', name: 'Cement Agent', type: 'cement', url: 'http://localhost', port: 10002, status: 'offline' },
      { id: '3', name: 'Steel Agent', type: 'steel', url: 'http://localhost', port: 10003, status: 'offline' }
    ];
    this.agents.set(defaults);
    this.saveToStorage();
  }
}
