# smalien

Smalien is an information flow analysis and information leakage detection tool for Android application analysts. Smalien performs static taint analysis of Android applications on a Linux machine as well as dynamic taint analysis, detection of information leakage due to implicit information flows, and privacy policy enforcement on an Android device at runtime.

## Smalien has following functions
- Analyzing an Android application statically and gathers information of classes, methods, variables, etc.
- Presenting the results of the analysis graphically such as a method call graph and an information flow diagram.
- Performing dynamic taint analysis on an Android device.
- Enforcing privacy policy specified by an analyst.
- Detecting information leakage due to implicit information flows.
- Logging actual information operated by any bytecode or API call, such as http request, at runtime to encourage an analyst in his/her inspection.

## Required Tools
- [Apktool](https://ibotpeaches.github.io/Apktool/)
- jarsigner
- keytool

## Usage
Check our [Wiki](https://github.com/h1nayoshi/smalien/wiki) for full instructions.
### Run static analysis
```
python main.py <apk_path>
```
It generates parsed_data.json and data_flows.json as the results.

### Generate graphs
```
python generate_graphs.py parsed_data.json data_flows.json
```
It generates output_class_calls.md and output_data_flows.md as the results. These files includes scripts for [mermaid](https://mermaidjs.github.io). You may use a markdown viewer such as Haroopad to check the graphs.

Currently, Smalien is a prototype of our academic research and doesn't have full-function. We are working on it!

