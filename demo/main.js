const { app, BrowserWindow, Menu, ipcMain, dialog} = require('electron');

const debug = /--debug/.test(process.argv[2]);
// prevent garbage collection
let mainWindow = null;
function createWindow () {
  // Create the browser window.
    mainWindow = new BrowserWindow({
        width: 1200, height: 880,
        icon: __dirname + '/icons/alien256.png',
        webPreferences: {
            nodeIntegration: true
        }
    });
    mainWindow.setMenuBarVisibility(false);
    mainWindow.setAutoHideMenuBar(true);
    mainWindow.loadFile(__dirname + '/dataflow/demo.html');
    if (debug) {
        // Open the DevTools.
        mainWindow.webContents.openDevTools();
    }
    mainWindow.on('closed', () => {
        mainWindow = null;
    });
}

app.on('ready', createWindow);
app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit()
  }
});
app.on('activate', () => {
  // On macOS it's common to re-create a window in the app when the
  // dock icon is clicked and there are no other windows open.
  if (win === null)  createWindow()
});

ipcMain.on('open-file-dialog', (event) => {
  dialog.showOpenDialog({
      properties: ['openFile'],
      title: "Select Config File",
      defaultPath: '.',
      filters: [
          { name: "CSV", extensions: ['csv']},
          { name: "ALL Files", extensions: ['*']}
      ]
  }, files => {
      if (files) {
          event.sender.send('selected-directory', files);
      }
  })
});

ipcMain.on('open-apk-dialog', (event) => {
  dialog.showOpenDialog({
      properties: ['openFile'],
      title: "Select APK File",
      defaultPath: '.',
      filters: [
          { name: "APK", extensions: ['apk']},
          { name: "ALL Files", extensions: ['*']}
      ]
  }, files => {
      if (files) {
          event.sender.send('selected-apk', files);
      }
  })
});
