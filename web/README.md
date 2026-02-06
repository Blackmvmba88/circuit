# Circuit Web Tools

Interactive web-based tools for viewing and analyzing `.circuit.json` files.

## 🎨 Dashboard (Cyberpunk Edition) - **NEW!**

A visually stunning, cyberpunk-styled dashboard for viewing, analyzing, and managing electronic circuits. Features neon colors, glitch effects, animated backgrounds, and interactive 2D canvas visualization.

### Quick Start with Dashboard
Open `dashboard.html` in your browser and drag-and-drop a `.circuit.json` file!

### Dashboard Features
- **Cyberpunk Aesthetic**: Neon colors, glowing borders, animated grid background
- **Interactive Canvas**: Pan, zoom, and click components for details
- **Real-time Metrics**: Component counts, connections, power estimation
- **Component List**: Color-coded icons and searchable list
- **System Console**: Live logging with timestamps
- **Responsive Design**: Works on desktop, tablet, and mobile

See `dashboard.html` for the full cyberpunk experience!

---

## 📊 Original Visualizer

Simple, lightweight viewer for `.circuit.json` files (see `visualizer.html`).

## Features

- 🎯 **Drag & Drop** - Simply drop your circuit file to load it
- ✅ **Validation** - Basic circuit validation
- 📊 **Statistics** - Component counts, connections, and metadata
- 📋 **Component List** - View all components with details
- 📦 **BOM Export** - Export Bill of Materials as CSV
- 🎨 **Simple Visualization** - Basic schematic representation
- 💾 **Download** - Download edited circuit files

## Usage

### Option 1: Open Locally

Simply open `visualizer.html` in any modern web browser (Chrome, Firefox, Safari, Edge).

```bash
# From the project root
open web/visualizer.html
# or
firefox web/visualizer.html
```

### Option 2: Serve with Python

```bash
cd web
python3 -m http.server 8000
# Open http://localhost:8000/visualizer.html
```

### Option 3: Serve with Node.js

```bash
cd web
npx http-server -p 8000
# Open http://localhost:8000/visualizer.html
```

## Supported Features

### Current
- ✅ Load .circuit.json files
- ✅ Display circuit metadata
- ✅ Show component statistics
- ✅ List components
- ✅ Basic validation
- ✅ Export BOM as CSV
- ✅ Simple visualization

### Planned
- 🚧 Advanced 2D schematic rendering
- 🚧 Interactive component placement
- 🚧 3D PCB visualization (using Three.js)
- 🚧 Net highlighting
- 🚧 Design rule checking
- 🚧 Export to various formats
- 🚧 Circuit editing capabilities

## Browser Compatibility

- ✅ Chrome 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Edge 90+

## Development

The visualizer is a single HTML file with embedded CSS and JavaScript - no build step required!

To enhance the visualizer:

1. Edit `visualizer.html`
2. Refresh your browser
3. Test with example circuits from `../examples/`

## Examples to Try

Load these example circuits to test the visualizer:

- `../examples/simple_circuit.circuit.json` - Basic LED circuit
- `../examples/voltage_regulator_lm7805.circuit.json` - Linear regulator
- `../examples/h_bridge_motor_driver.circuit.json` - Motor driver
- `../examples/circuit_with_3d.circuit.json` - Circuit with 3D models

## Screenshots

*Coming soon - screenshots of the visualizer in action*

## Future Enhancements

### Advanced Visualization
- SVG-based schematic rendering
- Interactive node dragging
- Zoom and pan controls
- Component search and filter

### 3D Rendering
- Three.js integration for 3D PCB view
- Component 3D models
- Layer visualization
- Real-time rendering

### Editing
- Add/remove components
- Edit component properties
- Create connections
- Save changes back to JSON

### Analysis
- Netlist analysis
- BOM generation with pricing (integration with component APIs)
- Design rule checking
- Electrical calculations

## Contributing

Contributions welcome! Areas to improve:

- Better schematic rendering
- 3D visualization
- Circuit editing
- Mobile responsive design
- Dark/light theme toggle
- Export to image/PDF

## License

MIT License - same as the parent Circuit project.
