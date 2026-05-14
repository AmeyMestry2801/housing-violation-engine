const WATCHER_LABELS = [
  { value: "peeling_paint", label: "Peeling Paint", color: "#b2721d" },
  { value: "vehicles_on_unpaved", label: "Vehicles on Unpaved", color: "#596275" },
  { value: "abandoned_vehicles", label: "Abandoned Vehicles", color: "#475569" },
  { value: "overgrown_vegetation", label: "Overgrown Vegetation", color: "#3d8b4f" },
  { value: "bad_roof", label: "Bad Roof", color: "#8b3d5e" },
  { value: "broken_door", label: "Broken Door", color: "#9e4a31" },
  { value: "broken_window", label: "Broken Window", color: "#c75b39" },
  { value: "rubbish", label: "Rubbish", color: "#6b7280" },
  { value: "damaged_walk_driveway", label: "Damaged Walk or Driveway", color: "#7c5a43" },
  { value: "damaged_siding", label: "Damaged Siding", color: "#2d6d91" },
  { value: "damaged_gutters", label: "Damaged Gutters", color: "#35627a" },
  { value: "damaged_soffit", label: "Damaged Soffit", color: "#4b5563" },
  { value: "damaged_foundation", label: "Damaged Foundation", color: "#7b4b2a" },
  { value: "damaged_steps", label: "Damaged Steps", color: "#8a6a52" },
  { value: "damaged_porch", label: "Damaged Porch", color: "#94532d" },
  { value: "abandoned", label: "Abandoned", color: "#8c5a2b" }
];

const INSPECTOR_LABELS = [
  { value: "peeling_paint", label: "Peeling Paint", color: "#b2721d" },
  { value: "vehicles_on_unpaved", label: "Vehicles on Unpaved", color: "#596275" },
  { value: "abandoned_vehicles", label: "Abandoned Vehicles", color: "#475569" },
  { value: "overgrown_vegetation", label: "Overgrown Vegetation", color: "#3d8b4f" },
  { value: "bad_roof", label: "Bad Roof", color: "#8b3d5e" },
  { value: "broken_door", label: "Broken Door", color: "#9e4a31" },
  { value: "broken_window", label: "Broken Window", color: "#c75b39" },
  { value: "rubbish", label: "Rubbish", color: "#6b7280" },
  { value: "damaged_walk_driveway", label: "Damaged Walk or Driveway", color: "#7c5a43" },
  { value: "damaged_siding", label: "Damaged Siding", color: "#2d6d91" },
  { value: "damaged_gutters", label: "Damaged Gutters", color: "#35627a" },
  { value: "damaged_soffit", label: "Damaged Soffit", color: "#4b5563" },
  { value: "damaged_foundation", label: "Damaged Foundation", color: "#7b4b2a" },
  { value: "damaged_steps", label: "Damaged Steps", color: "#8a6a52" },
  { value: "damaged_porch", label: "Damaged Porch", color: "#94532d" },
  { value: "abandoned", label: "Abandoned", color: "#8c5a2b" }
];

const DEMO_IMAGE =
  "data:image/svg+xml;utf8," +
  encodeURIComponent(`
    <svg xmlns="http://www.w3.org/2000/svg" width="1280" height="720" viewBox="0 0 1280 720">
      <defs>
        <linearGradient id="sky" x1="0" x2="0" y1="0" y2="1">
          <stop offset="0%" stop-color="#dfeef4"/>
          <stop offset="100%" stop-color="#f7efe3"/>
        </linearGradient>
      </defs>
      <rect width="1280" height="720" fill="url(#sky)"/>
      <rect y="480" width="1280" height="240" fill="#9db58f"/>
      <rect y="550" width="1280" height="170" fill="#7d8c74"/>
      <rect x="160" y="250" width="420" height="270" rx="8" fill="#d8c3ab" stroke="#8f735a" stroke-width="6"/>
      <polygon points="130,270 370,130 620,270" fill="#695244"/>
      <rect x="230" y="330" width="110" height="105" fill="#7e8b93"/>
      <rect x="392" y="330" width="112" height="105" fill="#7e8b93"/>
      <rect x="340" y="385" width="82" height="135" fill="#6b4735"/>
      <rect x="228" y="322" width="116" height="8" fill="#9e5237"/>
      <rect x="390" y="322" width="116" height="8" fill="#9e5237"/>
      <rect x="870" y="270" width="220" height="210" rx="8" fill="#cbb095" stroke="#7e6752" stroke-width="6"/>
      <polygon points="840,290 980,190 1120,290" fill="#59453a"/>
      <rect x="930" y="340" width="70" height="92" fill="#4f5a62"/>
      <rect x="960" y="210" width="24" height="80" fill="#2f343a"/>
      <path d="M 182 520 C 245 468, 315 470, 382 520" fill="none" stroke="#45683d" stroke-width="46" stroke-linecap="round"/>
      <path d="M 450 518 C 495 472, 532 478, 570 518" fill="none" stroke="#577d4f" stroke-width="34" stroke-linecap="round"/>
      <rect x="740" y="530" width="420" height="70" fill="#6a6761"/>
      <line x1="800" y1="530" x2="800" y2="600" stroke="#f7f3ec" stroke-width="5"/>
      <line x1="900" y1="530" x2="900" y2="600" stroke="#f7f3ec" stroke-width="5"/>
      <line x1="1000" y1="530" x2="1000" y2="600" stroke="#f7f3ec" stroke-width="5"/>
      <line x1="1100" y1="530" x2="1100" y2="600" stroke="#f7f3ec" stroke-width="5"/>
      <rect x="392" y="196" width="96" height="22" fill="#2d3440"/>
      <rect x="1030" y="485" width="66" height="26" transform="rotate(-8 1030 485)" fill="#272727"/>
      <text x="44" y="62" fill="#54483d" font-size="30" font-family="Georgia">Demo parcel image for audit presentation</text>
    </svg>
  `);

const roleSelect = document.getElementById("roleSelect");
const labelSelect = document.getElementById("labelSelect");
const imageUpload = document.getElementById("imageUpload");
const targetImage = document.getElementById("targetImage");
const imageStage = document.getElementById("imageStage");
const zoomSurface = document.getElementById("zoomSurface");
const boxLayer = document.getElementById("boxLayer");
const drawLayer = document.getElementById("drawLayer");
const annotationList = document.getElementById("annotationList");
const jsonOutput = document.getElementById("jsonOutput");
const parcelNameInput = document.getElementById("parcelName");
const workspaceTitle = document.getElementById("workspaceTitle");
const statusText = document.getElementById("statusText");
const emptyState = document.getElementById("emptyState");
const pendingBoxPanel = document.getElementById("pendingBoxPanel");
const pendingBoxText = document.getElementById("pendingBoxText");
const savePendingTagButton = document.getElementById("savePendingTag");
const discardPendingTagButton = document.getElementById("discardPendingTag");
const editBoxPanel = document.getElementById("editBoxPanel");
const editBoxText = document.getElementById("editBoxText");
const saveEditedTagButton = document.getElementById("saveEditedTag");
const cancelEditTagButton = document.getElementById("cancelEditTag");
const tagModeButton = document.getElementById("tagModeButton");
const panModeButton = document.getElementById("panModeButton");
const zoomInButton = document.getElementById("zoomInButton");
const zoomOutButton = document.getElementById("zoomOutButton");
const resetViewButton = document.getElementById("resetViewButton");
const zoomValue = document.getElementById("zoomValue");

let annotations = [];
let currentImageName = "";
let drawState = null;
let pendingAnnotation = null;
let editingIndex = null;
let viewMode = "tag";
let zoomLevel = 1;
let panX = 0;
let panY = 0;
let panState = null;
let isSpacePressed = false;

function getActiveLabels() {
  return roleSelect.value === "inspector" ? INSPECTOR_LABELS : WATCHER_LABELS;
}

function populateLabels() {
  const labels = getActiveLabels();
  labelSelect.innerHTML = "";

  labels.forEach((item) => {
    const option = document.createElement("option");
    option.value = item.value;
    option.textContent = item.label;
    option.dataset.color = item.color;
    labelSelect.appendChild(option);
  });
}

function getSelectedLabel() {
  const labels = getActiveLabels();
  return labels.find((item) => item.value === labelSelect.value) ?? labels[0];
}

function formatPercent(value) {
  return `${(value * 100).toFixed(1)}%`;
}

function renderAnnotations() {
  boxLayer.innerHTML = "";
  annotationList.innerHTML = "";

  if (!annotations.length) {
    const empty = document.createElement("div");
    empty.className = "annotation-item";
    empty.innerHTML = `
      <div class="annotation-meta">
        No annotations yet. Select a violation and draw a box on the image.
      </div>
    `;
    annotationList.appendChild(empty);
  }

  annotations.forEach((annotation, index) => {
    const box = document.createElement("div");
    box.className = "annotation-box";
    if (editingIndex === index) {
      box.classList.add("active");
    }
    box.style.left = formatPercent(annotation.x);
    box.style.top = formatPercent(annotation.y);
    box.style.width = formatPercent(annotation.width);
    box.style.height = formatPercent(annotation.height);
    box.style.setProperty("--box-color", annotation.color);
    box.dataset.index = String(index);

    const label = document.createElement("div");
    label.className = "annotation-label";
    label.style.setProperty("--box-color", annotation.color);
    label.textContent = annotation.label;
    box.appendChild(label);
    boxLayer.appendChild(box);

    const item = document.createElement("div");
    item.className = "annotation-item";
    if (editingIndex === index) {
      item.classList.add("active");
    }
    item.dataset.index = String(index);
    item.innerHTML = `
      <div class="annotation-item-header">
        <div class="annotation-chip" style="--chip-color:${annotation.color}">
          <span class="chip-dot"></span>
          ${annotation.label}
        </div>
        <button class="annotation-delete" data-index="${index}">Delete</button>
      </div>
    `;
    annotationList.appendChild(item);
  });

  if (pendingAnnotation) {
    const box = document.createElement("div");
    box.className = "annotation-box pending";
    box.style.left = formatPercent(pendingAnnotation.x);
    box.style.top = formatPercent(pendingAnnotation.y);
    box.style.width = formatPercent(pendingAnnotation.width);
    box.style.height = formatPercent(pendingAnnotation.height);

    const label = document.createElement("div");
    label.className = "annotation-label";
    label.style.setProperty("--box-color", "#111827");
    label.textContent = "Pending Region";
    box.appendChild(label);
    boxLayer.appendChild(box);
  }
}

function buildExportPayload() {
  return {
    parcel_name: parcelNameInput.value.trim() || "Unspecified parcel",
    image_name: currentImageName || "unloaded-image",
    role: roleSelect.value,
    annotation_count: annotations.length,
    annotations: annotations.map((annotation) => ({
      label: annotation.label,
      value: annotation.value,
      x: Number(annotation.x.toFixed(4)),
      y: Number(annotation.y.toFixed(4)),
      width: Number(annotation.width.toFixed(4)),
      height: Number(annotation.height.toFixed(4))
    }))
  };
}

function exportJson() {
  jsonOutput.value = JSON.stringify(buildExportPayload(), null, 2);
}

function renderPendingPanel() {
  if (!pendingAnnotation) {
    pendingBoxPanel.classList.add("hidden");
    pendingBoxText.textContent = "Draw a box on the image to assign a violation.";
    return;
  }

  pendingBoxPanel.classList.remove("hidden");
  pendingBoxText.textContent =
    `Region selected: x=${pendingAnnotation.x.toFixed(3)}, y=${pendingAnnotation.y.toFixed(3)}, ` +
    `w=${pendingAnnotation.width.toFixed(3)}, h=${pendingAnnotation.height.toFixed(3)}. ` +
    `Choose a violation and click Save Tag.`;
}

function renderEditPanel() {
  if (editingIndex === null || !annotations[editingIndex]) {
    editBoxPanel.classList.add("hidden");
    editBoxText.textContent = "Select a saved annotation to update its violation label.";
    return;
  }

  const annotation = annotations[editingIndex];
  editBoxPanel.classList.remove("hidden");
  editBoxText.textContent =
    `Editing saved tag: ${annotation.label}. Choose a new violation from the dropdown, then click Update Label.`;
}

function updateModeButtons() {
  tagModeButton.classList.toggle("active", viewMode === "tag");
  panModeButton.classList.toggle("active", viewMode === "pan");
  tagModeButton.classList.toggle("secondary", viewMode !== "tag");
  panModeButton.classList.toggle("secondary", viewMode !== "pan");
  imageStage.classList.toggle("tag-mode", viewMode === "tag");
  imageStage.classList.toggle("pan-mode", viewMode === "pan");
}

function applyViewTransform() {
  zoomSurface.style.transform = `translate(${panX}px, ${panY}px) scale(${zoomLevel})`;
  zoomValue.textContent = `${Math.round(zoomLevel * 100)}%`;
}

function resetView() {
  zoomLevel = 1;
  panX = 0;
  panY = 0;
  panState = null;
  imageStage.classList.remove("panning");
  applyViewTransform();
}

function setViewMode(mode) {
  viewMode = mode;
  panState = null;
  imageStage.classList.remove("panning");
  updateModeButtons();
}

function adjustZoom(delta) {
  zoomLevel = clamp(Number((zoomLevel + delta).toFixed(2)), 0.5, 4);
  applyViewTransform();
}

function clearEditingState() {
  editingIndex = null;
  renderAnnotations();
  renderEditPanel();
}

function startEditing(index) {
  if (!annotations[index]) return;
  editingIndex = index;
  labelSelect.value = annotations[index].value;
  statusText.textContent = "Editing saved tag. Choose a new violation label and click Update Label.";
  renderAnnotations();
  renderEditPanel();
}

function clamp(value, min, max) {
  return Math.min(Math.max(value, min), max);
}

function getRelativePoint(event) {
  const rect = zoomSurface.getBoundingClientRect();
  const x = clamp((event.clientX - rect.left) / rect.width, 0, 1);
  const y = clamp((event.clientY - rect.top) / rect.height, 0, 1);
  return { x, y };
}

function setStageLoaded(name) {
  currentImageName = name;
  pendingAnnotation = null;
  editingIndex = null;
  imageStage.classList.remove("empty");
  resetView();
  emptyState.style.display = "none";
  workspaceTitle.textContent = parcelNameInput.value.trim() || "Selected Parcel";
  statusText.textContent = "Draw a region first, then assign a violation and save it.";
  renderAnnotations();
  renderPendingPanel();
  renderEditPanel();
  exportJson();
}

function resetStage(message = "No image selected") {
  annotations = [];
  currentImageName = "";
  pendingAnnotation = null;
  editingIndex = null;
  targetImage.removeAttribute("src");
  imageStage.classList.add("empty");
  resetView();
  emptyState.style.display = "grid";
  emptyState.innerHTML = `<p>${message}</p>`;
  workspaceTitle.textContent = "No image loaded";
  statusText.textContent = "Upload an image or load the demo image to begin.";
  renderAnnotations();
  renderPendingPanel();
  renderEditPanel();
  exportJson();
}

function loadImage(source, name) {
  annotations = [];
  targetImage.onload = () => {
    setStageLoaded(name);
  };
  targetImage.onerror = () => {
    resetStage("This image format could not be displayed here. Try JPG or PNG.");
    statusText.textContent =
      "The selected file could not be rendered in the browser. HEIC may not be supported.";
  };
  targetImage.src = source;
}

function createTempBox() {
  const box = document.createElement("div");
  box.className = "annotation-box";
  const label = document.createElement("div");
  label.className = "annotation-label";
  label.textContent = "Drawing";
  box.style.setProperty("--box-color", "#111827");
  label.style.setProperty("--box-color", "#111827");
  box.appendChild(label);
  boxLayer.appendChild(box);
  return box;
}

function updateTempBox(box, start, end) {
  const left = Math.min(start.x, end.x);
  const top = Math.min(start.y, end.y);
  const width = Math.abs(start.x - end.x);
  const height = Math.abs(start.y - end.y);

  box.style.left = formatPercent(left);
  box.style.top = formatPercent(top);
  box.style.width = formatPercent(width);
  box.style.height = formatPercent(height);
}

imageStage.addEventListener("pointerdown", (event) => {
  if (imageStage.classList.contains("empty")) return;
  if (event.target.closest(".annotation-box")) return;

  if (viewMode === "pan" || isSpacePressed) {
    panState = {
      startClientX: event.clientX,
      startClientY: event.clientY,
      startPanX: panX,
      startPanY: panY
    };
    imageStage.classList.add("panning");
    return;
  }

  const start = getRelativePoint(event);
  const tempBox = createTempBox();
  drawState = { start, tempBox };
  updateTempBox(tempBox, start, start);
});

imageStage.addEventListener("pointermove", (event) => {
  if (panState) {
    panX = panState.startPanX + (event.clientX - panState.startClientX);
    panY = panState.startPanY + (event.clientY - panState.startClientY);
    applyViewTransform();
    return;
  }

  if (!drawState) return;
  const current = getRelativePoint(event);
  updateTempBox(drawState.tempBox, drawState.start, current);
});

function commitDraw(event) {
  if (!drawState) return;

  const end = getRelativePoint(event);
  const left = Math.min(drawState.start.x, end.x);
  const top = Math.min(drawState.start.y, end.y);
  const width = Math.abs(drawState.start.x - end.x);
  const height = Math.abs(drawState.start.y - end.y);

  drawState.tempBox.remove();

  if (width > 0.015 && height > 0.015) {
    editingIndex = null;
    pendingAnnotation = {
      x: left,
      y: top,
      width,
      height
    };
    statusText.textContent = "Region selected. Choose a violation, then click Save Tag.";
  }

  drawState = null;
  renderAnnotations();
  renderPendingPanel();
  renderEditPanel();
  exportJson();
}

function stopPan() {
  panState = null;
  imageStage.classList.remove("panning");
}

imageStage.addEventListener("pointerup", (event) => {
  if (panState) {
    stopPan();
    return;
  }
  commitDraw(event);
});

imageStage.addEventListener("pointerleave", (event) => {
  if (panState) {
    stopPan();
    return;
  }
  if (drawState) {
    commitDraw(event);
  }
});

imageStage.addEventListener(
  "wheel",
  (event) => {
    if (imageStage.classList.contains("empty")) return;
    event.preventDefault();
    adjustZoom(event.deltaY < 0 ? 0.1 : -0.1);
  },
  { passive: false }
);

window.addEventListener("keydown", (event) => {
  if (event.code === "Space") {
    isSpacePressed = true;
    if (viewMode !== "pan" && !imageStage.classList.contains("empty")) {
      imageStage.classList.add("pan-mode");
    }
    event.preventDefault();
  }
});

window.addEventListener("keyup", (event) => {
  if (event.code === "Space") {
    isSpacePressed = false;
    imageStage.classList.remove("panning");
    if (viewMode !== "pan") {
      imageStage.classList.remove("pan-mode");
      imageStage.classList.add("tag-mode");
    }
    event.preventDefault();
  }
});

annotationList.addEventListener("click", (event) => {
  const button = event.target.closest(".annotation-delete");
  if (!button) return;

  const index = Number(button.dataset.index);
  annotations.splice(index, 1);
  if (editingIndex === index) {
    editingIndex = null;
  } else if (editingIndex !== null && editingIndex > index) {
    editingIndex -= 1;
  }
  renderAnnotations();
  renderEditPanel();
  exportJson();
});

boxLayer.addEventListener("click", (event) => {
  const box = event.target.closest(".annotation-box");
  if (!box || box.classList.contains("pending")) return;
  const index = Number(box.dataset.index);
  startEditing(index);
});

annotationList.addEventListener("click", (event) => {
  if (event.target.closest(".annotation-delete")) return;
  const item = event.target.closest(".annotation-item");
  if (!item || !item.dataset.index) return;
  const index = Number(item.dataset.index);
  startEditing(index);
});

roleSelect.addEventListener("change", () => {
  populateLabels();
});

tagModeButton.addEventListener("click", () => {
  setViewMode("tag");
  statusText.textContent = "Tag mode enabled. Draw a region first, then assign a violation and save it.";
});

panModeButton.addEventListener("click", () => {
  setViewMode("pan");
  statusText.textContent = "Pan mode enabled. Drag the image to move around. Use wheel or zoom buttons to zoom.";
});

zoomInButton.addEventListener("click", () => {
  if (imageStage.classList.contains("empty")) return;
  adjustZoom(0.1);
});

zoomOutButton.addEventListener("click", () => {
  if (imageStage.classList.contains("empty")) return;
  adjustZoom(-0.1);
});

resetViewButton.addEventListener("click", () => {
  if (imageStage.classList.contains("empty")) return;
  resetView();
  statusText.textContent = "View reset.";
});

imageUpload.addEventListener("change", (event) => {
  const file = event.target.files?.[0];
  if (!file) return;

  const allowedTypes = ["image/jpeg", "image/png"];
  const lowerName = file.name.toLowerCase();
  const allowedByName =
    lowerName.endsWith(".jpg") ||
    lowerName.endsWith(".jpeg") ||
    lowerName.endsWith(".png");

  if (!allowedTypes.includes(file.type) && !allowedByName) {
    resetStage("This demo currently supports JPG and PNG files only.");
    statusText.textContent =
      "HEIC support is not enabled in this prototype yet. Please use JPG or PNG.";
    imageUpload.value = "";
    return;
  }

  resetStage("Loading image...");
  statusText.textContent = `Trying to load ${file.name}`;

  const reader = new FileReader();
  reader.onload = () => {
    loadImage(reader.result, file.name);
  };
  reader.readAsDataURL(file);
});

parcelNameInput.addEventListener("input", () => {
  if (!imageStage.classList.contains("empty")) {
    workspaceTitle.textContent = parcelNameInput.value.trim() || "Selected Parcel";
    exportJson();
  }
});

document.getElementById("clearAnnotations").addEventListener("click", () => {
  if (imageStage.classList.contains("empty")) {
    return;
  }
  annotations = [];
  pendingAnnotation = null;
  editingIndex = null;
  renderAnnotations();
  renderPendingPanel();
  renderEditPanel();
  exportJson();
});

document.getElementById("exportJson").addEventListener("click", () => {
  exportJson();
});

document.getElementById("loadDemoImage").addEventListener("click", () => {
  if (!parcelNameInput.value.trim()) {
    parcelNameInput.value = "13 Donaldson, Buffalo, NY 14208";
  }
  loadImage(DEMO_IMAGE, "demo-property-image.svg");
});

savePendingTagButton.addEventListener("click", () => {
  if (!pendingAnnotation) return;

  const selected = getSelectedLabel();
  annotations.push({
    label: selected.label,
    value: selected.value,
    color: selected.color,
    x: pendingAnnotation.x,
    y: pendingAnnotation.y,
    width: pendingAnnotation.width,
    height: pendingAnnotation.height
  });

  pendingAnnotation = null;
  editingIndex = null;
  statusText.textContent = "Tag saved. Draw another region to add more violations.";
  renderAnnotations();
  renderPendingPanel();
  renderEditPanel();
  exportJson();
});

discardPendingTagButton.addEventListener("click", () => {
  pendingAnnotation = null;
  statusText.textContent = "Pending region discarded. Draw a new region to continue.";
  renderAnnotations();
  renderPendingPanel();
  renderEditPanel();
  exportJson();
});

saveEditedTagButton.addEventListener("click", () => {
  if (editingIndex === null || !annotations[editingIndex]) return;

  const selected = getSelectedLabel();
  annotations[editingIndex] = {
    ...annotations[editingIndex],
    label: selected.label,
    value: selected.value,
    color: selected.color
  };

  statusText.textContent = "Saved annotation updated.";
  clearEditingState();
  exportJson();
});

cancelEditTagButton.addEventListener("click", () => {
  statusText.textContent = "Edit cancelled.";
  clearEditingState();
});

populateLabels();
renderAnnotations();
renderPendingPanel();
renderEditPanel();
updateModeButtons();
applyViewTransform();
