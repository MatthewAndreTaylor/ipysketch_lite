#!/bin/bash

npm install -g html-inline

html-inline frontend_src/sketch.html -o template.html -b frontend_src

escaped_html=$(cat template.html)
escaped_js=$(cat frontend_src/sketch.js)
escaped_css=$(cat frontend_src/sketch.css)

# Replace document.getElementById('root').appendChild(sketch); with el.appendChild(sketch);
escaped_js=$(echo "$escaped_js" | sed "s/document\.getElementById('root')\.appendChild(sketch);/el.appendChild(sketch);/g")

escaped_js="function render({ model, el }) { $escaped_js } export default { render };"

# Write the output into the Python template
echo "template_html = \"\"\"$escaped_html\"\"\"" > ipysketch_lite/_template.py
echo "" >> ipysketch_lite/_template.py
echo "template_js = \"\"\"$escaped_js\"\"\"" >> ipysketch_lite/_template.py
echo "" >> ipysketch_lite/_template.py
echo "template_css = \"\"\"$escaped_css\"\"\"" >> ipysketch_lite/_template.py

# Replace {width}, {height}, {canvas_upload} with 400, 300, return; in $escaped_html
echo "$escaped_html" | sed 's/{width}/400/g; s/{height}/300/g; s/{canvas_upload}/return;/g' > sketch.html

rm template.html

