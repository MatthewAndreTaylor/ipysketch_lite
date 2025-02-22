template_html = """<style>#sketch {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}
canvas {
  border: 2px solid #000;
}
.toolbar {
  display: flex;
  gap: 10px;
  margin-bottom: 10px;
  align-items: center;
}
button {
  padding: 6px;
}
input {
  padding: 6px 0;
}
button,
#color {
  border: none;
  background: white;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 4px;
  gap: 5px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}
button svg,
.color-picker-container svg {
  width: 20px;
  height: 20px;
}
button:hover,
.color-picker-container:hover,
.active {
  background: #d6d6d6;
}
.color-picker-container {
  display: flex;
  align-items: center;
  gap: 5px;
  padding: 1px;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  background: white;
  cursor: pointer;
}
.color-picker-container input {
  width: 30px;
  height: 30px;
  padding: 0;
}
</style>
<div id="root"></div>
<script>// Copyright: Matthew Taylor, 2025
var sketch = document.createElement('div');
sketch.innerHTML = `
<div id="sketch">
  <div class="toolbar">
    <label class="color-picker-container" for="color">
      <svg viewBox="0 0 24 24">
        <path
          d="M18.5 3A2.5 2.5 0 0 1 21 5.5q-.1 2.1-3.5 5.4a34 34 0 0 1-6.8 5.5l-3.3 2.8L4 15.5l2.8-3.4a57 57 0 0 1 5.5-6.7c2.2-2.1 4-3.4 6.2-2.4M5 20h14v2H5z"
        />
      </svg>
      <input id="color" type="color" value="#000000" title="brush color" />
    </label>
    <input
      type="range"
      id="size"
      min="3"
      max="30"
      value="4"
      title="Brush size"
    />
    <button id="clear">
      <span>clear</span>
      <svg viewBox="0 0 24 24">
        <path
          d="M6 19q.2 1.8 2 2h8a2 2 0 0 0 2-2V7H6zM19 4h-3.5l-.7-.7a2 2 0 0 0-1.4-.6h-2.8a2 2 0 0 0-1.4.6l-.7.7H5v2h14z"
        />
      </svg>
    </button>
    <button id="undo">
      <span>undo</span>
      <svg viewBox="0 0 24 24">
        <path
          d="M12 4V1L7 6l5 5V8a8 8 0 0 1 8 8q0 3.4-2.3 5.7l1.4 1.4A10 10 0 0 0 22 16 10 10 0 0 0 12 6z"
        />
      </svg>
    </button>
    <button id="redo">
      <svg viewBox="0 0 24 24">
        <path
          d="M12 4V1L17 6l-5 5V8a8 8 0 0 0-8 8q0 3.4 2.3 5.7L4.9 23A10 10 0 0 1 2 16 10 10 0 0 1 12 6z"
        />
      </svg>
      <span>redo</span>
    </button>
    <button id="toggleFill">
      <span>fill</span>
      <svg viewBox="0 0 24 24">
        <path
          d="M5.9 6.9c-4.5 4.5-5.4 5.6-5.4 7 0 3.4 6.2 9.6 9.6 9.6 1.2 0 2.4-.8 6-4.4 2.6-2.4 4.2-3.9 3.7-3.3q-.8 1-.7 2c.2 1.1 1.6 2 2.6 1.5.7-.2.8-1 .8-5 0-4.5 0-4.8-1.7-7-2-3-5.8-5.8-8-5.8-1.3 0-2.4.9-6.9 5.4m5.7-3.3Q10.3 5 12 7.9c1 1.6 1 1.6 4.7 1.6 2.1 0 3.8-.1 3.8-.3 0-.8-2.3-3.4-4.1-4.7Q13 2 11.6 3.6M5.9 8.9c-2.9 3-3.4 3.8-3.4 5.2 0 3 4.6 7.4 7.6 7.4q1.1-.1 4.7-3.5l3.6-3.5-1.6-.5a12 12 0 0 1-6.5-6.1l-1-2.5z"
          fill-rule="evenodd"
        />
      </svg>
    </button>
  </div>
  <canvas id="canvas" width="{width}" height="{height}"></canvas>
</div>
`;

var canvas = sketch.querySelector('canvas');
var colorInput = sketch.querySelector('#color');
colorInput.addEventListener('input', () => {
  ctx.strokeStyle = colorInput.value;
  ctx.fillStyle = colorInput.value;
});

var toggleFillButton = sketch.querySelector('#toggleFill');
toggleFillButton.addEventListener('click', toggleFill);

var brushSize = sketch.querySelector('#size');
brushSize.addEventListener('input', () => {
  ctx.lineWidth = brushSize.value;
});

var ctx = canvas.getContext('2d', { willReadFrequently: true });
ctx.lineWidth = 4;
ctx.lineJoin = 'round';
var drawing = false;
var mouse = { x: 0, y: 0 };
var fillMode = false;
var undoStack = [];
var redoStack = [];

function saveState() {
  redoStack = [];
  undoStack.push(ctx.getImageData(0, 0, canvas.width, canvas.height));
}

function canvasUpload() {
  {canvas_upload} /* prettier-ignore */
}

sketch.querySelector('#undo').addEventListener('click', () => {
  if (undoStack.length > 0) {
    redoStack.push(ctx.getImageData(0, 0, canvas.width, canvas.height));
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.putImageData(undoStack.pop(), 0, 0);
    canvasUpload();
  }
});

sketch.querySelector('#redo').addEventListener('click', () => {
  if (redoStack.length > 0) {
    undoStack.push(ctx.getImageData(0, 0, canvas.width, canvas.height));
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.putImageData(redoStack.pop(), 0, 0);
    canvasUpload();
  }
});

sketch.querySelector('#clear').addEventListener('click', () => {
  undoStack.push(ctx.getImageData(0, 0, canvas.width, canvas.height));
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  canvasUpload();
});

saveState();
canvasUpload();

function toggleFill() {
  fillMode = !fillMode;
  toggleFillButton.classList.toggle('active', fillMode);
}

function hexToRgb(hex) {
  return {
    r: parseInt(hex.substring(1, 3), 16),
    g: parseInt(hex.substring(3, 5), 16),
    b: parseInt(hex.substring(5, 7), 16),
    a: 255
  };
}

canvas.addEventListener('mousedown', e => {
  saveState();

  if (fillMode) {
    floodFill(hexToRgb(colorInput.value), e.offsetX, e.offsetY);
    canvasUpload();
    return;
  }

  mouse = { x: e.offsetX, y: e.offsetY };
  drawing = true;
});

canvas.addEventListener('mousemove', e => {
  if (drawing) {
    drawLine(mouse.x, mouse.y, e.offsetX, e.offsetY);
    mouse = { x: e.offsetX, y: e.offsetY };
  }
});

canvas.addEventListener('mouseup', e => {
  if (drawing) {
    drawLine(mouse.x, mouse.y, e.offsetX, e.offsetY);
    drawing = false;
    canvasUpload();
  }
});

function drawLine(x1, y1, x2, y2) {
  ctx.beginPath();
  ctx.moveTo(x1, y1);
  ctx.lineTo(x2, y2);
  ctx.closePath();
  ctx.stroke();
}

function floodFill(color, x, y) {
  var imgData = ctx.getImageData(0, 0, canvas.width, canvas.height);
  const { width, height, data } = imgData;
  toggleFill();

  if (pixelColMatch(x, y, color, data, width)) {
    return;
  }

  const stack = [[x, y]];
  const visited = new Uint8Array(width * height);
  var baseIdx = (width * y + x) * 4;
  const oColor = {
    r: data[baseIdx],
    g: data[baseIdx + 1],
    b: data[baseIdx + 2],
    a: data[baseIdx + 3]
  };

  while (stack.length) {
    var [cx, cy] = stack.pop();
    if (
      cx < 0 ||
      cy < 0 ||
      cx >= width ||
      cy >= height ||
      visited[cy * width + cx] ||
      !pixelColMatch(cx, cy, oColor, data, width)
    ) {
      continue;
    }

    setPixelCol(cx, cy, color, data, width);
    visited[cy * width + cx] = 1;
    stack.push([cx, cy + 1], [cx, cy - 1], [cx - 1, cy], [cx + 1, cy]);
  }

  ctx.putImageData(imgData, 0, 0);
  for (var i = 1; i < height - 1; i++) {
    for (var j = 1; j < width - 1; j++) {
      var index = i * width + j;
      if (
        visited[index] === 0 &&
        (visited[index - 1] === 1 ||
          visited[index + 1] === 1 ||
          visited[index - width] === 1 ||
          visited[index + width] === 1)
      ) {
        ctx.fillRect(j, i, 1, 1);
      }
    }
  }
}

function pixelColMatch(x, y, color, data, width) {
  var baseIdx = (width * y + x) * 4;
  return (
    data[baseIdx] === color.r &&
    data[baseIdx + 1] === color.g &&
    data[baseIdx + 2] === color.b &&
    data[baseIdx + 3] === color.a
  );
}

function setPixelCol(x, y, color, data, width) {
  var baseIdx = (width * y + x) * 4;
  data[baseIdx] = color.r & 0xff;
  data[baseIdx + 1] = color.g & 0xff;
  data[baseIdx + 2] = color.b & 0xff;
  data[baseIdx + 3] = color.a & 0xff;
}

var rect = canvas.getBoundingClientRect();
var offset = { x: rect.left, y: rect.top };
var touches = [];

canvas.addEventListener('touchstart', e => {
  saveState();
  e.preventDefault();
  rect = canvas.getBoundingClientRect();
  offset = { x: rect.left, y: rect.top };
  touches = Array.from(e.touches);

  if (fillMode) {
    var x = Math.floor(touches[0].clientX - offset.x);
    var y = Math.floor(touches[0].clientY - offset.y);
    floodFill(hexToRgb(colorInput.value), x, y);
  }
});

canvas.addEventListener('touchend', e => {
  canvasUpload();
});

canvas.addEventListener('touchmove', e => {
  if (fillMode) return;

  e.preventDefault();
  rect = canvas.getBoundingClientRect();
  offset = { x: rect.left, y: rect.top };
  for (var i = 0; i < e.changedTouches.length; i++) {
    var touch = e.changedTouches[i];
    var previousTouch = touches.find(t => t.identifier === touch.identifier);
    if (previousTouch) {
      drawLine(
        previousTouch.clientX - offset.x,
        previousTouch.clientY - offset.y,
        touch.clientX - offset.x,
        touch.clientY - offset.y
      );
    }
    touches.splice(i, 1, touch);
  }
});

document.getElementById('root').appendChild(sketch);
</script>"""

template_js  = """function render({ model, el }) { // Copyright: Matthew Taylor, 2025
var sketch = document.createElement('div');
sketch.innerHTML = `
<div id="sketch">
  <div class="toolbar">
    <label class="color-picker-container" for="color">
      <svg viewBox="0 0 24 24">
        <path
          d="M18.5 3A2.5 2.5 0 0 1 21 5.5q-.1 2.1-3.5 5.4a34 34 0 0 1-6.8 5.5l-3.3 2.8L4 15.5l2.8-3.4a57 57 0 0 1 5.5-6.7c2.2-2.1 4-3.4 6.2-2.4M5 20h14v2H5z"
        />
      </svg>
      <input id="color" type="color" value="#000000" title="brush color" />
    </label>
    <input
      type="range"
      id="size"
      min="3"
      max="30"
      value="4"
      title="Brush size"
    />
    <button id="clear">
      <span>clear</span>
      <svg viewBox="0 0 24 24">
        <path
          d="M6 19q.2 1.8 2 2h8a2 2 0 0 0 2-2V7H6zM19 4h-3.5l-.7-.7a2 2 0 0 0-1.4-.6h-2.8a2 2 0 0 0-1.4.6l-.7.7H5v2h14z"
        />
      </svg>
    </button>
    <button id="undo">
      <span>undo</span>
      <svg viewBox="0 0 24 24">
        <path
          d="M12 4V1L7 6l5 5V8a8 8 0 0 1 8 8q0 3.4-2.3 5.7l1.4 1.4A10 10 0 0 0 22 16 10 10 0 0 0 12 6z"
        />
      </svg>
    </button>
    <button id="redo">
      <svg viewBox="0 0 24 24">
        <path
          d="M12 4V1L17 6l-5 5V8a8 8 0 0 0-8 8q0 3.4 2.3 5.7L4.9 23A10 10 0 0 1 2 16 10 10 0 0 1 12 6z"
        />
      </svg>
      <span>redo</span>
    </button>
    <button id="toggleFill">
      <span>fill</span>
      <svg viewBox="0 0 24 24">
        <path
          d="M5.9 6.9c-4.5 4.5-5.4 5.6-5.4 7 0 3.4 6.2 9.6 9.6 9.6 1.2 0 2.4-.8 6-4.4 2.6-2.4 4.2-3.9 3.7-3.3q-.8 1-.7 2c.2 1.1 1.6 2 2.6 1.5.7-.2.8-1 .8-5 0-4.5 0-4.8-1.7-7-2-3-5.8-5.8-8-5.8-1.3 0-2.4.9-6.9 5.4m5.7-3.3Q10.3 5 12 7.9c1 1.6 1 1.6 4.7 1.6 2.1 0 3.8-.1 3.8-.3 0-.8-2.3-3.4-4.1-4.7Q13 2 11.6 3.6M5.9 8.9c-2.9 3-3.4 3.8-3.4 5.2 0 3 4.6 7.4 7.6 7.4q1.1-.1 4.7-3.5l3.6-3.5-1.6-.5a12 12 0 0 1-6.5-6.1l-1-2.5z"
          fill-rule="evenodd"
        />
      </svg>
    </button>
  </div>
  <canvas id="canvas" width="{width}" height="{height}"></canvas>
</div>
`;

var canvas = sketch.querySelector('canvas');
var colorInput = sketch.querySelector('#color');
colorInput.addEventListener('input', () => {
  ctx.strokeStyle = colorInput.value;
  ctx.fillStyle = colorInput.value;
});

var toggleFillButton = sketch.querySelector('#toggleFill');
toggleFillButton.addEventListener('click', toggleFill);

var brushSize = sketch.querySelector('#size');
brushSize.addEventListener('input', () => {
  ctx.lineWidth = brushSize.value;
});

var ctx = canvas.getContext('2d', { willReadFrequently: true });
ctx.lineWidth = 4;
ctx.lineJoin = 'round';
var drawing = false;
var mouse = { x: 0, y: 0 };
var fillMode = false;
var undoStack = [];
var redoStack = [];

function saveState() {
  redoStack = [];
  undoStack.push(ctx.getImageData(0, 0, canvas.width, canvas.height));
}

function canvasUpload() {
  {canvas_upload} /* prettier-ignore */
}

sketch.querySelector('#undo').addEventListener('click', () => {
  if (undoStack.length > 0) {
    redoStack.push(ctx.getImageData(0, 0, canvas.width, canvas.height));
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.putImageData(undoStack.pop(), 0, 0);
    canvasUpload();
  }
});

sketch.querySelector('#redo').addEventListener('click', () => {
  if (redoStack.length > 0) {
    undoStack.push(ctx.getImageData(0, 0, canvas.width, canvas.height));
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.putImageData(redoStack.pop(), 0, 0);
    canvasUpload();
  }
});

sketch.querySelector('#clear').addEventListener('click', () => {
  undoStack.push(ctx.getImageData(0, 0, canvas.width, canvas.height));
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  canvasUpload();
});

saveState();
canvasUpload();

function toggleFill() {
  fillMode = !fillMode;
  toggleFillButton.classList.toggle('active', fillMode);
}

function hexToRgb(hex) {
  return {
    r: parseInt(hex.substring(1, 3), 16),
    g: parseInt(hex.substring(3, 5), 16),
    b: parseInt(hex.substring(5, 7), 16),
    a: 255
  };
}

canvas.addEventListener('mousedown', e => {
  saveState();

  if (fillMode) {
    floodFill(hexToRgb(colorInput.value), e.offsetX, e.offsetY);
    canvasUpload();
    return;
  }

  mouse = { x: e.offsetX, y: e.offsetY };
  drawing = true;
});

canvas.addEventListener('mousemove', e => {
  if (drawing) {
    drawLine(mouse.x, mouse.y, e.offsetX, e.offsetY);
    mouse = { x: e.offsetX, y: e.offsetY };
  }
});

canvas.addEventListener('mouseup', e => {
  if (drawing) {
    drawLine(mouse.x, mouse.y, e.offsetX, e.offsetY);
    drawing = false;
    canvasUpload();
  }
});

function drawLine(x1, y1, x2, y2) {
  ctx.beginPath();
  ctx.moveTo(x1, y1);
  ctx.lineTo(x2, y2);
  ctx.closePath();
  ctx.stroke();
}

function floodFill(color, x, y) {
  var imgData = ctx.getImageData(0, 0, canvas.width, canvas.height);
  const { width, height, data } = imgData;
  toggleFill();

  if (pixelColMatch(x, y, color, data, width)) {
    return;
  }

  const stack = [[x, y]];
  const visited = new Uint8Array(width * height);
  var baseIdx = (width * y + x) * 4;
  const oColor = {
    r: data[baseIdx],
    g: data[baseIdx + 1],
    b: data[baseIdx + 2],
    a: data[baseIdx + 3]
  };

  while (stack.length) {
    var [cx, cy] = stack.pop();
    if (
      cx < 0 ||
      cy < 0 ||
      cx >= width ||
      cy >= height ||
      visited[cy * width + cx] ||
      !pixelColMatch(cx, cy, oColor, data, width)
    ) {
      continue;
    }

    setPixelCol(cx, cy, color, data, width);
    visited[cy * width + cx] = 1;
    stack.push([cx, cy + 1], [cx, cy - 1], [cx - 1, cy], [cx + 1, cy]);
  }

  ctx.putImageData(imgData, 0, 0);
  for (var i = 1; i < height - 1; i++) {
    for (var j = 1; j < width - 1; j++) {
      var index = i * width + j;
      if (
        visited[index] === 0 &&
        (visited[index - 1] === 1 ||
          visited[index + 1] === 1 ||
          visited[index - width] === 1 ||
          visited[index + width] === 1)
      ) {
        ctx.fillRect(j, i, 1, 1);
      }
    }
  }
}

function pixelColMatch(x, y, color, data, width) {
  var baseIdx = (width * y + x) * 4;
  return (
    data[baseIdx] === color.r &&
    data[baseIdx + 1] === color.g &&
    data[baseIdx + 2] === color.b &&
    data[baseIdx + 3] === color.a
  );
}

function setPixelCol(x, y, color, data, width) {
  var baseIdx = (width * y + x) * 4;
  data[baseIdx] = color.r & 0xff;
  data[baseIdx + 1] = color.g & 0xff;
  data[baseIdx + 2] = color.b & 0xff;
  data[baseIdx + 3] = color.a & 0xff;
}

var rect = canvas.getBoundingClientRect();
var offset = { x: rect.left, y: rect.top };
var touches = [];

canvas.addEventListener('touchstart', e => {
  saveState();
  e.preventDefault();
  rect = canvas.getBoundingClientRect();
  offset = { x: rect.left, y: rect.top };
  touches = Array.from(e.touches);

  if (fillMode) {
    var x = Math.floor(touches[0].clientX - offset.x);
    var y = Math.floor(touches[0].clientY - offset.y);
    floodFill(hexToRgb(colorInput.value), x, y);
  }
});

canvas.addEventListener('touchend', e => {
  canvasUpload();
});

canvas.addEventListener('touchmove', e => {
  if (fillMode) return;

  e.preventDefault();
  rect = canvas.getBoundingClientRect();
  offset = { x: rect.left, y: rect.top };
  for (var i = 0; i < e.changedTouches.length; i++) {
    var touch = e.changedTouches[i];
    var previousTouch = touches.find(t => t.identifier === touch.identifier);
    if (previousTouch) {
      drawLine(
        previousTouch.clientX - offset.x,
        previousTouch.clientY - offset.y,
        touch.clientX - offset.x,
        touch.clientY - offset.y
      );
    }
    touches.splice(i, 1, touch);
  }
});

el.appendChild(sketch); } export default { render };"""

template_css = """#sketch {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}
canvas {
  border: 2px solid #000;
}
.toolbar {
  display: flex;
  gap: 10px;
  margin-bottom: 10px;
  align-items: center;
}
button {
  padding: 6px;
}
input {
  padding: 6px 0;
}
button,
#color {
  border: none;
  background: white;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 4px;
  gap: 5px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}
button svg,
.color-picker-container svg {
  width: 20px;
  height: 20px;
}
button:hover,
.color-picker-container:hover,
.active {
  background: #d6d6d6;
}
.color-picker-container {
  display: flex;
  align-items: center;
  gap: 5px;
  padding: 1px;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  background: white;
  cursor: pointer;
}
.color-picker-container input {
  width: 30px;
  height: 30px;
  padding: 0;
}"""
