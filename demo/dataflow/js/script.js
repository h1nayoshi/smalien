const {PythonShell} = require('python-shell');
const storage = require('electron-json-storage');
const path = require('path');

const script_btn = document.getElementById('script_btn');
const output = document.getElementById('terminal_output');
script_btn.addEventListener('click', (event) => {
    storage.get('config', (error, data) => {
        if (error) throw error;
        if (Object.keys(data).length !== 0) {
            const target_path = data.apkFilePath;
            const smalien_path = path.resolve('../');
            const options = {
                mode: 'text',
                pythonOptions: ['-u'],
                scriptPath: smalien_path,
                args: ['-path', smalien_path, target_path]
            };
            let pyshell = new PythonShell('main.py', options);
            pyshell.on('message', message => {
                const pelem = document.createElement('p');
                pelem.innerText = message;
                output.insertAdjacentElement('beforeend', pelem);
            });
        };
    });
});

const terminal = document.getElementById('terminal');
