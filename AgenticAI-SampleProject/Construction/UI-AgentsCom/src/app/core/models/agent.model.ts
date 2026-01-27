export type AgentType = 'purchase' | 'cement' | 'steel';
export type AgentStatus = 'online' | 'offline' | 'error';

export interface Agent {
  id: string;
  name: string;
  type: AgentType;
  url: string;
  port: number;
  status: AgentStatus;
  lastSeen?: Date;
}
