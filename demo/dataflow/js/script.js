const {PythonShell} = require('python-shell');
const storage = require('electron-json-storage');
const path = require('path');
const { exec } = require('child_process');

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
            // when python script stop, this callback function execute
            pyshell.end((err, code, signal) => {
                if (err) throw err;
                if (code) console.log('The exit code was: ' + code);
                if (signal) console.log('The exit signal was: ' + signal);
                $("#load_states").removeClass("active");

                storage.get('config', (error, data) => {
                    const command = `aapt dump badging ${data.apkFilePath} | grep package:\\ name | awk \'{print $2}\'| cut -c 6- | tr -d "'"`;
                    exec(command, (err, stdout, stderr) => {
                        if (err) throw err;
                        if (stderr) console.log(`stderr: ${stderr}`);
                        console.log(`stdout: ${stdout}`);
                        const pkg_name = stdout.trim();
                        data.confFilePath = path.join(__dirname + '../../../../', `${pkg_name}_csvlist.json`);
                        console.log(data);
                        storage.set('config', data, error => {
                            if (error) throw error;
                        });
                        $("#selected-file").val(`${pkg_name}_csvlist.json`);
                        window.demo.updateTable(data.confFilePath);
                    });
                });
            });
        }
    });
});
