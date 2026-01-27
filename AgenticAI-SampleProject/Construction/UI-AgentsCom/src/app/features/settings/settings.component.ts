import { Component, OnInit, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { RouterModule } from '@angular/router';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatCardModule } from '@angular/material/card';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatSelectModule } from '@angular/material/select';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatChipsModule } from '@angular/material/chips';
import { Agent, AgentType } from '../../core/models/agent.model';
import { AgentConfigService } from '../../core/services/agent-config.service';
import { NotificationService } from '../../core/services/notification.service';

@Component({
  selector: 'app-settings',
  standalone: true,
  imports: [
    CommonModule,
    ReactiveFormsModule,
    RouterModule,
    MatToolbarModule,
    MatCardModule,
    MatFormFieldModule,
    MatInputModule,
    MatSelectModule,
    MatButtonModule,
    MatIconModule,
    MatChipsModule
  ],
  templateUrl: './settings.component.html',
  styleUrl: './settings.component.scss'
})
export class SettingsComponent implements OnInit {
  agentForm: FormGroup;
  agents!: ReturnType<AgentConfigService['getAgentsSignal']>;
  editingAgent: Agent | null = null;
  testing = signal<string | null>(null);

  constructor(
    private fb: FormBuilder,
    private agentService: AgentConfigService,
    private notification: NotificationService
  ) {
    this.agentForm = this.fb.group({
      name: ['', Validators.required],
      type: ['purchase' as AgentType, Validators.required],
      url: ['http://localhost', Validators.required],
      port: [10001, [Validators.required, Validators.min(1), Validators.max(65535)]],
      status: ['offline']
    });
  }

  ngOnInit(): void {
    this.agents = this.agentService.getAgentsSignal();
  }

  saveAgent(): void {
    if (this.agentForm.valid) {
      const agent: Agent = {
        id: this.editingAgent?.id || Date.now().toString(),
        ...this.agentForm.value
      };
      
      this.agentService.saveAgent(agent);
      this.notification.success(this.editingAgent ? 'Agent updated successfully' : 'Agent added successfully');
      this.resetForm();
    }
  }

  editAgent(agent: Agent): void {
    this.editingAgent = agent;
    this.agentForm.patchValue(agent);
  }

  deleteAgent(id: string): void {
    if (confirm('Are you sure you want to delete this agent?')) {
      this.agentService.deleteAgent(id);
      this.notification.success('Agent deleted successfully');
    }
  }

  testConnection(agent: Agent): void {
    this.testing.set(agent.id);
    this.agentService.testConnection(agent).subscribe({
      next: (success) => {
        agent.status = success ? 'online' : 'offline';
        this.agentService.saveAgent(agent);
        this.testing.set(null);
        this.notification.success(success ? 'Agent is online' : 'Agent is offline');
      },
      error: () => {
        agent.status = 'error';
        this.agentService.saveAgent(agent);
        this.testing.set(null);
        this.notification.error('Connection test failed');
      }
    });
  }

  cancelEdit(): void {
    this.resetForm();
  }

  private resetForm(): void {
    this.editingAgent = null;
    this.agentForm.reset({
      name: '',
      type: 'purchase',
      url: 'http://localhost',
      port: 10001,
      status: 'offline'
    });
  }
}
