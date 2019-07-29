const {PythonShell} = require('python-shell');

const script_btn = document.getElementById('script_btn');
const output = document.getElementById('terminal_output');
script_btn.addEventListener('click', (event) => {  
    const options = {
      mode: 'text',
      pythonOptions: ['-u'] // get print results in real-time
    };
    let pyshell = new PythonShell(__dirname + '/test.py', options);
    pyshell.on('message', message => {
        const pelem = document.createElement('p');
        pelem.innerText = message;
        output.insertAdjacentElement('beforeend', pelem);
    });
});

const terminal = document.getElementById('terminal');
