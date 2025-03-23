const WebSocket = require('ws');
const wss = new WebSocket.Server({ port: 8080 });  // WebSocket portu 8080

wss.on('connection', (ws) => {
  console.log('Yeni istemci bağlandı');
  
  ws.on('message', (message) => {
    console.log(`İstemciden gelen mesaj: ${message}`);
    
    // İstemciden gelen veriyi işleyip geri gönder
    let processedMessage = message.toUpperCase();  // Mesajı işleyelim
    ws.send(`İşlenmiş veri: ${processedMessage}`);
  });
});

console.log("WebSocket sunucusu 8080 portunda çalışıyor.");
