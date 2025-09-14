import { app, BrowserWindow } from 'electron';
import path from 'path';
import { fileURLToPath } from 'url';
import http from 'http';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

let mainWindow;

function createWindow() {
    const win = new BrowserWindow({
        width: 1200,
        height: 800,
        webPreferences: {
            preload: path.join(__dirname, 'preload.js'),
        }
    });
    win.loadFile(path.join(__dirname, 'public', 'index.html'));
    mainWindow = win;
}


app.whenReady().then(() => {
    createWindow();
    startHttpServer();
    app.on('activate', () => {
        if (BrowserWindow.getAllWindows().length === 0) createWindow();
    });
});

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') app.quit();
});

// Simple HTTP server for live update
function startHttpServer(port = 5123) {
    const server = http.createServer((req, res) => {
        if (req.method === 'POST' && req.url === '/update') {
            let body = '';
            req.on('data', chunk => { body += chunk; });
            req.on('end', () => {
                try {
                    const data = JSON.parse(body);
                    console.log('[dcad_ui] Received /update payload name:', data.name, 'parts:', data.parts?.length || 0);
                    if (mainWindow) {
                        mainWindow.webContents.send('assembly-update', data);
                    }
                    res.writeHead(200, { 'Content-Type': 'application/json' });
                    res.end(JSON.stringify({ status: 'ok' }));
                } catch (e) {
                    res.writeHead(400, { 'Content-Type': 'application/json' });
                    res.end(JSON.stringify({ status: 'error', message: e.message }));
                }
            });
        } else if (req.method === 'GET' && req.url === '/health') {
            res.writeHead(200, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify({ status: 'up' }));
        } else {
            res.writeHead(404);
            res.end();
        }
    });
    server.listen(port, () => {
        console.log(`[dcad_ui] HTTP update server listening on http://localhost:${port}`);
    });
}
