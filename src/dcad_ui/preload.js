// Preload uses CommonJS to avoid ESM import issues in Electron preload context
const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('dcad', {
    onAssemblyUpdate: (cb) => ipcRenderer.on('assembly-update', (_e, data) => cb(data))
});
