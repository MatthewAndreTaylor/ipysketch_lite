// Copyright: Matthew Taylor, 2025

function pathData(points) {
  return points.map((point, i) => `${i ? "L" : "M"} ${point.x} ${point.y}`).join(" ");
}

export default {
  async render({ model, el }) {
    const { default: p5 } = await import("https://cdn.jsdelivr.net/npm/p5@1.9.0/+esm");

    let lines = [];
    let fills = [];
    let regions = [];
    let currentLine = null;
    let fillMode = false;
    let canvas;
    let painter;
    const width = model.width;
    const height = model.height;
    const sampleInterval = 20;
    let lastTime = Date.now();

    const undoStack = [];
    let redoStack = [];

    function saveState() {
      // Completed strokes and fills are immutable; only their arrays change.
      undoStack.push({ lines: [...lines], fills: [...fills] });
      redoStack = [];
    }

    const sketch = document.createElement("div");
    sketch.id = "sketch";
    sketch.innerHTML = `
<div class="toolbar">
    <label class="color-picker-container" for="color">
      <svg viewBox="0 0 24 24"><path d="M18.5 3A2.5 2.5 0 0 1 21 5.5q-.1 2.1-3.5 5.4a34 34 0 0 1-6.8 5.5l-3.3 2.8L4 15.5l2.8-3.4a57 57 0 0 1 5.5-6.7c2.2-2.1 4-3.4 6.2-2.4M5 20h14v2H5z"/></svg>
      <input id="color" type="color" value="#000000" title="brush color" />
    </label>
    <input type="range" id="size" min="1" max="30" value="2" title="Line width" aria-label="Line width" />
    <button id="toggleFill" aria-pressed="false" title="Bucket fill">
      <span>fill</span>
      <svg viewBox="0 0 24 24"><path d="M5.9 6.9c-4.5 4.5-5.4 5.6-5.4 7 0 3.4 6.2 9.6 9.6 9.6 1.2 0 2.4-.8 6-4.4 2.6-2.4 4.2-3.9 3.7-3.3q-.8 1-.7 2c.2 1.1 1.6 2 2.6 1.5.7-.2.8-1 .8-5 0-4.5 0-4.8-1.7-7-2-3-5.8-5.8-8-5.8-1.3 0-2.4.9-6.9 5.4m5.7-3.3Q10.3 5 12 7.9c1 1.6 1 1.6 4.7 1.6 2.1 0 3.8-.1 3.8-.3 0-.8-2.3-3.4-4.1-4.7Q13 2 11.6 3.6M5.9 8.9c-2.9 3-3.4 3.8-3.4 5.2 0 3 4.6 7.4 7.6 7.4q1.1-.1 4.7-3.5l3.6-3.5-1.6-.5a12 12 0 0 1-6.5-6.1l-1-2.5z" fill-rule="evenodd"/></svg>
    </button>
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

    const colorInput = sketch.querySelector("#color");
    const sizeInput = sketch.querySelector("#size");
    const fillButton = sketch.querySelector("#toggleFill");
    fillButton.addEventListener("click", () => {
      fillMode = !fillMode;
      fillButton.classList.toggle("active", fillMode);
      fillButton.setAttribute("aria-pressed", String(fillMode));
    });
    const canvasContainer = document.createElement("div");
    canvasContainer.id = "canvas";
    sketch.appendChild(canvasContainer);
    el.appendChild(sketch);

    function drawSmoothLine(p, { points, color, size }) {
      p.strokeWeight(size);
      p.stroke(color);
      if (points.length === 1) {
        p.point(points[0].x, points[0].y);
        return;
      }
      p.noFill();
      p.beginShape();
      for (let point of points) p.vertex(point.x, point.y);
      p.endShape();
    }

    const instance = new p5((p) => {
      painter = p;
      p.setup = () => {
        p.pixelDensity(1);
        const cnv = p.createCanvas(width, height);
        canvas = cnv.elt;
        cnv.parent(canvasContainer);
        p.strokeCap(p.ROUND);
        p.strokeJoin(p.ROUND);
        p.noLoop();
        regions = findFillRegions();
        canvasUpload();
      };

      p.draw = () => {
        p.background(255);
        for (let fill of fills) {
          p.drawingContext.fillStyle = fill.color;
          p.drawingContext.fill(new Path2D(fill.path), "evenodd");
        }
        for (let item of lines) {
          drawSmoothLine(p, item);
        }
        if (currentLine) {
          drawSmoothLine(p, currentLine);
        }
      };

      p.mousePressed = () => {
        if (p.mouseX >= 0 && p.mouseX < width && p.mouseY >= 0 && p.mouseY < height) {
          if (fillMode) {
            const containsClick = (path) => p.drawingContext.isPointInPath(
              new Path2D(path), p.mouseX, p.mouseY, "evenodd"
            );
            const path = regions.find(containsClick);
            if (path) {
              const previous = fills.findLast((fill) => containsClick(fill.path));
              if ((previous?.color || "#ffffff") !== colorInput.value) {
                saveState();
                fills.push({ path, color: colorInput.value });
                canvasUpload();
              }
            }
            return;
          }
          saveState();
          currentLine = {
            points: [p.createVector(p.mouseX, p.mouseY)],
            color: colorInput.value,
            size: Number(sizeInput.value),
          };
          canvasUpload();
        }
      };

      p.mouseDragged = () => {
        const ms = Date.now();
        if (ms - lastTime < sampleInterval) {
          return;
        }
        lastTime = ms;
        if (currentLine) {
          const prev = currentLine.points.at(-1);
          const curr = p.createVector(p.mouseX, p.mouseY);
          if (p5.Vector.dist(prev, curr) > 2) {
            currentLine.points.push(curr);
            p.draw();
          }
        }
      };

      p.mouseReleased = () => {
        if (currentLine) {
          currentLine.points.push(p.createVector(p.mouseX, p.mouseY));
          lines.push(currentLine);
          currentLine = null;
          regions = findFillRegions();
          canvasUpload();
        }
      };
    });

    // Trace the bounded faces of the drawn polylines, including disconnected holes.
    function findFillRegions() {
      // The canvas edge bounds the background without adding a visible stroke.
      const strokes = width > 0 && height > 0 ? [...lines, {
        points: [{ x: 0, y: 0 }, { x: width, y: 0 }, { x: width, y: height }, { x: 0, y: height }, { x: 0, y: 0 }],
        size: 0,
      }] : lines;
      const segments = connectStrokeSegments(strokes);
      const edges = buildFillGraph(segments);
      return traceFillPaths(edges);
    }

    function toSVG() {
      const fillPaths = fills.map((fill) => `<path d="${fill.path}" fill="${fill.color}" fill-rule="evenodd" />`);
      const paths = lines.map((item) => {
        const path = pathData(item.points);
        return `<path d="${path}" stroke="${item.color}" stroke-width="${item.size}" stroke-linecap="round" stroke-linejoin="round" fill="none" />`;
      });
      return `<svg viewBox="0 0 ${width} ${height}" xmlns="http://www.w3.org/2000/svg"><rect width="${width}" height="${height}" fill="white" />${fillPaths.join("")}${paths.join("")}</svg>`;
    }

    function canvasUpload() {
      if (!canvas) return;
      painter.draw();
      model.set('_svg_data', toSVG());
      model.set('_sketch_data', canvas.toDataURL());
      model.save_changes();
    }

    function restoreState(state) {
      lines = state.lines;
      fills = state.fills;
      regions = findFillRegions();
      canvasUpload();
    }

    sketch.querySelector("#undo").addEventListener("click", () => {
      if (undoStack.length > 0) {
        redoStack.push({ lines, fills });
        restoreState(undoStack.pop());
      }
    });

    sketch.querySelector("#redo").addEventListener("click", () => {
      if (redoStack.length > 0) {
        undoStack.push({ lines, fills });
        restoreState(redoStack.pop());
      }
    });

    sketch.querySelector("#clear").addEventListener("click", () => {
      saveState();
      restoreState({ lines: [], fills: [] });
    });

    return () => instance.remove();
  }
};

const epsilon = 1e-8;
const cross = (a, b) => a.x * b.y - a.y * b.x;
const subtract = (a, b) => ({ x: a.x - b.x, y: a.y - b.y });
const dot = (a, b) => a.x * b.x + a.y * b.y;
const clampUnit = (t) => Math.max(0, Math.min(1, t));
const inSegment = (t) => t >= -epsilon && t <= 1 + epsilon;
const interpolate = (a, b, t) => ({ x: a.x + t * (b.x - a.x), y: a.y + t * (b.y - a.y) });

// Use stroke-outline unions if thick stroke sides must create boundaries without crossing centerlines or joined endpoints.
function connectStrokeSegments(strokes) {
  const segments = [];
  const endpoints = [];
  for (const line of strokes) {
    let distance = 0;
    const firstSegment = segments.length;
    for (let i = 1; i < line.points.length; i++) {
      const a = line.points[i - 1];
      const b = line.points[i];
      const length = Math.hypot(b.x - a.x, b.y - a.y);
      if (length > epsilon) segments.push({ a, b, line, start: distance, end: distance + length });
      distance += length;
    }
    if (distance > epsilon) {
      endpoints.push({ point: line.points[0], direction: subtract(segments[firstSegment].a, segments[firstSegment].b), distance: 0, line });
      endpoints.push({ point: line.points.at(-1), direction: subtract(segments.at(-1).b, segments.at(-1).a), distance, line });
    }
  }
  // Join visibly touching stroke ends beneath their ink, without shifting the strokes.
  const joins = [];
  for (const endpoint of endpoints) {
    for (const { point, distance } of strokeContacts(endpoint, segments)) {
      if (distance > epsilon) joins.push({ a: endpoint.point, b: point });
    }
  }
  return segments.concat(joins);
}

function buildFillGraph(segments) {
  for (const segment of segments) segment.cuts = [0, 1];
  for (const [i, first] of segments.entries()) {
    for (let j = i + 1; j < segments.length; j++) cutIntersections(first, segments[j]);
  }
  const vertices = new Map(), edges = [];
  for (const { a, b, cuts } of segments) {
    const points = cuts.sort((a, b) => a - b)
      .filter((t, i, all) => i === 0 || t - all[i - 1] > epsilon)
      .map((t) => fillVertex(vertices, interpolate(a, b, t)));
    for (let i = 1; i < points.length; i++) {
      const a = points[i - 1], b = points[i];
      if (a === b || a.outgoing.some((edge) => edge.to === b)) continue;
      const forward = { from: a, to: b }, reverse = { from: b, to: a, twin: forward };
      forward.twin = reverse;
      a.outgoing.push(forward);
      b.outgoing.push(reverse);
      edges.push(forward, reverse);
    }
  }
  for (const point of vertices.values()) {
    const angle = ({ to }) => Math.atan2(to.y - point.y, to.x - point.x);
    point.outgoing.sort((a, b) => angle(a) - angle(b));
    point.outgoing.forEach((edge, i, outgoing) => {
      edge.twin.next = outgoing[(i + outgoing.length - 1) % outgoing.length];
    });
  }
  return edges;
}

function strokeContacts({ point: end, direction: tangent, distance: along, line }, segments) {
  const contacts = new Map();
  for (const segment of segments) {
    const radius = ((line.size || 0) + (segment.line.size || 0)) / 2;
    if (segment.line === line && (along === 0 ? segment.start : along - segment.end) <= radius + epsilon) continue;
    const direction = subtract(segment.b, segment.a);
    if (Math.abs(cross(tangent, direction)) <= epsilon &&
        Math.abs(cross(subtract(segment.a, end), direction)) > epsilon) continue;
    const t = clampUnit(dot(subtract(end, segment.a), direction) / dot(direction, direction));
    const point = interpolate(segment.a, segment.b, t);
    const distance = Math.hypot(point.x - end.x, point.y - end.y);
    // Keep a contact per stroke so newer strokes cannot steal an older loop's closure.
    if (distance <= radius + epsilon && distance < (contacts.get(segment.line)?.distance ?? Infinity)) {
      contacts.set(segment.line, { point, distance });
    }
  }
  return contacts.values();
}

function cutIntersections(first, second) {
  const addCut = (segment, t) => {
    if (inSegment(t)) segment.cuts.push(clampUnit(t));
  };
  if (Math.max(first.a.x, first.b.x) + epsilon < Math.min(second.a.x, second.b.x) ||
      Math.max(second.a.x, second.b.x) + epsilon < Math.min(first.a.x, first.b.x) ||
      Math.max(first.a.y, first.b.y) + epsilon < Math.min(second.a.y, second.b.y) ||
      Math.max(second.a.y, second.b.y) + epsilon < Math.min(first.a.y, first.b.y)) return;
  const r = subtract(first.b, first.a), s = subtract(second.b, second.a);
  const delta = subtract(second.a, first.a), denominator = cross(r, s);
  if (Math.abs(denominator) > epsilon) {
    const t = cross(delta, s) / denominator, u = cross(delta, r) / denominator;
    if (inSegment(t) && inSegment(u)) {
      addCut(first, t);
      addCut(second, u);
    }
  } else if (Math.abs(cross(delta, r)) <= epsilon * Math.hypot(r.x, r.y)) {
    addCut(first, dot(delta, r) / dot(r, r));
    addCut(first, dot(subtract(second.b, first.a), r) / dot(r, r));
    addCut(second, dot(subtract(first.a, second.a), s) / dot(s, s));
    addCut(second, dot(subtract(first.b, second.a), s) / dot(s, s));
  }
}

function fillVertex(vertices, point) {
  const x = Math.round(point.x / epsilon);
  const y = Math.round(point.y / epsilon);
  // Independent intersection calculations may round into neighboring buckets.
  for (let dx = -1; dx <= 1; dx++) {
    for (let dy = -1; dy <= 1; dy++) {
      const existing = vertices.get(`${x + dx},${y + dy}`);
      if (existing && Math.abs(existing.x - point.x) <= epsilon && Math.abs(existing.y - point.y) <= epsilon) return existing;
    }
  }
  const key = `${x},${y}`;
  if (!vertices.has(key)) vertices.set(key, { ...point, outgoing: [] });
  return vertices.get(key);
}

function traceFillPaths(edges) {
  const regions = [];
  const holes = [];
  for (const start of edges) {
    if (start.visited) continue;
    const ring = [];
    let edge = start;
    let area = 0;
    do {
      edge.visited = true;
      ring.push(edge.from);
      area += cross(edge.from, edge.to) / 2;
      edge = edge.next;
    } while (edge !== start);
    if (area > epsilon) regions.push({ ring, area, path: `${pathData(ring)} Z` });
    else if (area < -epsilon) holes.push(ring);
  }
  const smallestFirst = [...regions].sort((a, b) => a.area - b.area);
  for (const ring of holes) {
    // The left of a clockwise boundary belongs to its enclosing face.
    const [a, b] = ring;
    const { x, y } = subtract(b, a);
    const length = Math.hypot(x, y);
    const offset = Math.min(1e-5, length / 4);
    const sample = { x: (a.x + b.x) / 2 - y / length * offset, y: (a.y + b.y) / 2 + x / length * offset };
    const parent = smallestFirst.find((region) => contains(region.ring, sample));
    if (parent) parent.path += ` ${pathData(ring)} Z`;
  }
  return regions.map(({ path }) => path);
}

function contains(ring, point) {
  let inside = false;
  for (let i = 0, j = ring.length - 1; i < ring.length; j = i++) {
    const a = ring[i], b = ring[j];
    if ((a.y > point.y) !== (b.y > point.y) &&
        point.x < (b.x - a.x) * (point.y - a.y) / (b.y - a.y) + a.x) inside = !inside;
  }
  return inside;
}
