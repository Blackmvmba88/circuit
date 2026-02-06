/**
 * Circuit Dashboard - Main application logic
 * Handles file loading, UI updates, and dashboard state management
 */

class CircuitDashboard {
  constructor() {
    this.circuit = null;
    this.renderer = null;
    this.consoleLines = [];
    this.maxConsoleLines = 100;
    
    this.init();
  }
  
  init() {
    // Initialize UI elements
    this.initElements();
    
    // Initialize circuit renderer
    this.initRenderer();
    
    // Setup event listeners
    this.setupEventListeners();
    
    // Log startup
    this.log('System initialized', 'success');
    this.log('Ready to load circuit files', 'info');
  }
  
  initElements() {
    // File input
    this.fileInput = document.getElementById('fileInput');
    this.dropZone = document.getElementById('dropZone');
    
    // Metrics
    this.metricComponents = document.getElementById('metricComponents');
    this.metricNets = document.getElementById('metricNets');
    this.metricDimensions = document.getElementById('metricDimensions');
    this.metricPower = document.getElementById('metricPower');
    
    // Console
    this.consoleContent = document.getElementById('consoleContent');
    this.consoleClear = document.getElementById('consoleClear');
    
    // Canvas
    this.canvas = document.getElementById('circuitCanvas');
    
    // Component list
    this.componentListContainer = document.getElementById('componentList');
    
    // Circuit info
    this.circuitName = document.getElementById('circuitName');
    this.circuitDescription = document.getElementById('circuitDescription');
  }
  
  initRenderer() {
    if (this.canvas) {
      this.renderer = new CircuitRenderer(this.canvas);
      
      // Listen for component selection
      this.canvas.addEventListener('componentSelected', (e) => {
        this.showComponentDetails(e.detail);
      });
    }
  }
  
  setupEventListeners() {
    // File input
    if (this.fileInput) {
      this.fileInput.addEventListener('change', (e) => this.handleFileSelect(e));
    }
    
    // Drop zone
    if (this.dropZone) {
      this.dropZone.addEventListener('click', () => this.fileInput.click());
      this.dropZone.addEventListener('dragover', (e) => this.handleDragOver(e));
      this.dropZone.addEventListener('dragleave', (e) => this.handleDragLeave(e));
      this.dropZone.addEventListener('drop', (e) => this.handleDrop(e));
    }
    
    // Console clear button
    if (this.consoleClear) {
      this.consoleClear.addEventListener('click', () => this.clearConsole());
    }
    
    // Reset view button
    const resetViewBtn = document.getElementById('resetView');
    if (resetViewBtn) {
      resetViewBtn.addEventListener('click', () => this.resetView());
    }
    
    // Export image button
    const exportBtn = document.getElementById('exportImage');
    if (exportBtn) {
      exportBtn.addEventListener('click', () => this.exportImage());
    }
    
    // Fit to view button
    const fitViewBtn = document.getElementById('fitView');
    if (fitViewBtn) {
      fitViewBtn.addEventListener('click', () => this.fitToView());
    }
  }
  
  // ==================== File Handling ====================
  
  handleFileSelect(event) {
    const file = event.target.files[0];
    if (file) {
      this.loadCircuitFile(file);
    }
  }
  
  handleDragOver(event) {
    event.preventDefault();
    event.stopPropagation();
    this.dropZone.classList.add('dragover');
  }
  
  handleDragLeave(event) {
    event.preventDefault();
    event.stopPropagation();
    this.dropZone.classList.remove('dragover');
  }
  
  handleDrop(event) {
    event.preventDefault();
    event.stopPropagation();
    this.dropZone.classList.remove('dragover');
    
    const file = event.dataTransfer.files[0];
    if (file) {
      this.loadCircuitFile(file);
    }
  }
  
  loadCircuitFile(file) {
    // Check file extension
    if (!file.name.endsWith('.circuit.json') && !file.name.endsWith('.json')) {
      this.log(`Invalid file type: ${file.name}`, 'error');
      this.showError('Please select a .circuit.json file');
      return;
    }
    
    this.log(`Loading file: ${file.name}`, 'info');
    
    const reader = new FileReader();
    
    reader.onload = (e) => {
      try {
        const data = JSON.parse(e.target.result);
        this.loadCircuit(data, file.name);
      } catch (error) {
        this.log(`Failed to parse JSON: ${error.message}`, 'error');
        this.showError('Invalid JSON file');
      }
    };
    
    reader.onerror = () => {
      this.log('Failed to read file', 'error');
      this.showError('Failed to read file');
    };
    
    reader.readAsText(file);
  }
  
  // ==================== Circuit Loading ====================
  
  loadCircuit(data, filename = 'circuit.json') {
    // Validate circuit data
    const validation = CircuitUtils.validateCircuit(data);
    
    if (!validation.valid) {
      this.log('Circuit validation failed:', 'error');
      validation.errors.forEach(error => {
        this.log(`  - ${error}`, 'error');
      });
      this.showError('Invalid circuit format');
      return;
    }
    
    this.circuit = data;
    
    this.log(`Loaded circuit: ${filename}`, 'success');
    this.log(`Components: ${data.components.length}`, 'info');
    
    // Update UI
    this.updateCircuitInfo();
    this.updateMetrics();
    this.updateComponentList();
    
    // Load into renderer
    if (this.renderer) {
      this.renderer.loadCircuit(data);
      this.log('Circuit rendered successfully', 'success');
    }
    
    // Hide drop zone, show viewport
    if (this.dropZone) {
      this.dropZone.style.display = 'none';
    }
  }
  
  // ==================== UI Updates ====================
  
  updateCircuitInfo() {
    if (!this.circuit) return;
    
    const metadata = this.circuit.metadata || {};
    
    if (this.circuitName) {
      this.circuitName.textContent = metadata.name || 'Unnamed Circuit';
      CircuitUtils.fadeIn(this.circuitName);
    }
    
    if (this.circuitDescription) {
      this.circuitDescription.textContent = metadata.description || 'No description available';
      CircuitUtils.fadeIn(this.circuitDescription);
    }
  }
  
  updateMetrics() {
    if (!this.circuit) return;
    
    // Component count
    const componentCount = this.circuit.components.length;
    if (this.metricComponents) {
      CircuitUtils.animateCounter(this.metricComponents, 0, componentCount, 1000);
    }
    
    // Net count
    let netCount = 0;
    if (this.circuit.nets) {
      netCount = this.circuit.nets.length;
    } else if (this.circuit.connections) {
      netCount = this.circuit.connections.length;
    }
    
    if (this.metricNets) {
      CircuitUtils.animateCounter(this.metricNets, 0, netCount, 1000);
    }
    
    // Board dimensions
    if (this.metricDimensions && this.circuit.board && this.circuit.board.dimensions) {
      const dims = this.circuit.board.dimensions;
      const dimText = `${dims.width || 0}×${dims.height || 0}`;
      this.metricDimensions.textContent = dimText;
      CircuitUtils.fadeIn(this.metricDimensions.parentElement);
    } else if (this.metricDimensions) {
      this.metricDimensions.textContent = 'N/A';
    }
    
    // Power estimation
    if (this.metricPower) {
      const power = this.estimatePower();
      if (power > 0) {
        this.metricPower.textContent = power.toFixed(2);
        CircuitUtils.fadeIn(this.metricPower.parentElement);
      } else {
        this.metricPower.textContent = 'N/A';
      }
    }
  }
  
  updateComponentList() {
    if (!this.componentListContainer || !this.circuit) return;
    
    CircuitUtils.clearElement(this.componentListContainer);
    
    this.circuit.components.forEach((component, index) => {
      const item = this.createComponentListItem(component);
      
      // Stagger animations
      setTimeout(() => {
        this.componentListContainer.appendChild(item);
        CircuitUtils.slideInUp(item);
      }, index * 50);
    });
  }
  
  createComponentListItem(component) {
    const item = document.createElement('div');
    item.className = 'component-item';
    item.dataset.componentId = component.id;
    
    const info = document.createElement('div');
    info.className = 'component-info';
    
    const id = document.createElement('div');
    id.className = 'component-id';
    id.textContent = component.id;
    
    const type = document.createElement('div');
    type.className = 'component-type';
    type.textContent = component.type;
    
    const value = document.createElement('div');
    value.className = 'component-value';
    value.textContent = component.value || component.description || '';
    
    info.appendChild(id);
    info.appendChild(type);
    if (component.value || component.description) {
      info.appendChild(value);
    }
    
    const symbol = document.createElement('div');
    symbol.textContent = CircuitUtils.getComponentSymbol(component.type);
    symbol.style.fontSize = '1.5rem';
    symbol.style.color = CircuitUtils.getComponentColor(component.type);
    
    item.appendChild(info);
    item.appendChild(symbol);
    
    // Click to highlight in renderer
    item.addEventListener('click', () => {
      if (this.renderer) {
        this.renderer.selectedComponent = component.id;
        this.renderer.centerOn(component.id);
        this.renderer.render();
      }
      this.showComponentDetails(component);
    });
    
    return item;
  }
  
  showComponentDetails(component) {
    this.log(`Selected: ${component.id} (${component.type})`, 'info');
    
    // Could expand this to show a detail panel
    if (component.value) {
      this.log(`  Value: ${component.value}`, 'info');
    }
    if (component.params) {
      Object.entries(component.params).forEach(([key, value]) => {
        this.log(`  ${key}: ${value}`, 'info');
      });
    }
  }
  
  // ==================== Metrics Calculation ====================
  
  estimatePower() {
    if (!this.circuit || !this.circuit.properties) return 0;
    
    // Try to get power from properties
    if (this.circuit.properties.power_consumption) {
      const powerStr = this.circuit.properties.power_consumption.toString();
      const match = powerStr.match(/(\d+\.?\d*)/);
      if (match) {
        // Convert to watts
        if (powerStr.includes('mW')) {
          return parseFloat(match[1]) / 1000;
        }
        return parseFloat(match[1]);
      }
    }
    
    // Estimate from components
    let totalPower = 0;
    this.circuit.components.forEach(component => {
      if (component.params && component.params.power_rating_w) {
        totalPower += component.params.power_rating_w * 0.5; // Assume 50% usage
      }
    });
    
    return totalPower;
  }
  
  // ==================== Console Functions ====================
  
  log(message, type = 'info') {
    const timestamp = CircuitUtils.formatTime();
    const line = { timestamp, type, message };
    
    this.consoleLines.push(line);
    
    // Limit console lines
    if (this.consoleLines.length > this.maxConsoleLines) {
      this.consoleLines.shift();
    }
    
    // Add to DOM
    if (this.consoleContent) {
      const lineElement = this.createConsoleLine(line);
      this.consoleContent.appendChild(lineElement);
      
      // Auto-scroll to bottom
      if (this.consoleContent.parentElement) {
        this.consoleContent.parentElement.scrollTop = this.consoleContent.parentElement.scrollHeight;
      }
    }
  }
  
  createConsoleLine(line) {
    const element = document.createElement('div');
    element.className = `console-line ${line.type}`;
    
    const timestamp = document.createElement('span');
    timestamp.className = 'console-timestamp';
    timestamp.textContent = line.timestamp;
    
    const prefix = document.createElement('span');
    prefix.className = 'console-prefix';
    prefix.textContent = '>';
    
    const message = document.createElement('span');
    message.className = 'console-message';
    message.textContent = line.message;
    
    element.appendChild(timestamp);
    element.appendChild(prefix);
    element.appendChild(message);
    
    return element;
  }
  
  clearConsole() {
    this.consoleLines = [];
    if (this.consoleContent) {
      CircuitUtils.clearElement(this.consoleContent);
    }
    this.log('Console cleared', 'info');
  }
  
  // ==================== View Controls ====================
  
  resetView() {
    if (this.renderer) {
      this.renderer.reset();
      if (this.circuit) {
        this.renderer.loadCircuit(this.circuit);
      }
      this.log('View reset', 'info');
    }
  }
  
  fitToView() {
    if (this.renderer && this.circuit) {
      this.renderer.fitToView();
      this.renderer.render();
      this.log('Fitted to view', 'info');
    }
  }
  
  exportImage() {
    if (this.renderer && this.circuit) {
      const dataUrl = this.renderer.exportImage();
      
      // Create download link
      const link = document.createElement('a');
      link.download = `${this.circuit.metadata.name || 'circuit'}.png`;
      link.href = dataUrl;
      link.click();
      
      this.log('Image exported', 'success');
    }
  }
  
  // ==================== Error Handling ====================
  
  showError(message) {
    // Could show a modal or toast notification
    if (this.dropZone) {
      CircuitUtils.glitchEffect(this.dropZone);
    }
  }
}

// Initialize dashboard when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
  window.dashboard = new CircuitDashboard();
});
