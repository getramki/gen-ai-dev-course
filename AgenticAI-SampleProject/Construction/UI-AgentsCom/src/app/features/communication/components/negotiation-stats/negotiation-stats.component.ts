import { Component, Input, OnChanges, computed, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatCardModule } from '@angular/material/card';
import { MatChipsModule } from '@angular/material/chips';
import { ConversationMessage } from '../../../../core/models/conversation.model';
import { NegotiationState } from '../../../../core/models/negotiation.model';
import { ConversationService } from '../../../../core/services/conversation.service';

@Component({
  selector: 'app-negotiation-stats',
  standalone: true,
  imports: [CommonModule, MatCardModule, MatChipsModule],
  template: `
    <mat-card class="stats-card">
      <mat-card-header>
        <mat-card-title>Negotiation Statistics</mat-card-title>
      </mat-card-header>
      <mat-card-content>
        <div class="stats-grid">
          <div class="stat-item">
            <span class="stat-label">Total Messages</span>
            <span class="stat-value">{{ messages.length }}</span>
          </div>
          <div class="stat-item">
            <span class="stat-label">Current Cycle</span>
            <span class="stat-value">{{ negotiationState()?.currentCycle || 0 }} / {{ negotiationState()?.maxCycles || 4 }}</span>
          </div>
          <div class="stat-item">
            <span class="stat-label">Total Budget</span>
            <span class="stat-value">\${{ negotiationState()?.totalBudget || 0 }}K</span>
          </div>
          <div class="stat-item">
            <span class="stat-label">Status</span>
            <mat-chip [class]="'status-' + (negotiationState()?.status || 'pending')">
              {{ negotiationState()?.status || 'pending' }}
            </mat-chip>
          </div>
        </div>

        @if (negotiationState()) {
          <div class="budget-breakdown">
            <h4>Budget Breakdown</h4>
            <div class="budget-item">
              <span>Cement Budget:</span>
              <span class="budget-value">\${{ negotiationState()!.cementBudget }}K</span>
              @if (negotiationState()!.cementQuotes.length > 0) {
                <span class="quote-value">
                  Latest Quote: \${{ negotiationState()!.cementQuotes[negotiationState()!.cementQuotes.length - 1].price }}K
                </span>
              }
            </div>
            <div class="budget-item">
              <span>Steel Budget:</span>
              <span class="budget-value">\${{ negotiationState()!.steelBudget }}K</span>
              @if (negotiationState()!.steelQuotes.length > 0) {
                <span class="quote-value">
                  Latest Quote: \${{ negotiationState()!.steelQuotes[negotiationState()!.steelQuotes.length - 1].price }}K
                </span>
              }
            </div>
          </div>
        }
      </mat-card-content>
    </mat-card>
  `,
  styles: [`
    .stats-card {
      height: 100%;
      overflow: hidden;
      max-width: 100%;
    }
    
    mat-card-content {
      overflow: hidden;
    }

    .stats-grid {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 12px;
      margin-bottom: 20px;
    }

    .stat-item {
      display: flex;
      flex-direction: column;
      gap: 8px;
      padding: 12px;
      background: #f5f5f5;
      border-radius: 8px;
      min-height: 80px;

      .stat-label {
        font-size: 12px;
        color: #666;
        text-transform: uppercase;
        white-space: nowrap;
      }

      .stat-value {
        font-size: 20px;
        font-weight: 600;
        color: #333;
      }
    }

    mat-chip {
      font-size: 10px;
      min-height: 20px;
      height: 20px;
      padding: 2px 6px;
      line-height: 16px;
      
      &.status-pending {
        background: #9e9e9e;
        color: white;
      }
      &.status-negotiating {
        background: #2196F3;
        color: white;
      }
      &.status-completed {
        background: #4caf50;
        color: white;
      }
      &.status-failed {
        background: #f44336;
        color: white;
      }
    }

    .budget-breakdown {
      h4 {
        margin: 0 0 12px 0;
        font-size: 14px;
        color: #666;
      }
    }

    .budget-item {
      display: flex;
      align-items: center;
      gap: 8px;
      padding: 8px 0;
      border-bottom: 1px solid #e0e0e0;
      font-size: 13px;
      overflow: hidden;

      &:last-child {
        border-bottom: none;
      }
      
      span {
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
      }

      .budget-value {
        font-weight: 600;
        color: #2196F3;
        flex-shrink: 0;
      }

      .quote-value {
        margin-left: auto;
        color: #FF9800;
        font-weight: 500;
        flex-shrink: 0;
      }
    }

    @media (max-width: 768px) {
      .stats-grid {
        grid-template-columns: 1fr;
      }
    }
  `]
})
export class NegotiationStatsComponent implements OnChanges {
  @Input() messages: ConversationMessage[] = [];
  negotiationState = signal<NegotiationState | null>(null);

  constructor(private conversationService: ConversationService) {}

  ngOnChanges(): void {
    if (this.messages.length > 0) {
      const state = this.conversationService.parseNegotiationData(this.messages);
      this.negotiationState.set(state);
    }
  }
}
