/**
 * Circuit Renderer - 2D Canvas-based circuit visualization
 * Renders electronic components and connections with cyberpunk styling
 */

class CircuitRenderer {
  constructor(canvas) {
    this.canvas = canvas;
    this.ctx = canvas.getContext('2d');
    this.circuit = null;
    
    // View state
    this.offsetX = 0;
    this.offsetY = 0;
    this.scale = 1;
    this.minScale = 0.1;
    this.maxScale = 3;
    
    // Component layout
    this.componentPositions = new Map();
    this.hoveredComponent = null;
    this.selectedComponent = null;
    
    // Colors (cyberpunk theme)
    this.colors = {
      background: '#0a0a0f',
      grid: 'rgba(0, 255, 249, 0.1)',
      component: {
        resistor: '#ff006e',
        capacitor: '#00fff9',
        inductor: '#8338ec',
        diode: '#ffd700',
        led: '#39ff14',
        transistor: '#ff006e',
        ic: '#00fff9',
        connector: '#a0a0a0',
        power_supply: '#39ff14',
        ground: '#606060',
        voltage_regulator: '#00fff9',
        default: '#e0e0e0'
      },
      connection: 'rgba(0, 255, 249, 0.6)',
      connectionHover: '#00fff9',
      text: '#e0e0e0',
      textDim: '#606060',
      highlight: '#ff006e'
    };
    
    // Mouse interaction
    this.isDragging = false;
    this.lastMouseX = 0;
    this.lastMouseY = 0;
    
    this.setupEventListeners();
    this.resizeCanvas();
    
    // Handle window resize
    window.addEventListener('resize', () => this.resizeCanvas());
  }
  
  setupEventListeners() {
    // Mouse events for pan and zoom
    this.canvas.addEventListener('mousedown', (e) => this.handleMouseDown(e));
    this.canvas.addEventListener('mousemove', (e) => this.handleMouseMove(e));
    this.canvas.addEventListener('mouseup', () => this.handleMouseUp());
    this.canvas.addEventListener('wheel', (e) => this.handleWheel(e));
    this.canvas.addEventListener('mouseleave', () => this.handleMouseUp());
    
    // Click for component selection
    this.canvas.addEventListener('click', (e) => this.handleClick(e));
  }
  
  resizeCanvas() {
    const rect = this.canvas.getBoundingClientRect();
    this.canvas.width = rect.width;
    this.canvas.height = rect.height;
    this.render();
  }
  
  // ==================== Data Loading ====================
  
  loadCircuit(circuitData) {
    this.circuit = circuitData;
    this.calculateLayout();
    this.fitToView();
    this.render();
  }
  
  calculateLayout() {
    if (!this.circuit || !this.circuit.components) return;
    
    const components = this.circuit.components;
    const gridSize = 100;
    const cols = Math.ceil(Math.sqrt(components.length));
    
    components.forEach((component, index) => {
      const col = index % cols;
      const row = Math.floor(index / cols);
      
      this.componentPositions.set(component.id, {
        x: col * gridSize + 50,
        y: row * gridSize + 50,
        width: 60,
        height: 40
      });
    });
  }
  
  fitToView() {
    if (this.componentPositions.size === 0) return;
    
    let minX = Infinity, minY = Infinity;
    let maxX = -Infinity, maxY = -Infinity;
    
    this.componentPositions.forEach(pos => {
      minX = Math.min(minX, pos.x);
      minY = Math.min(minY, pos.y);
      maxX = Math.max(maxX, pos.x + pos.width);
      maxY = Math.max(maxY, pos.y + pos.height);
    });
    
    const width = maxX - minX;
    const height = maxY - minY;
    const padding = 50;
    
    const scaleX = (this.canvas.width - padding * 2) / width;
    const scaleY = (this.canvas.height - padding * 2) / height;
    this.scale = Math.min(scaleX, scaleY, 1);
    
    this.offsetX = (this.canvas.width - width * this.scale) / 2 - minX * this.scale;
    this.offsetY = (this.canvas.height - height * this.scale) / 2 - minY * this.scale;
  }
  
  // ==================== Mouse Interaction ====================
  
  handleMouseDown(e) {
    this.isDragging = true;
    this.lastMouseX = e.clientX;
    this.lastMouseY = e.clientY;
    this.canvas.style.cursor = 'grabbing';
  }
  
  handleMouseMove(e) {
    if (this.isDragging) {
      const dx = e.clientX - this.lastMouseX;
      const dy = e.clientY - this.lastMouseY;
      
      this.offsetX += dx;
      this.offsetY += dy;
      
      this.lastMouseX = e.clientX;
      this.lastMouseY = e.clientY;
      
      this.render();
    } else {
      // Check for hover
      const rect = this.canvas.getBoundingClientRect();
      const mouseX = (e.clientX - rect.left - this.offsetX) / this.scale;
      const mouseY = (e.clientY - rect.top - this.offsetY) / this.scale;
      
      let foundHover = false;
      this.componentPositions.forEach((pos, id) => {
        if (mouseX >= pos.x && mouseX <= pos.x + pos.width &&
            mouseY >= pos.y && mouseY <= pos.y + pos.height) {
          this.hoveredComponent = id;
          foundHover = true;
          this.canvas.style.cursor = 'pointer';
        }
      });
      
      if (!foundHover && this.hoveredComponent) {
        this.hoveredComponent = null;
        this.canvas.style.cursor = 'crosshair';
        this.render();
      } else if (foundHover) {
        this.render();
      }
    }
  }
  
  handleMouseUp() {
    this.isDragging = false;
    this.canvas.style.cursor = 'crosshair';
  }
  
  handleWheel(e) {
    e.preventDefault();
    
    const rect = this.canvas.getBoundingClientRect();
    const mouseX = e.clientX - rect.left;
    const mouseY = e.clientY - rect.top;
    
    const zoomFactor = e.deltaY > 0 ? 0.9 : 1.1;
    const newScale = this.scale * zoomFactor;
    
    if (newScale >= this.minScale && newScale <= this.maxScale) {
      // Zoom towards mouse position
      this.offsetX = mouseX - (mouseX - this.offsetX) * zoomFactor;
      this.offsetY = mouseY - (mouseY - this.offsetY) * zoomFactor;
      this.scale = newScale;
      
      this.render();
    }
  }
  
  handleClick(e) {
    if (!this.hoveredComponent) {
      this.selectedComponent = null;
    } else {
      this.selectedComponent = this.hoveredComponent;
      
      // Dispatch event for component selection
      const component = this.circuit.components.find(c => c.id === this.selectedComponent);
      if (component) {
        const event = new CustomEvent('componentSelected', {
          detail: component
        });
        this.canvas.dispatchEvent(event);
      }
    }
    this.render();
  }
  
  // ==================== Rendering ====================
  
  render() {
    // Clear canvas
    this.ctx.fillStyle = this.colors.background;
    this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
    
    // Draw grid
    this.drawGrid();
    
    // Apply transformations
    this.ctx.save();
    this.ctx.translate(this.offsetX, this.offsetY);
    this.ctx.scale(this.scale, this.scale);
    
    // Draw connections
    this.drawConnections();
    
    // Draw components
    this.drawComponents();
    
    this.ctx.restore();
    
    // Draw UI elements (not affected by zoom/pan)
    this.drawUI();
  }
  
  drawGrid() {
    this.ctx.strokeStyle = this.colors.grid;
    this.ctx.lineWidth = 1;
    
    const gridSize = 50;
    const startX = Math.floor((-this.offsetX / this.scale) / gridSize) * gridSize;
    const startY = Math.floor((-this.offsetY / this.scale) / gridSize) * gridSize;
    const endX = startX + (this.canvas.width / this.scale) + gridSize;
    const endY = startY + (this.canvas.height / this.scale) + gridSize;
    
    this.ctx.save();
    this.ctx.translate(this.offsetX, this.offsetY);
    this.ctx.scale(this.scale, this.scale);
    
    // Vertical lines
    for (let x = startX; x <= endX; x += gridSize) {
      this.ctx.beginPath();
      this.ctx.moveTo(x, startY);
      this.ctx.lineTo(x, endY);
      this.ctx.stroke();
    }
    
    // Horizontal lines
    for (let y = startY; y <= endY; y += gridSize) {
      this.ctx.beginPath();
      this.ctx.moveTo(startX, y);
      this.ctx.lineTo(endX, y);
      this.ctx.stroke();
    }
    
    this.ctx.restore();
  }
  
  drawComponents() {
    if (!this.circuit || !this.circuit.components) return;
    
    this.circuit.components.forEach(component => {
      const pos = this.componentPositions.get(component.id);
      if (!pos) return;
      
      const isHovered = this.hoveredComponent === component.id;
      const isSelected = this.selectedComponent === component.id;
      
      this.drawComponent(component, pos, isHovered, isSelected);
    });
  }
  
  drawComponent(component, pos, isHovered, isSelected) {
    const { x, y, width, height } = pos;
    
    // Get component color
    const color = this.colors.component[component.type] || this.colors.component.default;
    
    // Draw component box
    this.ctx.save();
    
    // Shadow/glow effect
    if (isHovered || isSelected) {
      this.ctx.shadowBlur = 20;
      this.ctx.shadowColor = color;
    }
    
    // Component border
    this.ctx.strokeStyle = color;
    this.ctx.lineWidth = isSelected ? 3 : 2;
    this.ctx.fillStyle = 'rgba(19, 19, 26, 0.9)';
    
    // Rounded rectangle
    this.roundRect(x, y, width, height, 5);
    this.ctx.fill();
    this.ctx.stroke();
    
    this.ctx.restore();
    
    // Draw component ID
    this.ctx.fillStyle = color;
    this.ctx.font = 'bold 12px "Fira Code", monospace';
    this.ctx.textAlign = 'center';
    this.ctx.textBaseline = 'middle';
    this.ctx.fillText(component.id, x + width / 2, y + height / 2 - 8);
    
    // Draw component type
    this.ctx.fillStyle = this.colors.textDim;
    this.ctx.font = '9px "Fira Code", monospace';
    this.ctx.fillText(component.type, x + width / 2, y + height / 2 + 6);
    
    // Draw value if exists
    if (component.value) {
      this.ctx.fillStyle = this.colors.text;
      this.ctx.font = '8px "Fira Code", monospace';
      this.ctx.fillText(component.value, x + width / 2, y + height + 12);
    }
  }
  
  drawConnections() {
    if (!this.circuit) return;
    
    // Draw connections from 'connections' array (legacy format)
    if (this.circuit.connections && Array.isArray(this.circuit.connections)) {
      this.circuit.connections.forEach(conn => {
        this.drawConnection(conn.from, conn.to);
      });
    }
    
    // Draw nets (modern format)
    if (this.circuit.nets && Array.isArray(this.circuit.nets)) {
      this.circuit.nets.forEach(net => {
        if (net.connections && net.connections.length > 1) {
          // Connect all pins in the net
          for (let i = 0; i < net.connections.length - 1; i++) {
            const from = `${net.connections[i].component}.${net.connections[i].pin}`;
            const to = `${net.connections[i + 1].component}.${net.connections[i + 1].pin}`;
            this.drawConnection(from, to, net.id);
          }
        }
      });
    }
  }
  
  drawConnection(from, to, netId = null) {
    const fromId = from.split('.')[0];
    const toId = to.split('.')[0];
    
    const fromPos = this.componentPositions.get(fromId);
    const toPos = this.componentPositions.get(toId);
    
    if (!fromPos || !toPos) return;
    
    const fromX = fromPos.x + fromPos.width / 2;
    const fromY = fromPos.y + fromPos.height / 2;
    const toX = toPos.x + toPos.width / 2;
    const toY = toPos.y + toPos.height / 2;
    
    this.ctx.save();
    
    // Line style
    this.ctx.strokeStyle = this.colors.connection;
    this.ctx.lineWidth = 2;
    this.ctx.setLineDash([5, 5]);
    
    // Glow effect
    this.ctx.shadowBlur = 10;
    this.ctx.shadowColor = 'rgba(0, 255, 249, 0.5)';
    
    // Draw line
    this.ctx.beginPath();
    this.ctx.moveTo(fromX, fromY);
    this.ctx.lineTo(toX, toY);
    this.ctx.stroke();
    
    this.ctx.restore();
    
    // Draw net label if provided
    if (netId) {
      const midX = (fromX + toX) / 2;
      const midY = (fromY + toY) / 2;
      
      this.ctx.fillStyle = 'rgba(0, 255, 249, 0.8)';
      this.ctx.font = '8px "Fira Code", monospace';
      this.ctx.textAlign = 'center';
      this.ctx.fillText(netId, midX, midY - 5);
    }
  }
  
  drawUI() {
    // Draw zoom level
    this.ctx.fillStyle = 'rgba(19, 19, 26, 0.9)';
    this.ctx.fillRect(10, this.canvas.height - 40, 100, 30);
    
    this.ctx.strokeStyle = this.colors.connection;
    this.ctx.lineWidth = 1;
    this.ctx.strokeRect(10, this.canvas.height - 40, 100, 30);
    
    this.ctx.fillStyle = this.colors.text;
    this.ctx.font = '12px "Fira Code", monospace';
    this.ctx.textAlign = 'left';
    this.ctx.textBaseline = 'middle';
    this.ctx.fillText(`Zoom: ${(this.scale * 100).toFixed(0)}%`, 20, this.canvas.height - 25);
    
    // Draw instructions if no circuit loaded
    if (!this.circuit) {
      this.ctx.fillStyle = this.colors.textDim;
      this.ctx.font = '16px "Fira Code", monospace';
      this.ctx.textAlign = 'center';
      this.ctx.textBaseline = 'middle';
      this.ctx.fillText('Load a circuit to visualize', this.canvas.width / 2, this.canvas.height / 2);
    }
  }
  
  // ==================== Helper Functions ====================
  
  roundRect(x, y, width, height, radius) {
    this.ctx.beginPath();
    this.ctx.moveTo(x + radius, y);
    this.ctx.lineTo(x + width - radius, y);
    this.ctx.quadraticCurveTo(x + width, y, x + width, y + radius);
    this.ctx.lineTo(x + width, y + height - radius);
    this.ctx.quadraticCurveTo(x + width, y + height, x + width - radius, y + height);
    this.ctx.lineTo(x + radius, y + height);
    this.ctx.quadraticCurveTo(x, y + height, x, y + height - radius);
    this.ctx.lineTo(x, y + radius);
    this.ctx.quadraticCurveTo(x, y, x + radius, y);
    this.ctx.closePath();
  }
  
  // ==================== Public API ====================
  
  reset() {
    this.offsetX = 0;
    this.offsetY = 0;
    this.scale = 1;
    this.hoveredComponent = null;
    this.selectedComponent = null;
    this.componentPositions.clear();
    this.render();
  }
  
  getSelectedComponent() {
    if (!this.selectedComponent || !this.circuit) return null;
    return this.circuit.components.find(c => c.id === this.selectedComponent);
  }
  
  centerOn(componentId) {
    const pos = this.componentPositions.get(componentId);
    if (!pos) return;
    
    this.offsetX = this.canvas.width / 2 - (pos.x + pos.width / 2) * this.scale;
    this.offsetY = this.canvas.height / 2 - (pos.y + pos.height / 2) * this.scale;
    this.render();
  }
  
  exportImage() {
    return this.canvas.toDataURL('image/png');
  }
}

// Export for use in other modules
if (typeof window !== 'undefined') {
  window.CircuitRenderer = CircuitRenderer;
}
