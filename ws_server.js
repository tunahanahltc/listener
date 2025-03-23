const WebSocket = require("ws");
const axios = require("axios");

const PORT = process.env.PORT || 10000;
const FASTAPI_URL = "http://localhost:10001/process"; // FastAPI servisi için

const wss = new WebSocket.Server({ port: PORT });

wss.on("connection", (ws) => {
    console.log("Yeni istemci bağlandı");

    ws.on("message", async (message) => {
        console.log(`İstemciden gelen mesaj: ${message}`);

        try {
            // Veriyi FastAPI'ye gönder (işlenmesi için)
            const response = await axios.post(FASTAPI_URL, { data: message });

            // İşlenmiş veriyi istemciye geri gönder
            ws.send(response.data.processed);
        } catch (error) {
            console.error("FastAPI servisine bağlanırken hata oluştu!", error.message);
        }
    });

    ws.on("close", () => {
        console.log("İstemci bağlantıyı kapattı.");
    });
});

console.log(`WebSocket sunucusu ${PORT} portunda çalışıyor...`);
