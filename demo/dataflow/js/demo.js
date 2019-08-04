const d3 = require('d3');
const dagreD3 = require('dagre-d3');
const $ = require('jquery');
const fs = require('fs');
const storage = require('electron-json-storage');
const path = require('path');
require('jquery-resizable');

$(document).ready( () => {
    const selectedFile = document.getElementById('selected-file');
    const selectedApk = document.getElementById('selected-apk');
    storage.get('config', (error, data) => {
        if (error) throw error;
        selectedFile.addEventListener('focus', () => selectedFile.value = data.confFilePath);
        selectedFile.addEventListener('focusout', () => selectedFile.value = path.basename(data.confFilePath));
        selectedApk.addEventListener('focus', () => selectedApk.value = data.apkFilePath);
        selectedApk.addEventListener('focusout', () => selectedApk.value = path.basename(data.confFilePath));
        if ('confFilePath' in data) {
            selectedFile.value = path.basename(data.confFilePath);
        }
        if ('apkFilePath' in data) {
            selectedApk.value = path.basename(data.apkFilePath);
        }
    });
    storage.get('config', (error, data) => {
        if (error) throw error;
        $("#graph_area").resizable({
            stop: () => {
                if (data.confFilePath)
                    showDataFlow(data.confFilePath)
            },
            direction: ['right', 'bottom'],
            maxWidth: $("#graph_area").width
        });
    });
    let timer = setInterval(function(){
        $("#terminal_output").animate({scrollTop: $('#terminal_output')[0].scrollHeight}, "fast");
    },500);
});

function showDataFlow(path)
{
    const content = fs.readFileSync(path, {encoding: 'utf-8'});
    const g = new dagreD3.graphlib.Graph({compound:true})
        .setGraph({})
        .setDefaultEdgeLabel(function() { return {}; });
    const data_list = content.split('\n\n'),
        nodes = data_list[0].split('\n'),
        parents = data_list[1].split('\n'),
        edges = data_list[2].split('\n');

    //console.log("Set nodes");
    for (let i=0; i<nodes.length; i++) {
        if (nodes[i] !== '') {
            let params = nodes[i].split(',');
            //console.log(params[0], params[1]);
            const options = {
                "label": params[1],
                "labelStyle": "fill: #ffffff",
                "clusterLabelPos": "top",
                "description": "AAA"
            };
            if (params.length === 3)
                options.style = "fill: #FF0000";
            g.setNode(params[0], options);
        }
    }
    g.nodes().forEach(function(v) {
        var node = g.node(v);
        node.rx = node.ry = 5;
    });
    //console.log("Set Group");
    for (let i=0; i<parents.length; i++) {
        if (parents[i] !== '') {
            let params = parents[i].split(',');
            //console.log(params[0], params[1]);
            g.setParent(params[0], params[1]);
        }
    }
    //console.log("Set edges");
    for (let i=0; i<edges.length; i++) {
        if (edges[i] !== '') {
            let params = edges[i].split(',');
            //console.log(params[0], params[1]);
            g.setEdge(params[0], params[1],
                {
                    arrowhead: "vee",
                    curve: d3.curveBasis
                });
        }
    }
    // Create the renderer
    const render = new dagreD3.render();
    // Set up an SVG group so that we can translate the final graph.
    const svg = d3.select("svg"),
        inner = svg.select("g"),
        svgGroup = svg.append("g");
    const zoom = d3.zoom().on("zoom", function() {
        inner.attr("transform", d3.event.transform);
    });
    svg.call(zoom);

    // Simple function to style the tooltip for the given node.
    let styleTooltip = function(name, description) {
        return "<p class='name'>" + name + "</p><p class='description'>" + description + "</p>";
    };

    // Run the renderer. This is what draws the final graph.1
    render(d3.select("svg g"), g);

    inner.selectAll("g.node")
        .attr("title", v => { return styleTooltip(v, g.node(v).description) })
        .each(() => { $(this).tipsy({ gravity: "w", opacity: 1, html: true }); });

    // Center the graph
    const initialScale = 0.5;
    svg.call(zoom.transform,
        d3.zoomIdentity.translate(
            (svg.attr("width") - g.graph().width * initialScale)/3, 20)
            .scale(initialScale));

    // svgGroup.attr("transform", "translate(" + xCenterOffset + ", 20)");
    // svg.attr("height", g.graph().height + 40);
}
window.demo = window.demo|| {};
window.demo.showDataFlow = showDataFlow;
// Show Button
const run_btn = $('#runner');
run_btn.on('click', () => {
    storage.get('config', (error, data) => {
        if (error) throw error;
        if (Object.keys(data).length !== 0) {
            const confPath = data.confFilePath;
            if (confPath) {
                showDataFlow(confPath);
            } else{
                $('#err_msg').html('Invalid config file path');
                $('#err_msg').show();
                $("#selected-file").addClass("error");
            }
        }
    });
});

