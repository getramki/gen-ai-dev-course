# Agent Communication Dashboard

Real-time visualization dashboard for A2A (Agent-to-Agent) communication between Construction Purchase Agent, Cement Sales Agent, and Steel Sales Agent.

## Features

- 🎯 **Agent Configuration**: Manage agent endpoints with CRUD operations
- 💬 **Real-time Communication**: View live agent conversations
- 📊 **Negotiation Statistics**: Track budgets, quotes, and cycles
- 📈 **Timeline Visualization**: D3.js-powered message timeline
- 🔄 **HTTP Polling**: Auto-refresh messages from agents
- 📁 **File Loading**: Import conversation logs from JSON files
- 🎨 **Material Design**: Clean, modern UI with Angular Material

## Tech Stack

- **Angular 19** (Standalone Components)
- **Angular Material 19**
- **RxJS + Signals** (State Management)
- **D3.js** (Timeline Visualization)
- **TypeScript**
- **SCSS**

## Prerequisites

- Node.js 18+ and npm
- Docker (for running agent containers)
- Modern web browser

## Installation

```bash
# Install dependencies
npm install

# Development server
npm start

# Production build
npm run build
```

## Docker Agent Configuration

The UI connects to three Docker containers:

| Agent | Port | Endpoint |
|-------|------|----------|
| Purchase Agent | 10001 | http://localhost:10001 |
| Cement Agent | 10002 | http://localhost:10002 |
| Steel Agent | 10003 | http://localhost:10003 |

### Required API Endpoint

Your agents should expose:
```
GET http://localhost:10001/messages
```

**Response Format**:
```json
[
  {
    "timestamp": "2024-01-20T10:30:00.000Z",
    "from_agent": "Purchase Agent",
    "to_agent": "Cement Agent",
    "type": "REQUEST",
    "content": "CYCLE 1: Requesting quote...",
    "llm_reasoning": "Starting negotiation"
  }
]
```

## Usage

### 1. Configure Agents

Navigate to **Settings** (`/settings`):
- Add/edit agent endpoints
- Test connections
- Configure ports (default: 10001, 10002, 10003)

### 2. Load Conversations

Three options available:

**Option A: Sample Data**
- Click "Load Sample Data"
- Loads 9 demo messages

**Option B: JSON File**
- Click "Load JSON File"
- Select conversation log from filesystem
- Example: `../part-03-a2a-communication/logs/conversation_*.json`

**Option C: Live Polling**
- Click "Start Polling"
- Polls Purchase Agent every 3 seconds
- New messages appear automatically
- Click "Stop Polling" to stop

### 3. View Dashboard

The dashboard shows:
- **Agent Cards**: Status, endpoint, message count
- **Conversation Flow**: Real-time message stream with color coding
- **Timeline**: D3.js visualization of message events
- **Statistics**: Budgets, quotes, cycles, negotiation status

## Message Types

Messages are color-coded by type:
- 🟢 **CONNECTED**: Green - Connection established
- 🔵 **REQUEST**: Blue - Quote request
- 🟠 **RESPONSE**: Orange - Quote response
- 🟣 **ANALYSIS**: Purple - Internal analysis

## Project Structure

```
src/app/
├── core/
│   ├── models/          # TypeScript interfaces
│   ├── services/        # Business logic
│   └── interceptors/    # HTTP interceptors
├── features/
│   ├── settings/        # Agent configuration
│   └── communication/   # Dashboard components
└── shared/
    └── components/      # Reusable components
```

## Development

```bash
# Run dev server
npm start

# Build for production
npm run build

# Serve production build
npx http-server dist/ui-agents-com -p 4200
```

## Configuration

Edit `src/environments/environment.ts`:

```typescript
export const environment = {
  production: false,
  apiUrl: 'http://localhost:10001',
  pollingInterval: 3000, // milliseconds
  agentEndpoints: {
    purchase: 'http://localhost:10001',
    cement: 'http://localhost:10002',
    steel: 'http://localhost:10003'
  }
};
```

## Troubleshooting

### Agents Not Connecting
1. Verify Docker containers are running: `docker ps`
2. Check agent logs: `docker logs <container-name>`
3. Test endpoints: `curl http://localhost:10001/health`

### CORS Errors
Ensure agents have CORS enabled for `http://localhost:4200`

### Polling Not Working
1. Verify `/messages` endpoint exists
2. Check endpoint returns JSON array
3. Review browser console for errors

## Documentation

- [Docker Agent Configuration](./DOCKER_AGENTS.md)
- [Implementation Tracker](./IMPLEMENTATION_TRACKER.md)
- [Project Plan](./PROJECT_PLAN.md)

## License

MIT
