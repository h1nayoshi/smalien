const {PythonShell} = require('python-shell');
const storage = require('electron-json-storage');
const path = require('path');
const demo = require('./demo.js');
const load = require('./load.js');

const output = $('#terminal_output');
$("#static").on('click', () => {
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
            let pkgName = '';
            pyshell.on('message', line => {
                if (line.indexOf("Target pkg name") !== -1) {
                    pkgName = line.trim();
                    pkgName = pkgName.slice(pkgName.indexOf(':')+2);
                }
                output.append('<pre>'+ line +'</pre>');
            });
            // when python script stop, this callback function execute
            pyshell.end((err, code, signal) => {
                if (err) throw err;
                if (code) console.log('The exit code was: ' + code);
                if (signal) console.log('The exit signal was: ' + signal);
                $("#load_states").removeClass("active");
                const outPre = $("#terminal_output").children('pre');
                let instApkPath = outPre[outPre.length - 1].innerText; // last index
                instApkPath = instApkPath.trim();
                instApkPath = instApkPath.slice(instApkPath.indexOf(' ')+1);
                exports.installApkPath = instApkPath;
                storage.get('config', (error, data) => {
                    if (err) throw err;
                    data.confFilePath = path.join(__dirname + '../../../../', `${pkgName}_csvlist.json`);
                    storage.set('config', data, error => {
                        if (error) throw error;
                    });
                    $("#selected-file").val(`${pkgName}_csvlist.json`);
                    load.updateTable(data.confFilePath);
                });
                demo.stopTimer();
            });
        }
    });
});
