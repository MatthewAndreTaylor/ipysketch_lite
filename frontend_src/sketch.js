var canvas = document.getElementById('canvas');
var colorInput = document.getElementById('color');

colorInput.addEventListener('input', () => {
  ctx.strokeStyle = colorInput.value;
  ctx.fillStyle = colorInput.value;
});

var toggleFillButton = document.getElementById('toggleFill');
var brushSize = document.getElementById('size');
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

function undo() {
  if (undoStack.length > 0) {
    redoStack.push(ctx.getImageData(0, 0, canvas.width, canvas.height));
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.putImageData(undoStack.pop(), 0, 0);
  }
}

function redo() {
  if (redoStack.length > 0) {
    undoStack.push(ctx.getImageData(0, 0, canvas.width, canvas.height));
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.putImageData(redoStack.pop(), 0, 0);
  }
}

function canvasUpload() {
  {canvas_upload} /* prettier-ignore */
}

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

function clearCanvas() {
  ctx.clearRect(0, 0, ctx.canvas.width, ctx.canvas.height);
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
