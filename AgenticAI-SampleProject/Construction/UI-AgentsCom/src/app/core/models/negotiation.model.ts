export type NegotiationStatus = 'pending' | 'negotiating' | 'completed' | 'failed';

export interface Quote {
  agent: string;
  price: number;
  cycle: number;
  timestamp: string;
}

export interface NegotiationState {
  projectName: string;
  totalBudget: number;
  cementBudget: number;
  steelBudget: number;
  currentCycle: number;
  maxCycles: number;
  cementQuotes: Quote[];
  steelQuotes: Quote[];
  status: NegotiationStatus;
}
