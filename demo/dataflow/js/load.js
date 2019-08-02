const {ipcRenderer} = require('electron');
const path = require('path');
const storage = require('electron-json-storage');
const fs = require('fs');

// APK
const selectApkBtn = document.getElementById('select-apk');
selectApkBtn.addEventListener('click', (event) => {
    ipcRenderer.send('open-apk-dialog')
});
let savedApkPath = '',
    savedConfPath = '';
storage.get('config', (error, data) => {
    if (error) throw error;
    if ('apkFilePath' in data)
        savedApkPath = data.apkFilePath;
    if ('confFilePath' in data)
        savedConfPath = data.confFilePath;
});
const jsonSetting = {apkFilePath: savedApkPath, confFilePath: savedConfPath};
ipcRenderer.on('selected-apk', (event, file) => {
    const filePath = file.toString();
    jsonSetting.apkFilePath = filePath;
    storage.set('config', jsonSetting, error => {
        if (error) throw error;
    });
    const selectedApkFile = document.getElementById('selected-apk');
    selectedApkFile.value = path.basename(filePath);
});

// Config file
const selectDirBtn = document.getElementById('select-directory');
selectDirBtn.addEventListener('click', (event) => {
    ipcRenderer.send('open-file-dialog')
});
ipcRenderer.on('selected-directory', (event, file) => {
    const filePath = file.toString();
    jsonSetting.confFilePath = filePath;
    storage.set('config', jsonSetting, error => {
        if (error) throw error;
    });
    const selectedFile = document.getElementById('selected-file');
    selectedFile.value = path.basename(filePath);
    // read csv list
    const jsonObj = JSON.parse(fs.readFileSync(filePath, {encoding: 'utf-8'}));

    for (let i=0; i<jsonObj.source.length; i++) {
        $("#source_table > tbody").append('<tr><td>'+ jsonObj.source[i] +'</td><td>');
    }
    for (let i=0; i<jsonObj.sink.length; i++) {
        $("#sink_table > tbody").append('<tr><td>'+ jsonObj.sink[i] +'</td><td>')
    }
});

