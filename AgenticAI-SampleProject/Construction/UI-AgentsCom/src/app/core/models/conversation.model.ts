export type MessageType = 'CONNECTED' | 'REQUEST' | 'RESPONSE' | 'ANALYSIS';

export interface ConversationMessage {
  timestamp: string;
  from_agent: string;
  to_agent: string;
  type: MessageType;
  content: string;
  llm_reasoning?: string | null;
}
