import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { ConversationMessage } from '../../../../core/models/conversation.model';

@Component({
  selector: 'app-message-item',
  standalone: true,
  imports: [CommonModule, MatCardModule, MatButtonModule, MatIconModule],
  template: `
    <div [class]="'message-item message-' + message.type.toLowerCase()">
      <div class="message-header">
        <span class="from">{{ message.from_agent }}</span>
        <mat-icon class="arrow">arrow_forward</mat-icon>
        <span class="to">{{ message.to_agent }}</span>
        <span class="type-badge">{{ message.type }}</span>
        <span class="timestamp">{{ formatTime(message.timestamp) }}</span>
      </div>
      <div class="message-content">{{ message.content }}</div>
      @if (message.llm_reasoning) {
        <button mat-button class="reasoning-toggle" (click)="showReasoning = !showReasoning">
          <mat-icon>{{ showReasoning ? 'expand_less' : 'expand_more' }}</mat-icon>
          LLM Reasoning
        </button>
        @if (showReasoning) {
          <div class="reasoning-content">{{ message.llm_reasoning }}</div>
        }
      }
    </div>
  `,
  styles: [`
    .message-item {
      margin: 12px 0;
      padding: 12px;
      border-radius: 8px;
      border-left: 4px solid;
      background: white;
      box-shadow: 0 1px 3px rgba(0,0,0,0.1);

      &.message-connected {
        border-color: #4CAF50;
        background: #f1f8f4;
      }
      &.message-request {
        border-color: #2196F3;
        background: #f0f7ff;
      }
      &.message-response {
        border-color: #FF9800;
        background: #fff8f0;
      }
      &.message-analysis {
        border-color: #9C27B0;
        background: #f8f0ff;
      }
    }

    .message-header {
      display: flex;
      align-items: center;
      gap: 8px;
      margin-bottom: 8px;
      font-size: 13px;

      .from, .to {
        font-weight: 500;
      }
      
      .arrow {
        font-size: 16px;
        width: 16px;
        height: 16px;
        color: #999;
      }

      .type-badge {
        background: rgba(0,0,0,0.1);
        padding: 2px 8px;
        border-radius: 12px;
        font-size: 11px;
        font-weight: 500;
      }

      .timestamp {
        margin-left: auto;
        color: #999;
        font-size: 12px;
      }
    }

    .message-content {
      font-size: 14px;
      line-height: 1.5;
      color: #333;
    }

    .reasoning-toggle {
      margin-top: 8px;
      font-size: 12px;
    }

    .reasoning-content {
      margin-top: 8px;
      padding: 12px;
      background: rgba(0,0,0,0.05);
      border-radius: 4px;
      font-size: 13px;
      color: #555;
      white-space: pre-wrap;
    }
  `]
})
export class MessageItemComponent {
  @Input() message!: ConversationMessage;
  showReasoning = false;

  formatTime(timestamp: string): string {
    const date = new Date(timestamp);
    return date.toLocaleTimeString();
  }
}
