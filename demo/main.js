const { app, BrowserWindow, Menu, ipcMain, dialog} = require('electron');
const debug = /--debug/.test(process.argv[2]);
// prevent garbage collection
let mainWindow = null;
function createWindow () {
  // Create the browser window.
    mainWindow = new BrowserWindow({
        width: 1100, height: 800,
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
    const menu = Menu.buildFromTemplate(template);
    Menu.setApplicationMenu(menu);
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
  if (mainWindow === null)  createWindow()
});

ipcMain.on('open-file-dialog', (event) => {
  dialog.showOpenDialog({
      properties: ['openFile'],
      title: "Select Config File",
      defaultPath: '../',
      filters: [
          { name: "JSON", extensions: ['json']},
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
      defaultPath: '../',
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

isMac = process.platform === 'darwin';

const template = [
    {
        label: app.getName(),
        submenu: [
            { role: 'about' },
            { type: 'separator' },
            { role: 'services' },
            { type: 'separator' },
            { role: 'hide' },
            { role: 'hideothers' },
            { role: 'unhide' },
            { type: 'separator' },
            { role: 'quit' }
        ]
    },
    {
        label: 'Edit',
        submenu: [
            { role: 'undo' },
            { role: 'redo' },
            { type: 'separator' },
            { role: 'cut' },
            { role: 'copy' },
            { role: 'paste' },
            ...(isMac ? [
                { role: 'pasteAndMatchStyle' },
                { role: 'delete' },
                { role: 'selectAll' },
                { type: 'separator' },
                {
                    label: 'Speech',
                    submenu: [
                        { role: 'startspeaking' },
                        { role: 'stopspeaking' }
                    ]
                }
            ] : [
                { role: 'delete' },
                { type: 'separator' },
                { role: 'selectAll' }
            ])
        ]
    },
    {
        label: 'View',
        submenu: [
            { role: 'toggledevtools'},
            { role: 'reload' },
            { role: 'forcereload' }
        ]
    }
];
