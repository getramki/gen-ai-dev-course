import { Component, Input, ElementRef, ViewChild, AfterViewChecked, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { ConversationMessage } from '../../../../core/models/conversation.model';
import { MessageItemComponent } from '../message-item/message-item.component';

@Component({
  selector: 'app-conversation-flow',
  standalone: true,
  imports: [CommonModule, MatButtonModule, MatIconModule, MessageItemComponent],
  template: `
    <div class="conversation-container">
      <div class="conversation-header">
        <h3>Conversation Flow</h3>
        <div class="controls">
          <button mat-icon-button (click)="toggleAutoScroll()">
            <mat-icon>{{ autoScroll() ? 'pause' : 'play_arrow' }}</mat-icon>
          </button>
          <button mat-icon-button (click)="clearMessages()">
            <mat-icon>clear_all</mat-icon>
          </button>
        </div>
      </div>
      <div class="messages-container" #messagesContainer>
        @if (messages.length === 0) {
          <div class="empty-state">
            <mat-icon>chat_bubble_outline</mat-icon>
            <p>No messages yet. Load a conversation or connect to live agents.</p>
          </div>
        } @else {
          @for (message of messages; track message.timestamp) {
            <app-message-item [message]="message" />
          }
        }
      </div>
    </div>
  `,
  styles: [`
    :host {
      display: flex;
      flex: 1;
      min-height: 0;
    }
    
    .conversation-container {
      width: 100%;
      display: flex;
      flex-direction: column;
      background: #fafafa;
      border-radius: 8px;
      overflow: hidden;
    }

    .conversation-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 16px;
      background: white;
      border-bottom: 1px solid #e0e0e0;

      h3 {
        margin: 0;
        font-size: 18px;
      }

      .controls {
        display: flex;
        gap: 8px;
      }
    }

    .messages-container {
      flex: 1;
      overflow-y: auto;
      overflow-x: hidden;
      padding: 16px;
      min-height: 0;
    }

    .empty-state {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      height: 100%;
      color: #999;

      mat-icon {
        font-size: 64px;
        width: 64px;
        height: 64px;
        margin-bottom: 16px;
      }

      p {
        font-size: 14px;
      }
    }
  `]
})
export class ConversationFlowComponent implements AfterViewChecked {
  @Input() messages: ConversationMessage[] = [];
  @ViewChild('messagesContainer') messagesContainer!: ElementRef;
  
  autoScroll = signal(true);
  private shouldScroll = false;

  ngAfterViewChecked(): void {
    if (this.autoScroll() && this.shouldScroll) {
      this.scrollToBottom();
      this.shouldScroll = false;
    }
  }

  ngOnChanges(): void {
    if (this.autoScroll()) {
      this.shouldScroll = true;
    }
  }

  toggleAutoScroll(): void {
    this.autoScroll.set(!this.autoScroll());
  }

  clearMessages(): void {
    if (confirm('Clear all messages?')) {
      this.messages = [];
    }
  }

  private scrollToBottom(): void {
    if (this.messagesContainer) {
      const element = this.messagesContainer.nativeElement;
      element.scrollTop = element.scrollHeight;
    }
  }
}
