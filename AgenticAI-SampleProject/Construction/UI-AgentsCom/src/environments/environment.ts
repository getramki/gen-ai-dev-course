export const environment = {
  production: false,
  apiUrl: 'http://localhost:10001',
  pollingInterval: 3000, // 3 seconds
  agentEndpoints: {
    purchase: 'http://localhost:10001',
    cement: 'http://localhost:10002',
    steel: 'http://localhost:10003'
  }
};
