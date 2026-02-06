/**
 * Utility functions for the Circuit Dashboard
 * Includes animations, formatting, and helper functions
 */

// ==================== Formatting Functions ====================

/**
 * Format a timestamp for display
 * @param {Date} date - Date object to format
 * @returns {string} Formatted time string (HH:MM:SS)
 */
function formatTime(date = new Date()) {
  return date.toTimeString().split(' ')[0];
}

/**
 * Format a number with animation-friendly counter
 * @param {number} value - Number to format
 * @param {number} decimals - Number of decimal places
 * @returns {string} Formatted number
 */
function formatNumber(value, decimals = 0) {
  if (value === undefined || value === null) return '0';
  return Number(value).toFixed(decimals);
}

/**
 * Format byte size to human-readable format
 * @param {number} bytes - Size in bytes
 * @returns {string} Formatted size string
 */
function formatBytes(bytes) {
  if (bytes === 0) return '0 Bytes';
  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
}

// ==================== Animation Functions ====================

/**
 * Animate a counter from start to end value
 * @param {HTMLElement} element - Element to update
 * @param {number} start - Starting value
 * @param {number} end - Ending value
 * @param {number} duration - Animation duration in ms
 * @param {number} decimals - Number of decimal places
 */
function animateCounter(element, start, end, duration = 1000, decimals = 0) {
  const startTime = performance.now();
  const difference = end - start;
  
  function update(currentTime) {
    const elapsed = currentTime - startTime;
    const progress = Math.min(elapsed / duration, 1);
    
    // Easing function (easeOutExpo)
    const easedProgress = progress === 1 ? 1 : 1 - Math.pow(2, -10 * progress);
    const currentValue = start + (difference * easedProgress);
    
    element.textContent = formatNumber(currentValue, decimals);
    
    if (progress < 1) {
      requestAnimationFrame(update);
    }
  }
  
  requestAnimationFrame(update);
}

/**
 * Add a glitch effect to an element
 * @param {HTMLElement} element - Element to apply effect to
 * @param {number} duration - Effect duration in ms
 */
function glitchEffect(element, duration = 300) {
  element.classList.add('glitch');
  setTimeout(() => {
    element.classList.remove('glitch');
  }, duration);
}

/**
 * Fade in an element
 * @param {HTMLElement} element - Element to fade in
 */
function fadeIn(element) {
  element.classList.add('fade-in');
  setTimeout(() => {
    element.classList.remove('fade-in');
  }, 300);
}

/**
 * Slide in an element from the bottom
 * @param {HTMLElement} element - Element to slide in
 */
function slideInUp(element) {
  element.classList.add('slide-in-up');
  setTimeout(() => {
    element.classList.remove('slide-in-up');
  }, 300);
}

// ==================== DOM Helper Functions ====================

/**
 * Create an HTML element with attributes and content
 * @param {string} tag - HTML tag name
 * @param {object} attributes - Object of attributes to set
 * @param {string|HTMLElement} content - Content to add to element
 * @returns {HTMLElement} Created element
 */
function createElement(tag, attributes = {}, content = '') {
  const element = document.createElement(tag);
  
  Object.entries(attributes).forEach(([key, value]) => {
    if (key === 'class') {
      element.className = value;
    } else if (key === 'style' && typeof value === 'object') {
      Object.assign(element.style, value);
    } else {
      element.setAttribute(key, value);
    }
  });
  
  if (typeof content === 'string') {
    element.textContent = content;
  } else if (content instanceof HTMLElement) {
    element.appendChild(content);
  }
  
  return element;
}

/**
 * Clear all children from an element
 * @param {HTMLElement} element - Element to clear
 */
function clearElement(element) {
  while (element.firstChild) {
    element.removeChild(element.firstChild);
  }
}

// ==================== Component Type Functions ====================

/**
 * Get color for component type
 * @param {string} type - Component type
 * @returns {string} Hex color code
 */
function getComponentColor(type) {
  const colors = {
    resistor: '#ff006e',
    capacitor: '#00fff9',
    inductor: '#8338ec',
    diode: '#ffd700',
    led: '#39ff14',
    transistor: '#ff006e',
    ic: '#00fff9',
    connector: '#a0a0a0',
    switch: '#ffd700',
    power_supply: '#39ff14',
    ground: '#606060',
    voltage_regulator: '#00fff9',
    default: '#e0e0e0'
  };
  
  return colors[type] || colors.default;
}

/**
 * Get symbol/icon for component type
 * @param {string} type - Component type
 * @returns {string} Unicode symbol or emoji
 */
function getComponentSymbol(type) {
  const symbols = {
    resistor: '⚡',
    capacitor: '⚡',
    inductor: '⚡',
    diode: '▶',
    led: '💡',
    transistor: '⚙',
    ic: '🔲',
    connector: '🔌',
    switch: '⚡',
    power_supply: '🔋',
    ground: '⏚',
    voltage_regulator: '⚙',
    default: '•'
  };
  
  return symbols[type] || symbols.default;
}

// ==================== Validation Functions ====================

/**
 * Validate circuit JSON structure
 * @param {object} data - Circuit data to validate
 * @returns {object} Validation result {valid: boolean, errors: string[]}
 */
function validateCircuit(data) {
  const errors = [];
  
  if (!data) {
    errors.push('No data provided');
    return { valid: false, errors };
  }
  
  if (!data.version) {
    errors.push('Missing version field');
  }
  
  if (!data.metadata) {
    errors.push('Missing metadata field');
  } else if (!data.metadata.name) {
    errors.push('Missing metadata.name field');
  }
  
  if (!data.components || !Array.isArray(data.components)) {
    errors.push('Missing or invalid components array');
  } else if (data.components.length === 0) {
    errors.push('No components defined');
  }
  
  // Check for duplicate component IDs
  if (data.components) {
    const ids = data.components.map(c => c.id);
    const duplicates = ids.filter((id, index) => ids.indexOf(id) !== index);
    if (duplicates.length > 0) {
      errors.push(`Duplicate component IDs: ${duplicates.join(', ')}`);
    }
  }
  
  return {
    valid: errors.length === 0,
    errors
  };
}

// ==================== Math Utilities ====================

/**
 * Clamp a value between min and max
 * @param {number} value - Value to clamp
 * @param {number} min - Minimum value
 * @param {number} max - Maximum value
 * @returns {number} Clamped value
 */
function clamp(value, min, max) {
  return Math.min(Math.max(value, min), max);
}

/**
 * Linear interpolation
 * @param {number} a - Start value
 * @param {number} b - End value
 * @param {number} t - Interpolation factor (0-1)
 * @returns {number} Interpolated value
 */
function lerp(a, b, t) {
  return a + (b - a) * t;
}

/**
 * Calculate distance between two points
 * @param {number} x1 - First point X
 * @param {number} y1 - First point Y
 * @param {number} x2 - Second point X
 * @param {number} y2 - Second point Y
 * @returns {number} Distance
 */
function distance(x1, y1, x2, y2) {
  return Math.sqrt(Math.pow(x2 - x1, 2) + Math.pow(y2 - y1, 2));
}

// ==================== Local Storage Utilities ====================

/**
 * Save data to local storage
 * @param {string} key - Storage key
 * @param {any} data - Data to store
 */
function saveToStorage(key, data) {
  try {
    localStorage.setItem(key, JSON.stringify(data));
    return true;
  } catch (e) {
    console.error('Failed to save to storage:', e);
    return false;
  }
}

/**
 * Load data from local storage
 * @param {string} key - Storage key
 * @returns {any} Loaded data or null
 */
function loadFromStorage(key) {
  try {
    const data = localStorage.getItem(key);
    return data ? JSON.parse(data) : null;
  } catch (e) {
    console.error('Failed to load from storage:', e);
    return null;
  }
}

/**
 * Remove data from local storage
 * @param {string} key - Storage key
 */
function removeFromStorage(key) {
  try {
    localStorage.removeItem(key);
    return true;
  } catch (e) {
    console.error('Failed to remove from storage:', e);
    return false;
  }
}

// ==================== Debounce and Throttle ====================

/**
 * Debounce a function call
 * @param {Function} func - Function to debounce
 * @param {number} wait - Wait time in ms
 * @returns {Function} Debounced function
 */
function debounce(func, wait) {
  let timeout;
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout);
      func(...args);
    };
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
}

/**
 * Throttle a function call
 * @param {Function} func - Function to throttle
 * @param {number} limit - Time limit in ms
 * @returns {Function} Throttled function
 */
function throttle(func, limit) {
  let inThrottle;
  return function executedFunction(...args) {
    if (!inThrottle) {
      func(...args);
      inThrottle = true;
      setTimeout(() => inThrottle = false, limit);
    }
  };
}

// ==================== Export Functions ====================
// Make functions available globally
if (typeof window !== 'undefined') {
  window.CircuitUtils = {
    formatTime,
    formatNumber,
    formatBytes,
    animateCounter,
    glitchEffect,
    fadeIn,
    slideInUp,
    createElement,
    clearElement,
    getComponentColor,
    getComponentSymbol,
    validateCircuit,
    clamp,
    lerp,
    distance,
    saveToStorage,
    loadFromStorage,
    removeFromStorage,
    debounce,
    throttle
  };
}
