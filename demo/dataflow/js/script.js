const {PythonShell} = require('python-shell');
const storage = require('electron-json-storage');
const path = require('path');

const script_btn = document.getElementById('script_btn');
const output = document.getElementById('terminal_output');
script_btn.addEventListener('click', (event) => {
    $("#terminal_output").empty();
    storage.get('config', (error, data) => {
        if (error) throw error;
        if (Object.keys(data).length !== 0) {
            const target_path = data.apkFilePath;
            const smalien_path = path.resolve('../');
            const ppe = document.getElementsByClassName('ui toggle checkbox')[0].children[0].checked
            if (ppe)
              args = ['-ppe', '-path', smalien_path, target_path]
            else 
              args = ['-path', smalien_path, target_path]
            const options = {
                mode: 'text',
                pythonOptions: ['-u'],
                scriptPath: smalien_path,
                args: args
            };
            let pyshell = new PythonShell('main.py', options);
            pyshell.on('message', message => {
                const elem = document.createElement('pre');
                elem.innerText = message;
                output.insertAdjacentElement('beforeend', elem);
            });
        }
    });
});
