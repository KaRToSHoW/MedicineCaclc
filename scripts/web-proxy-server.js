// Simple HTTP proxy server to serve HTML wrapper for Expo Metro Bundler
const http = require('http');
const httpProxy = require('http-proxy');
const fs = require('fs');
const path = require('path');

const PORT = 3000; // Proxy port (public)
const METRO_PORT = 3001; // Metro Bundler port

// Create a proxy server
const proxy = httpProxy.createProxyServer({
  target: `http://localhost:${METRO_PORT}`,
  changeOrigin: true,
  ws: true, // Enable WebSocket proxying for hot reload
});

// HTML template
const htmlTemplate = `<!DOCTYPE html>
<html lang="ru">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no" />
    <title>Медицинский Калькулятор</title>
    <style>
      * { box-sizing: border-box; }
      html, body, #root {
        width: 100%;
        height: 100%;
        margin: 0;
        padding: 0;
      }
      body {
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        overflow: hidden;
      }
      #root {
        display: flex;
        flex-direction: column;
      }
      .expo-loading {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        text-align: center;
      }
      .spinner {
        width: 50px;
        height: 50px;
        border: 4px solid #f3f3f3;
        border-top: 4px solid #6366f1;
        border-radius: 50%;
        animation: spin 1s linear infinite;
        margin: 0 auto 20px;
      }
      @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
      }
    </style>
  </head>
  <body>
    <div id="root">
      <div class="expo-loading">
        <div class="spinner"></div>
        <p>Загрузка приложения...</p>
      </div>
    </div>
    <script src="/node_modules/expo-router/entry.bundle?platform=web&dev=true&hot=false&lazy=true&transform.routerRoot=app"></script>
  </body>
</html>`;

// Create HTTP server
const server = http.createServer((req, res) => {
  // Serve HTML for root path
  if (req.url === '/' || req.url === '/index.html') {
    res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
    res.end(htmlTemplate);
    return;
  }

  // Proxy all other requests to Metro Bundler
  proxy.web(req, res, (error) => {
    console.error('Proxy error:', error.message);
    res.writeHead(502, { 'Content-Type': 'text/plain' });
    res.end('Metro Bundler unavailable');
  });
});

// Handle WebSocket upgrade for hot reload
server.on('upgrade', (req, socket, head) => {
  proxy.ws(req, socket, head);
});

server.listen(PORT, () => {
  console.log(`✅ Proxy server running on http://localhost:${PORT}`);
  console.log(`📱 Proxying to Metro Bundler at http://localhost:${METRO_PORT}`);
  console.log(`🌐 Open http://localhost:${PORT} in your browser`);
});
