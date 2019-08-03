const {ipcRenderer} = require('electron');
const path = require('path');
const storage = require('electron-json-storage');
const fs = require('fs');

let jsonSetting;
storage.get('config', (error, data) => {
    if (error) throw error;
    jsonSetting = data;
});

// APK
const selectApkBtn = $('#select-apk');
selectApkBtn.on('click', () => {
    ipcRenderer.send('open-apk-dialog')
});
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
const selectDirBtn = $('#select-directory');
selectDirBtn.on('click', (event) => {
    ipcRenderer.send('open-file-dialog')
});
ipcRenderer.on('selected-directory', (event, file) => {
    const filePath = file.toString();
    jsonSetting.confFilePath = filePath;
    storage.set('config', jsonSetting, error => {
        if (error) throw error;
    });
    const selectedFile = $('#selected-file');
    selectedFile.value = path.basename(filePath);

    // read csv list from json file and update table
    const jsonObj = JSON.parse(fs.readFileSync(filePath, {encoding: 'utf-8'}));
    const showDataFlow = (path) => window.demo.showDataFlow(path);
    for (let i = 0; i < jsonObj.source.length; i++) {
        $("#source_table > tbody").append(`<tr id="source${i}"><td>` + jsonObj.source[i] + '</td><td>');
        $(`#source${i}`).on('click', () =>showDataFlow(path.join(__dirname+'/../../../', jsonObj.source[i])));
    }
    for (let i=0; i<jsonObj.sink.length; i++) {
        $("#sink_table > tbody").append(`<tr id="sink${i}"><td>` + jsonObj.sink[i] + '</td><td>');
        $(`#sink${i}`).on('click', () => showDataFlow(path.join(__dirname+'/../../../', jsonObj.sink[i])));
    }
});

