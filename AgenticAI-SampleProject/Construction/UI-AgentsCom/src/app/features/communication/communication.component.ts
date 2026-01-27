import { Component, OnInit, signal, computed } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { HttpClient } from '@angular/common/http';
import { HeaderComponent } from '../../shared/components/header/header.component';
import { AgentCardComponent } from './components/agent-card/agent-card.component';
import { ConversationFlowComponent } from './components/conversation-flow/conversation-flow.component';
import { MessageTimelineComponent } from './components/message-timeline/message-timeline.component';
import { NegotiationStatsComponent } from './components/negotiation-stats/negotiation-stats.component';
import { AgentConfigService } from '../../core/services/agent-config.service';
import { ConversationService } from '../../core/services/conversation.service';
import { PollingService } from '../../core/services/websocket.service';
import { NotificationService } from '../../core/services/notification.service';
import { ConversationMessage } from '../../core/models/conversation.model';
import { environment } from '../../../environments/environment';

@Component({
  selector: 'app-communication',
  standalone: true,
  imports: [
    CommonModule,
    MatButtonModule,
    MatIconModule,
    MatProgressSpinnerModule,
    HeaderComponent,
    AgentCardComponent,
    ConversationFlowComponent,
    MessageTimelineComponent,
    NegotiationStatsComponent
  ],
  templateUrl: './communication.component.html',
  styleUrl: './communication.component.scss'
})
export class CommunicationComponent implements OnInit {
  agents!: ReturnType<AgentConfigService['getAgentsSignal']>;
  messages!: ReturnType<ConversationService['getMessages']>;
  pollingActive = signal(false);
  loading = signal(false);

  purchaseAgent!: ReturnType<typeof computed<any>>;
  cementAgent!: ReturnType<typeof computed<any>>;
  steelAgent!: ReturnType<typeof computed<any>>;

  constructor(
    private agentService: AgentConfigService,
    private conversationService: ConversationService,
    private pollingService: PollingService,
    private notification: NotificationService,
    private http: HttpClient
  ) {}

  ngOnInit(): void {
    this.agents = this.agentService.getAgentsSignal();
    this.messages = this.conversationService.getMessages();
    
    this.purchaseAgent = computed(() => this.agents().find(a => a.type === 'purchase'));
    this.cementAgent = computed(() => this.agents().find(a => a.type === 'cement'));
    this.steelAgent = computed(() => this.agents().find(a => a.type === 'steel'));

    this.pollingService.onMessage().subscribe(msg => {
      this.conversationService.addMessage(msg);
    });
  }

  loadSampleData(): void {
    this.loading.set(true);
    const baseTime = new Date();
    const sampleMessages: ConversationMessage[] = [
      {
        timestamp: new Date(baseTime.getTime()).toISOString(),
        from_agent: 'Purchase Agent',
        to_agent: 'Cement Agent',
        type: 'CONNECTED',
        content: 'Connection established with Cement Sales Agent',
        llm_reasoning: null
      },
      {
        timestamp: new Date(baseTime.getTime() + 1000).toISOString(),
        from_agent: 'Purchase Agent',
        to_agent: 'Steel Agent',
        type: 'CONNECTED',
        content: 'Connection established with Steel Sales Agent',
        llm_reasoning: null
      },
      {
        timestamp: new Date(baseTime.getTime() + 2000).toISOString(),
        from_agent: 'Purchase Agent',
        to_agent: 'Cement Agent',
        type: 'REQUEST',
        content: 'CYCLE 1: Requesting cement quote. Budget: $55K',
        llm_reasoning: 'Starting negotiation cycle 1 with cement supplier'
      },
      {
        timestamp: new Date(baseTime.getTime() + 3000).toISOString(),
        from_agent: 'Cement Agent',
        to_agent: 'Purchase Agent',
        type: 'RESPONSE',
        content: 'Quote: $60K for premium cement',
        llm_reasoning: 'Initial quote above budget'
      },
      {
        timestamp: new Date(baseTime.getTime() + 4000).toISOString(),
        from_agent: 'Purchase Agent',
        to_agent: 'Steel Agent',
        type: 'REQUEST',
        content: 'CYCLE 1: Requesting steel quote. Budget: $75K',
        llm_reasoning: 'Starting negotiation cycle 1 with steel supplier'
      },
      {
        timestamp: new Date(baseTime.getTime() + 5000).toISOString(),
        from_agent: 'Steel Agent',
        to_agent: 'Purchase Agent',
        type: 'RESPONSE',
        content: 'Quote: $80K for steel beams',
        llm_reasoning: 'Initial quote above budget'
      },
      {
        timestamp: new Date(baseTime.getTime() + 6000).toISOString(),
        from_agent: 'Purchase Agent',
        to_agent: 'Cement Agent',
        type: 'REQUEST',
        content: 'CYCLE 2: Counter-offer needed. Budget: $55K',
        llm_reasoning: 'Negotiating better price in cycle 2'
      },
      {
        timestamp: new Date(baseTime.getTime() + 7000).toISOString(),
        from_agent: 'Cement Agent',
        to_agent: 'Purchase Agent',
        type: 'RESPONSE',
        content: 'Revised quote: $57K',
        llm_reasoning: 'Reduced price but still above budget'
      },
      {
        timestamp: new Date(baseTime.getTime() + 8000).toISOString(),
        from_agent: 'Purchase Agent',
        to_agent: 'Purchase Agent',
        type: 'ANALYSIS',
        content: 'Analyzing quotes: Cement $57K vs budget $55K, Steel $80K vs budget $75K',
        llm_reasoning: 'Evaluating negotiation progress and determining next steps'
      }
    ];

    sampleMessages.forEach(msg => this.conversationService.addMessage(msg));
    this.loading.set(false);
    this.notification.success('Sample data loaded successfully');
  }

  startPolling(): void {
    const purchaseAgent = this.purchaseAgent();
    if (purchaseAgent) {
      const url = `${purchaseAgent.url}:${purchaseAgent.port}`;
      this.pollingService.startPolling(url, 3000);
      this.pollingActive.set(true);
      this.notification.info('Polling started - checking for new messages every 3 seconds');
    } else {
      this.notification.error('Purchase agent not configured');
    }
  }

  stopPolling(): void {
    this.pollingService.stopPolling();
    this.pollingActive.set(false);
    this.notification.info('Polling stopped');
  }

  loadFromFile(): void {
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = '.json';
    input.onchange = (e: any) => {
      const file = e.target.files[0];
      if (!file) return;
      
      this.loading.set(true);
      const reader = new FileReader();
      reader.onload = (event: any) => {
        try {
          const messages = JSON.parse(event.target.result);
          if (!Array.isArray(messages)) {
            throw new Error('Invalid format: expected array of messages');
          }
          this.conversationService.clearMessages();
          messages.forEach((msg: ConversationMessage) => 
            this.conversationService.addMessage(msg)
          );
          this.loading.set(false);
          this.notification.success(`Loaded ${messages.length} messages from file`);
        } catch (error) {
          this.loading.set(false);
          this.notification.error('Error parsing JSON file: ' + (error as Error).message);
        }
      };
      reader.onerror = () => {
        this.loading.set(false);
        this.notification.error('Error reading file');
      };
      reader.readAsText(file);
    };
    input.click();
  }

  getMessageCount(agentName: string): number {
    return this.messages().filter(m => 
      m.from_agent === agentName || m.to_agent === agentName
    ).length;
  }
}
