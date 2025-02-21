#!/bin/bash

npm install -g html-inline

html-inline frontend_src/sketch.html -o template.html -b frontend_src

escaped_html=$(cat template.html)

# Write the output into the Python template
echo "template = \"\"\"$escaped_html\"\"\"" > ipysketch_lite/template.py

# replace {width}, {height}, {canvas_upload} with 400, 300, return; in $escaped_html
echo "$escaped_html" | sed 's/{width}/400/g; s/{height}/300/g; s/{canvas_upload}/return;/g' > sketch.html

