import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, Subject, interval, Subscription } from 'rxjs';
import { switchMap, catchError, tap } from 'rxjs/operators';
import { ConversationMessage } from '../models/conversation.model';

@Injectable({
  providedIn: 'root'
})
export class PollingService {
  private messages$ = new Subject<ConversationMessage>();
  private pollingSubscription?: Subscription;
  private lastMessageTimestamp?: string;

  constructor(private http: HttpClient) {}

  startPolling(agentUrl: string, intervalMs: number = 2000): void {
    this.stopPolling();

    this.pollingSubscription = interval(intervalMs).pipe(
      switchMap(() => this.fetchMessages(agentUrl)),
      catchError((error) => {
        console.error('Polling error:', error);
        return [];
      })
    ).subscribe((messages: ConversationMessage[]) => {
      messages.forEach(msg => {
        if (!this.lastMessageTimestamp || msg.timestamp > this.lastMessageTimestamp) {
          this.messages$.next(msg);
          this.lastMessageTimestamp = msg.timestamp;
        }
      });
    });
  }

  stopPolling(): void {
    this.pollingSubscription?.unsubscribe();
    this.pollingSubscription = undefined;
  }

  onMessage(): Observable<ConversationMessage> {
    return this.messages$.asObservable();
  }

  private fetchMessages(agentUrl: string): Observable<ConversationMessage[]> {
    return this.http.get<ConversationMessage[]>(`${agentUrl}/messages`);
  }

  loadFromUrl(url: string): Observable<ConversationMessage[]> {
    return this.http.get<ConversationMessage[]>(url);
  }
}
