import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatCardModule } from '@angular/material/card';
import { MatChipsModule } from '@angular/material/chips';
import { Agent } from '../../../../core/models/agent.model';

@Component({
  selector: 'app-agent-card',
  standalone: true,
  imports: [CommonModule, MatCardModule, MatChipsModule],
  template: `
    <mat-card [class]="'agent-card agent-' + agent.type">
      <mat-card-header>
        <mat-card-title>{{ agent.name }}</mat-card-title>
        <mat-chip [class]="'status-' + agent.status">{{ agent.status }}</mat-chip>
      </mat-card-header>
      <mat-card-content>
        <div class="stat">
          <span class="label">Type:</span>
          <span class="value">{{ agent.type }}</span>
        </div>
        <div class="stat">
          <span class="label">Endpoint:</span>
          <span class="value">{{ agent.url }}:{{ agent.port }}</span>
        </div>
        <div class="stat">
          <span class="label">Messages:</span>
          <span class="value">{{ messageCount }}</span>
        </div>
      </mat-card-content>
    </mat-card>
  `,
  styles: [`
    .agent-card {
      height: 100%;
      
      &.agent-purchase {
        border-left: 4px solid #2196F3;
      }
      &.agent-cement {
        border-left: 4px solid #FF9800;
      }
      &.agent-steel {
        border-left: 4px solid #607D8B;
      }
    }

    mat-card-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 16px;
    }

    mat-card-title {
      font-size: 18px;
      margin: 0;
    }

    mat-chip {
      font-size: 11px;
      min-height: 20px;
      padding: 0 8px;
      
      &.status-online {
        background: #4caf50;
        color: white;
      }
      &.status-offline {
        background: #9e9e9e;
        color: white;
      }
      &.status-error {
        background: #f44336;
        color: white;
      }
    }

    .stat {
      display: flex;
      justify-content: space-between;
      margin: 8px 0;
      font-size: 14px;
      
      .label {
        color: #666;
      }
      .value {
        font-weight: 500;
      }
    }
  `]
})
export class AgentCardComponent {
  @Input() agent!: Agent;
  @Input() messageCount = 0;
}
