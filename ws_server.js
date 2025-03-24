const WebSocket = require('ws');

const wss = new WebSocket.Server({ port: 8080 });

let listenerSocket = null;
const clients = new Set();

wss.on('connection', (ws, req) => {
    const url = req.url;

    if (url.includes('/listener')) {
        console.log('Listener connected');
        listenerSocket = ws;
    } else {
        console.log('New client connected');
        clients.add(ws);
    }

    ws.on('message', (message) => {
        console.log(`Received: ${message}`);

        if (ws === listenerSocket) {
            // Listener'dan gelen veriyi sadece istemcilere ilet
            clients.forEach(client => {
                if (client.readyState === WebSocket.OPEN) {
                    client.send(`Listener says: ${message}`);
                }
            });
        } else {
            // İstemciden gelen veriyi sadece listener'a ilet
            if (listenerSocket && listenerSocket.readyState === WebSocket.OPEN) {
                listenerSocket.send(`Client sent: ${message}`);
            }
        }
    });

    ws.on('close', () => {
        console.log('Client disconnected');
        clients.delete(ws);
        if (ws === listenerSocket) {
            listenerSocket = null;
        }
    });
});

console.log('WebSocket server running on ws://localhost:8080');
