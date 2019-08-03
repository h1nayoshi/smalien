const {PythonShell} = require('python-shell');
const storage = require('electron-json-storage');
const path = require('path');

const output = $('#terminal_output');
$("#script_btn").on('click', () => {
    output.empty();
    $("#load_states").addClass("active");
    storage.get('config', (error, data) => {
        if (error) throw error;
        if (Object.keys(data).length !== 0) {
            const target_path = data.apkFilePath;
            const smalien_path = path.resolve('../');
            const ppe =$('.ui.checkbox').checkbox('is checked');
            if (ppe)
                args = ['-ppe', '-path', smalien_path, target_path];
            else
                args = ['-path', smalien_path, target_path]
            const options = {
                mode: 'text',
                pythonOptions: ['-u'],
                scriptPath: smalien_path,
                args: args
            };
            const pyshell = new PythonShell('main.py', options);
            pyshell.on('message', message => {
                output.append('<pre>'+ message +'</pre>');
            });
            pyshell.end((err, code, signal) => {
                if (err) throw err;
                $("#load_states").removeClass("active");
            });
        }
    });
});
