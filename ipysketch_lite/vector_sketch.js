// Copyright: Matthew Taylor, 2025

export default {
  async render({ model, el }) {
    const { default: p5 } = await import("https://cdn.jsdelivr.net/npm/p5@1.9.0/+esm");

    let lines = [];
    let currentLine = [];
    let isDrawing = false;
    const width = model.width;
    const height = model.height;
    let sampleInterval = 25;
    let lastTime = new Date();

    let undoStack = [];
    let redoStack = [];

    function saveState() {
      undoStack.push(JSON.parse(JSON.stringify(lines)));
      redoStack = [];
    }

    var sketch = document.createElement("div");
    sketch.id = "sketch";
    sketch.innerHTML = `
<div class="toolbar">
    <label class="color-picker-container" for="color">
      <svg viewBox="0 0 24 24"><path d="M18.5 3A2.5 2.5 0 0 1 21 5.5q-.1 2.1-3.5 5.4a34 34 0 0 1-6.8 5.5l-3.3 2.8L4 15.5l2.8-3.4a57 57 0 0 1 5.5-6.7c2.2-2.1 4-3.4 6.2-2.4M5 20h14v2H5z"/></svg>
      <input id="color" type="color" value="#000000" title="brush color" />
    </label>
    <button id="clear">
      <span>clear</span>
      <svg viewBox="0 0 24 24"><path d="M6 19q.2 1.8 2 2h8a2 2 0 0 0 2-2V7H6zM19 4h-3.5l-.7-.7a2 2 0 0 0-1.4-.6h-2.8a2 2 0 0 0-1.4.6l-.7.7H5v2h14z"/></svg>
    </button>
    <button id="undo">
      <span>undo</span>
      <svg viewBox="0 0 24 24"><path d="M12 4V1L7 6l5 5V8a8 8 0 0 1 8 8q0 3.4-2.3 5.7l1.4 1.4A10 10 0 0 0 22 16 10 10 0 0 0 12 6z"/></svg>
    </button>
    <button id="redo">
      <svg viewBox="0 0 24 24"><path d="M12 4V1L17 6l-5 5V8a8 8 0 0 0-8 8q0 3.4 2.3 5.7L4.9 23A10 10 0 0 1 2 16 10 10 0 0 1 12 6z"/></svg>
      <span>redo</span>
    </button>
  </div>`;

    var colorInput = sketch.querySelector("#color");
    const canvasContainer = document.createElement("div");
    canvasContainer.id = "canvas";
    sketch.appendChild(canvasContainer);
    el.appendChild(sketch);

    function drawSmoothLine(p, points, color) {
      if (points.length < 2) return;
      p.stroke(color);
      p.noFill();
      p.beginShape();
      for (let point of points) p.vertex(point.x, point.y);
      p.endShape();
    }

    new p5((p) => {
      p.setup = () => {
        const cnv = p.createCanvas(width, height);
        cnv.parent(canvasContainer);
        p.strokeWeight(2);
      };

      p.draw = () => {
        p.background(255);
        for (let [line, color] of lines) {
          drawSmoothLine(p, line, color);
        }
        if (isDrawing) {
          drawSmoothLine(p, currentLine, colorInput.value);
        }
      };

      p.mousePressed = () => {
        if (p.mouseX >= 0 && p.mouseX <= width && p.mouseY >= 0 && p.mouseY <= height) {
          saveState();
          isDrawing = true;
          currentLine = [p.createVector(p.mouseX, p.mouseY)];
          canvasUpload();
        }
      };

      p.mouseDragged = () => {
        var ms = new Date();
        if (ms - lastTime < sampleInterval) {
          return;
        }
        lastTime = ms;
        if (isDrawing) {
          let prev = currentLine[currentLine.length - 1];
          let curr = p.createVector(p.mouseX, p.mouseY);
          if (p5.Vector.dist(prev, curr) > 2) {
            currentLine.push(curr);
          }
        }
      };

      p.mouseReleased = () => {
        if (isDrawing) {
          isDrawing = false;
          lines.push([currentLine, colorInput.value]);
          canvasUpload();
        }
      };
    });

    function toSVG(lines) {
      let svgHeader = `<svg viewBox="0 0 ${width} ${height}" xmlns="http://www.w3.org/2000/svg"><g stroke-width="1">`;
      let svgPaths = lines.map(([points, color]) => {
        let pathData = points
          .map((p, i) => (i === 0 ? `M ${p.x} ${p.y}` : `L ${p.x} ${p.y}`))
          .join(" ");
        return `<path d="${pathData}" stroke="${color}" fill="none" />`;
      });
      let svgFooter = `</g></svg>`;
      return svgHeader + svgPaths.join("") + svgFooter;
    }

    let canvas = sketch.querySelector("canvas");

    function canvasUpload() {
      model.canvas_upload /* prettier-ignore */
    }

    sketch.querySelector("#undo").addEventListener("click", () => {
      if (undoStack.length > 0) {
        redoStack.push(lines);
        lines = undoStack.pop();
        canvasUpload();
      }
    });

    sketch.querySelector("#redo").addEventListener("click", () => {
      if (redoStack.length > 0) {
        undoStack.push(lines);
        lines = redoStack.pop();
        canvasUpload();
      }
    });

    sketch.querySelector("#clear").addEventListener("click", () => {
      undoStack.push(lines);
      lines = [];
      canvasUpload();
    });

    canvasUpload();
  }
};
