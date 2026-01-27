# Angular UI for Agent Communication Visualization

## Project Overview
Real-time visualization dashboard for A2A (Agent-to-Agent) communication between Construction Purchase Agent, Cement Sales Agent, and Steel Sales Agent. Built with Angular 19 standalone components.

## Technology Stack
- **Framework**: Angular 19 (Standalone Components)
- **UI Library**: Angular Material 19
- **State Management**: RxJS + Signals
- **Real-time**: WebSocket / Server-Sent Events (SSE)
- **Visualization**: D3.js / ngx-charts
- **HTTP Client**: Angular HttpClient
- **Styling**: SCSS + Angular Material Theme

## Project Structure
```
UI-AgentsCom/
├── src/
│   ├── app/
│   │   ├── core/
│   │   │   ├── models/
│   │   │   │   ├── agent.model.ts
│   │   │   │   ├── conversation.model.ts
│   │   │   │   └── negotiation.model.ts
│   │   │   ├── services/
│   │   │   │   ├── agent-config.service.ts
│   │   │   │   ├── conversation.service.ts
│   │   │   │   └── websocket.service.ts
│   │   │   └── interceptors/
│   │   │       └── error.interceptor.ts
│   │   ├── features/
│   │   │   ├── settings/
│   │   │   │   ├── settings.component.ts
│   │   │   │   ├── settings.component.html
│   │   │   │   └── settings.component.scss
│   │   │   └── communication/
│   │   │       ├── communication.component.ts
│   │   │       ├── communication.component.html
│   │   │       ├── communication.component.scss
│   │   │       └── components/
│   │   │           ├── agent-card/
│   │   │           ├── conversation-flow/
│   │   │           ├── message-timeline/
│   │   │           └── negotiation-stats/
│   │   ├── shared/
│   │   │   ├── components/
│   │   │   │   ├── header/
│   │   │   │   └── loading-spinner/
│   │   │   └── pipes/
│   │   │       └── timestamp.pipe.ts
│   │   ├── app.component.ts
│   │   ├── app.config.ts
│   │   └── app.routes.ts
│   ├── assets/
│   │   └── icons/
│   ├── styles/
│   │   ├── _variables.scss
│   │   ├── _mixins.scss
│   │   └── styles.scss
│   └── environments/
│       ├── environment.ts
│       └── environment.prod.ts
├── angular.json
├── package.json
├── tsconfig.json
└── README.md
```

## Core Features

### 1. Settings Page
**Route**: `/settings`

#### Features:
- **Agent Configuration**
  - Add/Edit/Delete agent endpoints
  - Agent types: Purchase, Cement, Steel
  - Fields: Name, Type, URL, Port, Status
  - Test connection button
  - Save to localStorage

- **Connection Settings**
  - WebSocket/SSE endpoint configuration
  - Polling interval (for fallback)
  - Auto-reconnect settings

- **Display Preferences**
  - Theme selection (Light/Dark)
  - Animation speed
  - Message grouping options

#### Components:
- `SettingsComponent` (main container)
- `AgentConfigFormComponent` (agent CRUD)
- `ConnectionSettingsComponent`
- `PreferencesComponent`

### 2. Communication Dashboard
**Route**: `/communication` (default)

#### Layout:
```
┌─────────────────────────────────────────────────────┐
│  Header (Agent Status Indicators)                   │
├──────────────┬──────────────────────┬───────────────┤
│              │                      │               │
│  Purchase    │  Conversation Flow   │  Cement       │
│  Agent Card  │  (Center Panel)      │  Agent Card   │
│              │                      │               │
│              ├──────────────────────┤               │
│              │                      │  Steel        │
│              │  Timeline View       │  Agent Card   │
│              │                      │               │
├──────────────┴──────────────────────┴───────────────┤
│  Negotiation Statistics & Metrics                   │
└─────────────────────────────────────────────────────┘
```

#### Features:

**A. Agent Cards (Left/Right Panels)**
- Agent name, type, status (online/offline)
- Current negotiation cycle
- Last activity timestamp
- Quick stats (messages sent/received)

**B. Conversation Flow (Center Panel)**
- Real-time message stream
- Message types: CONNECTED, REQUEST, RESPONSE, ANALYSIS
- Color-coded by agent
- Expandable message details
- LLM reasoning display (collapsible)
- Auto-scroll with pause option

**C. Timeline View**
- Horizontal timeline of events
- Negotiation cycles marked
- Key milestones highlighted
- Zoom/pan controls

**D. Statistics Panel (Bottom)**
- Total messages count
- Negotiation cycles completed
- Budget vs. Quoted prices
- Response time metrics
- Success/failure indicators

#### Components:
- `CommunicationComponent` (main container)
- `AgentCardComponent` (reusable)
- `ConversationFlowComponent`
- `MessageItemComponent`
- `TimelineComponent`
- `NegotiationStatsComponent`

## Data Models

### Agent Model
```typescript
interface Agent {
  id: string;
  name: string;
  type: 'purchase' | 'cement' | 'steel';
  url: string;
  port: number;
  status: 'online' | 'offline' | 'error';
  lastSeen?: Date;
}
```

### Conversation Message Model
```typescript
interface ConversationMessage {
  timestamp: string;
  from_agent: string;
  to_agent: string;
  type: 'CONNECTED' | 'REQUEST' | 'RESPONSE' | 'ANALYSIS';
  content: string;
  llm_reasoning?: string | null;
}
```

### Negotiation State Model
```typescript
interface NegotiationState {
  projectName: string;
  totalBudget: number;
  cementBudget: number;
  steelBudget: number;
  currentCycle: number;
  maxCycles: number;
  cementQuotes: Quote[];
  steelQuotes: Quote[];
  status: 'pending' | 'negotiating' | 'completed' | 'failed';
}
```

## Services

### 1. AgentConfigService
```typescript
- getAgents(): Agent[]
- saveAgent(agent: Agent): void
- deleteAgent(id: string): void
- testConnection(agent: Agent): Observable<boolean>
```

### 2. ConversationService
```typescript
- getConversations(): Observable<ConversationMessage[]>
- loadFromFile(filePath: string): Observable<ConversationMessage[]>
- subscribeToLive(): Observable<ConversationMessage>
- parseNegotiationData(messages: ConversationMessage[]): NegotiationState
```

### 3. WebSocketService
```typescript
- connect(url: string): void
- disconnect(): void
- onMessage(): Observable<ConversationMessage>
- send(message: any): void
```

## Implementation Phases

### Phase 1: Project Setup (1 hour)
- [ ] Create Angular 19 project with standalone components
- [ ] Install dependencies (Angular Material, RxJS, etc.)
- [ ] Setup project structure
- [ ] Configure routing
- [ ] Setup Material theme
- [ ] Create environment files

### Phase 2: Core Models & Services (2 hours)
- [ ] Create data models (Agent, Conversation, Negotiation)
- [ ] Implement AgentConfigService with localStorage
- [ ] Implement ConversationService
- [ ] Create WebSocketService skeleton
- [ ] Add error handling interceptor

### Phase 3: Settings Page (3 hours)
- [ ] Create SettingsComponent layout
- [ ] Implement agent configuration form
- [ ] Add agent list with CRUD operations
- [ ] Implement connection test functionality
- [ ] Add preferences section
- [ ] Form validation
- [ ] Save/Load from localStorage

### Phase 4: Communication Dashboard - Basic (4 hours)
- [ ] Create CommunicationComponent layout
- [ ] Implement AgentCardComponent
- [ ] Create ConversationFlowComponent
- [ ] Implement MessageItemComponent
- [ ] Add message type styling
- [ ] Implement auto-scroll functionality
- [ ] Add pause/resume controls

### Phase 5: Communication Dashboard - Advanced (4 hours)
- [ ] Implement TimelineComponent with D3.js
- [ ] Create NegotiationStatsComponent
- [ ] Add real-time data parsing
- [ ] Implement negotiation cycle tracking
- [ ] Add budget vs. quote visualization
- [ ] Create expandable message details
- [ ] Add LLM reasoning display

### Phase 6: Real-time Integration (3 hours)
- [ ] Implement WebSocket connection
- [ ] Add SSE fallback
- [ ] Implement auto-reconnect logic
- [ ] Add connection status indicators
- [ ] Test with live agent endpoints
- [ ] Handle connection errors gracefully

### Phase 7: Polish & Testing (3 hours)
- [ ] Add loading states
- [ ] Implement error messages
- [ ] Add animations and transitions
- [ ] Responsive design testing
- [ ] Cross-browser testing
- [ ] Performance optimization
- [ ] Documentation

## Key Features Implementation Details

### Real-time Message Display
```typescript
// Conversation flow with auto-scroll
messages$ = this.conversationService.subscribeToLive().pipe(
  scan((acc, msg) => [...acc, msg], [] as ConversationMessage[]),
  tap(() => this.scrollToBottom())
);
```

### Negotiation Cycle Tracking
```typescript
// Parse negotiation cycles from messages
const cycles = messages
  .filter(m => m.type === 'REQUEST' && m.content.includes('CYCLE'))
  .map(m => this.extractCycleNumber(m.content));
```

### Agent Status Monitoring
```typescript
// Check agent health every 30 seconds
interval(30000).pipe(
  switchMap(() => this.testAllAgents()),
  tap(statuses => this.updateAgentStatuses(statuses))
);
```

## UI/UX Guidelines

### Color Scheme
- **Purchase Agent**: Blue (#2196F3)
- **Cement Agent**: Orange (#FF9800)
- **Steel Agent**: Grey (#607D8B)
- **System Messages**: Green (#4CAF50)
- **Errors**: Red (#F44336)

### Message Types
- **CONNECTED**: Green badge, agent icon
- **REQUEST**: Blue arrow right, expandable
- **RESPONSE**: Orange arrow left, expandable
- **ANALYSIS**: Purple info icon, collapsible

### Animations
- Fade-in for new messages (300ms)
- Slide-in for agent cards (400ms)
- Pulse for active negotiation
- Smooth scroll for timeline

## Testing Strategy

### Unit Tests
- Services (AgentConfig, Conversation, WebSocket)
- Components (isolated testing)
- Pipes and utilities

### Integration Tests
- Settings form submission
- Message flow rendering
- Real-time updates

### E2E Tests
- Complete user journey
- Settings → Communication flow
- Error handling scenarios

## Deployment

### Development
```bash
ng serve --open
```

### Production Build
```bash
ng build --configuration production
```

### Docker Deployment
```dockerfile
FROM node:20-alpine as build
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist/ui-agentscom /usr/share/nginx/html
EXPOSE 80
```

## Environment Configuration

### Development
```typescript
export const environment = {
  production: false,
  apiUrl: 'http://localhost:8000',
  wsUrl: 'ws://localhost:8000/ws',
  agents: {
    purchase: 'http://localhost:10001',
    cement: 'http://localhost:10002',
    steel: 'http://localhost:10003'
  }
};
```

### Production
```typescript
export const environment = {
  production: true,
  apiUrl: 'https://api.agents.example.com',
  wsUrl: 'wss://api.agents.example.com/ws',
  agents: {
    purchase: 'https://purchase-agent.example.com',
    cement: 'https://cement-agent.example.com',
    steel: 'https://steel-agent.example.com'
  }
};
```

## Dependencies

### Core
- @angular/core: ^19.0.0
- @angular/common: ^19.0.0
- @angular/router: ^19.0.0
- @angular/forms: ^19.0.0
- rxjs: ^7.8.0

### UI
- @angular/material: ^19.0.0
- @angular/cdk: ^19.0.0
- @angular/animations: ^19.0.0

### Visualization
- d3: ^7.8.0
- ngx-charts: ^20.0.0

### Utilities
- date-fns: ^3.0.0
- lodash-es: ^4.17.21

## Success Criteria

- ✅ Settings page allows CRUD operations on agent configurations
- ✅ Real-time message display with < 500ms latency
- ✅ Conversation history loads from JSON files
- ✅ Negotiation cycles clearly visualized
- ✅ Budget vs. quotes comparison displayed
- ✅ Responsive design (desktop, tablet, mobile)
- ✅ Error handling and reconnection logic
- ✅ Smooth animations and transitions
- ✅ Accessible (WCAG 2.1 Level AA)

## Future Enhancements

- Export conversation to PDF/CSV
- Filter messages by agent/type
- Search functionality
- Historical negotiation comparison
- Agent performance analytics
- Custom alert rules
- Multi-language support
- Dark mode toggle
