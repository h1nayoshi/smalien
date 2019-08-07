const {ipcRenderer} = require('electron');
const path = require('path');
const storage = require('electron-json-storage');
const fs = require('fs');
const demo = require('./demo.js');

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
selectDirBtn.on('click', () => {
    ipcRenderer.send('open-file-dialog')
});
let targetCSV = '';
const updateTable = filePath => {
    const jsonObj = JSON.parse(fs.readFileSync(filePath, {encoding: 'utf-8'}));
    const showDataFlow = (path) => demo.showDataFlow(path);
    $("#source_table > tbody").empty();
    $("#sink_table > tbody").empty();
    for (let i = 0; i < jsonObj.source.length; i++) {
        $("#source_table > tbody").append(`<tr><td class="ui transparent button" id="source${i}">` + jsonObj.source[i] + '</td><td>');
        $(`#source${i}`).on('click', () => {
            targetCSV = path.join(__dirname+'/../../../', jsonObj.source[i]);
            exports.targetCSV = targetCSV;
            showDataFlow(targetCSV);
        });
    }
    for (let i=0; i<jsonObj.sink.length; i++) {
        $("#sink_table > tbody").append(`<tr><td class="ui transparent button" id="sink${i}">` + jsonObj.sink[i] + '</td><td>');
        $(`#sink${i}`).on('click', () => {
            targetCSV = path.join(__dirname+'/../../../', jsonObj.sink[i]);
            exports.targetCSV = targetCSV;
            showDataFlow(targetCSV);
        });
    }
};
exports.updateTable = updateTable;

ipcRenderer.on('selected-directory', (event, file) => {
    const filePath = file.toString();
    jsonSetting.confFilePath = filePath;
    storage.set('config', jsonSetting, error => {
        if (error) throw error;
    });
    const selectedFile = $('#selected-file');
    selectedFile.value = path.basename(filePath);

    // read csv list from json file and update table
    updateTable(filePath);
});
