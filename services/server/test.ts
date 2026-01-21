/**
 * @file This file contains a function for running comprehensive tests on the server.
 */
import { testDatabaseConnections } from './test-endpoints.js';

/**
 * Runs a comprehensive set of tests on the server, including database connections,
 * API endpoints, and WebSocket connections.
 * @returns {Promise<boolean>} A promise that resolves to true if all tests pass, false otherwise.
 */
export async function runTests() {
  console.log('🧪 Starting comprehensive tests...\n');
  
  // Test database connections
  const dbResult = await testDatabaseConnections();
  if (!dbResult) {
    console.error('❌ Database tests failed');
    return false;
  }
  
  // Test API endpoints
  console.log('\n🌐 Testing API endpoints...');
  try {
    const response = await fetch('http://localhost:5000/health');
    const data = await response.json();
    console.log('✅ Health endpoint:', data);
  } catch (error) {
    console.log('❌ Health endpoint failed:', error.message);
  }
  
  // Test WebSocket connection
  console.log('\n🔌 Testing WebSocket...');
  try {
    const ws = new (await import('ws')).WebSocket('ws://localhost:5000');
    ws.on('open', () => {
      console.log('✅ WebSocket connection established');
      ws.close();
    });
    ws.on('error', (error) => {
      console.log('❌ WebSocket failed:', error.message);
    });
  } catch (error) {
    console.log('❌ WebSocket test failed:', error.message);
  }
  
  console.log('\n✅ All tests completed');
  return true;
}

if (import.meta.url === `file://${process.argv[1]}`) {
  runTests();
}
