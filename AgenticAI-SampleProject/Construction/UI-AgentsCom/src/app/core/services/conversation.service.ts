import { Injectable, signal } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, Subject } from 'rxjs';
import { ConversationMessage } from '../models/conversation.model';
import { NegotiationState, Quote } from '../models/negotiation.model';

@Injectable({
  providedIn: 'root'
})
export class ConversationService {
  private messages = signal<ConversationMessage[]>([]);
  private liveMessages$ = new Subject<ConversationMessage>();

  constructor(private http: HttpClient) {}

  getMessages() {
    return this.messages.asReadonly();
  }

  addMessage(message: ConversationMessage): void {
    this.messages.set([...this.messages(), message]);
    this.liveMessages$.next(message);
  }

  clearMessages(): void {
    this.messages.set([]);
  }

  loadFromFile(filePath: string): Observable<ConversationMessage[]> {
    return this.http.get<ConversationMessage[]>(filePath);
  }

  subscribeToLive(): Observable<ConversationMessage> {
    return this.liveMessages$.asObservable();
  }

  parseNegotiationData(messages: ConversationMessage[]): NegotiationState {
    const cementQuotes: Quote[] = [];
    const steelQuotes: Quote[] = [];
    let currentCycle = 0;
    let projectName = 'Construction Project';
    let totalBudget = 0;
    let cementBudget = 0;
    let steelBudget = 0;

    messages.forEach(msg => {
      if (msg.type === 'REQUEST' && msg.content.includes('CYCLE')) {
        const cycleMatch = msg.content.match(/CYCLE (\d+)/);
        if (cycleMatch) currentCycle = parseInt(cycleMatch[1]);
      }

      if (msg.content.includes('budget')) {
        const budgetMatch = msg.content.match(/\$(\d+)K/g);
        if (budgetMatch) {
          const amounts = budgetMatch.map(b => parseInt(b.replace(/\$|K/g, '')));
          if (amounts.length >= 2) {
            cementBudget = amounts[0];
            steelBudget = amounts[1];
            totalBudget = cementBudget + steelBudget;
          }
        }
      }

      if (msg.type === 'RESPONSE' && msg.content.includes('quote')) {
        const priceMatch = msg.content.match(/\$(\d+)K/);
        if (priceMatch) {
          const quote: Quote = {
            agent: msg.from_agent,
            price: parseInt(priceMatch[1]),
            cycle: currentCycle,
            timestamp: msg.timestamp
          };
          
          if (msg.from_agent.toLowerCase().includes('cement')) {
            cementQuotes.push(quote);
          } else if (msg.from_agent.toLowerCase().includes('steel')) {
            steelQuotes.push(quote);
          }
        }
      }
    });

    return {
      projectName,
      totalBudget,
      cementBudget,
      steelBudget,
      currentCycle,
      maxCycles: 4,
      cementQuotes,
      steelQuotes,
      status: currentCycle >= 4 ? 'completed' : 'negotiating'
    };
  }
}
