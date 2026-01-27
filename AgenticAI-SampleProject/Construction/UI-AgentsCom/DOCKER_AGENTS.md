# Docker Agent Configuration

## Agent Endpoints

The UI is configured to connect to the following Docker container endpoints:

| Agent | Type | Endpoint | Port |
|-------|------|----------|------|
| Purchase Agent | purchase | http://localhost:10001 | 10001 |
| Cement Agent | cement | http://localhost:10002 | 10002 |
| Steel Agent | steel | http://localhost:10003 | 10003 |

## Configuration Files Updated

1. **Environment Configuration** (`src/environments/environment.ts`):
   - `apiUrl`: http://localhost:10001
   - `wsUrl`: ws://localhost:10001/ws
   - Agent endpoints: 10001, 10002, 10003

2. **Default Agents** (`agent-config.service.ts`):
   - Pre-configured with ports 10001, 10002, 10003
   - Automatically loaded on first run

3. **Settings Form** (`settings.component.ts`):
   - Default port value: 10001

## Testing Agent Connections

### From Settings Page:
1. Navigate to `/settings`
2. Click the WiFi icon next to each agent
3. Status will update to:
   - 🟢 **Online** - Agent is running and accessible
   - ⚪ **Offline** - Agent is not responding
   - 🔴 **Error** - Connection error

### From Command Line:
```bash
# Test Purchase Agent
curl http://localhost:10001/health

# Test Cement Agent
curl http://localhost:10002/health

# Test Steel Agent
curl http://localhost:10003/health
```

## HTTP Polling for Real-time Updates

Since there's no WebSocket backend, the UI uses **HTTP polling** to fetch messages:

- **Polling Endpoint**: `http://localhost:10001/messages`
- **Polling Interval**: 3 seconds (configurable in environment.ts)
- **Method**: GET request every 3 seconds

### Expected API Response Format:
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

The UI will only display new messages (based on timestamp) to avoid duplicates.

## Running the UI

```bash
# Development server
npm start

# Production build
npm run build

# Serve production build
npx http-server dist/ui-agents-com -p 4200
```

The UI will be available at: http://localhost:4200

## Troubleshooting

### Agents Not Connecting
1. Verify Docker containers are running:
   ```bash
   docker ps
   ```

2. Check container logs:
   ```bash
   docker logs <container-name>
   ```

3. Verify port mappings:
   ```bash
   docker port <container-name>
   ```

### CORS Issues
If you encounter CORS errors, ensure your agent containers have CORS enabled:
```python
# Example for FastAPI
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Polling Not Working
1. Verify `/messages` endpoint exists on Purchase Agent (port 10001)
2. Check if endpoint returns JSON array of messages
3. Verify CORS headers allow requests from http://localhost:4200
4. Check browser console for HTTP errors
5. Adjust polling interval in environment.ts if needed

## Loading Conversations

### Option 1: Load Sample Data
- Click "Load Sample Data" button
- Loads 9 pre-configured messages for testing

### Option 2: Load JSON File
- Click "Load JSON File" button
- Select a JSON file from your local system
- File must contain array of ConversationMessage objects
- Example: Load files from `../part-03-a2a-communication/logs/`

### Option 3: HTTP Polling (Live)
- Click "Start Polling" button
- UI polls `http://localhost:10001/messages` every 3 seconds
- New messages automatically appear in conversation flow
- Click "Stop Polling" to stop

## Next Steps

Ready to proceed with **Phase 6: Real-time Integration**?
- WebSocket connection implementation
- SSE fallback mechanism
- Auto-reconnect logic
- Connection status indicators
- Live agent testing
