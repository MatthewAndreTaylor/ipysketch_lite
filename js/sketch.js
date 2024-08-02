var canvas = document.getElementById('canvas');
var colorInput = document.getElementById('color');
var toggleFillButton = document.getElementById('toggleFill');
var ctx = canvas.getContext('2d');
ctx.lineWidth = 4;
ctx.lineJoin = 'round';
var drawing = false;
var mouse = { x: 0, y: 0 };
var fillMode = false;

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
  if (fillMode) {
    floodFill(hexToRgb(colorInput.value), e.offsetX, e.offsetY);
    return;
  }

  mouse = { x: e.offsetX, y: e.offsetY };
  drawing = true;
});

canvas.addEventListener('mousemove', e => {
  if (drawing) {
    drawLine(ctx, mouse.x, mouse.y, e.offsetX, e.offsetY);
    mouse = { x: e.offsetX, y: e.offsetY };
  }
});

canvas.addEventListener('mouseup', e => {
  if (drawing) {
    drawLine(ctx, mouse.x, mouse.y, e.offsetX, e.offsetY);
    drawing = false;
  }
});

function drawLine(context, x1, y1, x2, y2) {
  ctx.strokeStyle = colorInput.value;
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
  if (pixelColMatch(x, y, color, data, width)) return;

  const stack = [[x, y]];
  let baseIdx = (width * y + x) * 4;
  const oColor = {
    r: data[baseIdx],
    g: data[baseIdx + 1],
    b: data[baseIdx + 2],
    a: data[baseIdx + 3]
  };

  while (stack.length) {
    var [cx, cy] = stack.pop();
    const move = (dx, dy) => {
      let nx = cx + dx;
      let ny = cy + dy;
      while (
        ny >= 0 &&
        ny < height &&
        pixelColMatch(nx, ny, oColor, data, width)
      ) {
        setPixelCol(nx, ny, color, data, width);
        stack.push([nx, ny]);
        ny += dy;
      }
    };
    move(0, 1);
    move(0, -1);
    move(-1, 0);
    move(1, 0);
  }
  ctx.putImageData(imgData, 0, 0);
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
        ctx,
        previousTouch.clientX - offset.x,
        previousTouch.clientY - offset.y,
        touch.clientX - offset.x,
        touch.clientY - offset.y
      );
    }
    touches.splice(i, 1, touch);
  }
});
