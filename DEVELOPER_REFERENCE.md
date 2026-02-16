# Frontend Developer Quick Reference Guide

## Color Palette

### Primary Colors
```css
Indigo:    #6366f1
Purple:    #8b5cf6
Pink:      #ec4899
```

### Secondary Colors
```css
Blue:      #3b82f6 / #1d4ed8
Green:     #10b981 / #059669
Amber:     #f59e0b / #d97706
Red:       #ef4444 / #dc2626
Cyan:      #06b6d4 / #0891b2
```

### Neutral Colors
```css
Slate 900: #0f172a (Darkest)
Slate 800: #1e293b
Slate 700: #334155
Slate 600: #475569
Slate 500: #64748b
Slate 400: #94a3b8
Slate 300: #cbd5e1 (Border)
Slate 200: #e2e8f0
Slate 100: #f1f5f9
Slate 50:  #f8fafc (Lightest)
```

---

## Common CSS Classes & Patterns

### Buttons
```css
/* Primary Button */
.btn-primary {
  background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
  color: white;
  padding: 0.875rem 2rem;
  border: none;
  border-radius: 12px;
  font-weight: 600;
  cursor: pointer;
  box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3);
  transition: all 0.3s ease;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(99, 102, 241, 0.4);
}

/* Secondary Button */
.btn-secondary {
  background: white;
  color: #6366f1;
  border: 2px solid #6366f1;
  padding: 0.875rem 2rem;
  border-radius: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-secondary:hover {
  background: #f0f4ff;
  transform: translateY(-2px);
}
```

### Cards
```css
/* Standard Card */
.card {
  background: white;
  border-radius: 16px;
  padding: 1.75rem;
  border: 2px solid #e2e8f0;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.card:hover {
  transform: translateY(-8px);
  box-shadow: 0 12px 24px rgba(99, 102, 241, 0.15);
  border-color: #6366f1;
}

/* Gradient Card */
.card-gradient {
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
  border: 2px solid #e2e8f0;
}
```

### Tags & Badges
```css
/* Skill Tag */
.skill-tag {
  background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
  color: #1e40af;
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 500;
  border: 1px solid #93c5fd;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
}

.skill-tag:hover {
  background: linear-gradient(135deg, #93c5fd 0%, #60a5fa 100%);
  color: white;
  transform: translateY(-2px);
}

/* Feature Tag */
.feature-tag {
  padding: 0.5rem 1.25rem;
  background: rgba(99, 102, 241, 0.08);
  color: #4f46e5;
  border-radius: 9999px;
  font-size: 0.9rem;
  font-weight: 500;
  border: 1px solid rgba(99, 102, 241, 0.2);
}

.feature-tag:hover {
  background: rgba(99, 102, 241, 0.15);
  transform: scale(1.05);
}
```

---

## Animations

### Fade In
```css
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.element {
  animation: fadeIn 0.5s ease-out;
}
```

### Slide In Up
```css
@keyframes slideInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.element {
  animation: slideInUp 0.5s ease-out;
}
```

### Bounce
```css
@keyframes bounce {
  0%, 100% {
    transform: translateY(0) scale(1);
  }
  50% {
    transform: translateY(-10px) scale(1.05);
  }
}

.element {
  animation: bounce 0.6s ease;
}
```

### Pulse
```css
@keyframes pulse {
  0%, 100% {
    transform: scale(1);
    opacity: 1;
  }
  50% {
    transform: scale(1.1);
    opacity: 0.8;
  }
}

.element {
  animation: pulse 2s ease-in-out infinite;
}
```

### Shake
```css
@keyframes shake {
  0%, 100% { 
    transform: translateX(0); 
  }
  25% { 
    transform: translateX(-10px); 
  }
  75% { 
    transform: translateX(10px); 
  }
}

.element {
  animation: shake 0.3s ease-in-out;
}
```

### Loading Spinner
```css
@keyframes spin {
  to { 
    transform: rotate(360deg); 
  }
}

.spinner {
  border: 3px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}
```

---

## Responsive Breakpoints

### Mobile First Approach
```css
/* Mobile (base styles) */
.element {
  font-size: 1rem;
  padding: 1rem;
}

/* Tablet (768px and up) */
@media (min-width: 768px) {
  .element {
    font-size: 1.1rem;
    padding: 1.5rem;
  }
}

/* Desktop (1024px and up) */
@media (min-width: 1024px) {
  .element {
    font-size: 1.25rem;
    padding: 2rem;
  }
}

/* Large Desktop (1280px and up) */
@media (min-width: 1280px) {
  .element {
    font-size: 1.5rem;
    padding: 2.5rem;
  }
}
```

### Common Breakpoints
```css
/* Extra Small (Below 480px) */
@media (max-width: 479px) { }

/* Small (480px - 767px) */
@media (min-width: 480px) { }

/* Medium/Tablet (768px - 1023px) */
@media (min-width: 768px) { }

/* Large/Desktop (1024px - 1279px) */
@media (min-width: 1024px) { }

/* Extra Large (1280px+) */
@media (min-width: 1280px) { }
```

---

## Flexbox & Grid Patterns

### Centered Content
```css
.centered {
  display: flex;
  align-items: center;
  justify-content: center;
}
```

### Space Between
```css
.space-between {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
```

### Grid - Auto Fit
```css
.auto-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
}
```

### Grid - Auto Fill
```css
.fill-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
  gap: 1rem;
}
```

### Stack Layout
```css
.stack {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}
```

---

## Text & Typography

### Gradient Text
```css
.gradient-text {
  background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
```

### Text Truncation
```css
/* Single line */
.truncate {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

/* Multi-line (2 lines) */
.truncate-2 {
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}
```

### Text Styles
```css
/* Heading Styles */
h1 { font-size: 2.75rem; font-weight: 700; }
h2 { font-size: 2rem; font-weight: 700; }
h3 { font-size: 1.5rem; font-weight: 600; }
h4 { font-size: 1.25rem; font-weight: 600; }

/* Body Text */
p { font-size: 1rem; line-height: 1.6; }
small { font-size: 0.875rem; }
```

---

## Shadows

### Shadow Elevations
```css
/* No Shadow */
.shadow-none {
  box-shadow: none;
}

/* Small */
.shadow-sm {
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}

/* Medium */
.shadow-md {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

/* Large */
.shadow-lg {
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
}

/* Extra Large */
.shadow-xl {
  box-shadow: 0 12px 36px rgba(0, 0, 0, 0.15);
}

/* 2XL */
.shadow-2xl {
  box-shadow: 0 20px 48px rgba(0, 0, 0, 0.2);
}

/* Primary Color Shadow */
.shadow-primary {
  box-shadow: 0 4px 20px rgba(99, 102, 241, 0.3);
}
```

---

## Common Transitions

```css
/* Smooth All */
.smooth {
  transition: all 0.3s ease;
}

/* Cubic Bezier */
.smooth-cubic {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

/* Fast */
.fast {
  transition: all 0.15s ease;
}

/* Slow */
.slow {
  transition: all 0.5s ease;
}

/* Specific Properties */
.transition-colors {
  transition: background-color 0.3s ease, color 0.3s ease;
}

.transition-transform {
  transition: transform 0.3s ease;
}
```

---

## Input & Form Elements

### Text Input
```css
input[type="text"],
input[type="email"],
input[type="password"],
textarea {
  width: 100%;
  padding: 0.75rem 1rem;
  border: 2px solid #e2e8f0;
  border-radius: 12px;
  font-size: 1rem;
  font-family: inherit;
  transition: all 0.3s ease;
}

input:focus,
textarea:focus {
  outline: none;
  border-color: #6366f1;
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
}
```

### Floating Label
```css
.form-group {
  position: relative;
  margin-bottom: 1.5rem;
}

.form-group input {
  width: 100%;
  padding: 1rem 0.75rem 0.5rem;
  border: none;
  border-bottom: 2px solid #e2e8f0;
}

.form-group label {
  position: absolute;
  top: 0.75rem;
  left: 0.75rem;
  color: #94a3b8;
  font-size: 1rem;
  transition: all 0.3s ease;
  pointer-events: none;
}

.form-group input:focus + label,
.form-group input:valid + label {
  top: -0.25rem;
  font-size: 0.75rem;
  color: #6366f1;
}
```

---

## Scrollbar Styling

```css
/* Webkit Browsers (Chrome, Safari, Edge) */
.element::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

.element::-webkit-scrollbar-track {
  background: transparent;
}

.element::-webkit-scrollbar-thumb {
  background: rgba(99, 102, 241, 0.3);
  border-radius: 4px;
}

.element::-webkit-scrollbar-thumb:hover {
  background: rgba(99, 102, 241, 0.5);
}
```

---

## Utility Classes Template

```css
/* Spacing */
.p-1 { padding: 0.25rem; }
.p-2 { padding: 0.5rem; }
.p-4 { padding: 1rem; }
.p-6 { padding: 1.5rem; }
.p-8 { padding: 2rem; }

.m-1 { margin: 0.25rem; }
.m-2 { margin: 0.5rem; }
.m-4 { margin: 1rem; }
.m-6 { margin: 1.5rem; }
.m-8 { margin: 2rem; }

/* Display */
.flex { display: flex; }
.grid { display: grid; }
.block { display: block; }
.hidden { display: none; }

/* Positioning */
.relative { position: relative; }
.absolute { position: absolute; }
.fixed { position: fixed; }

/* Text Alignment */
.text-center { text-align: center; }
.text-left { text-align: left; }
.text-right { text-align: right; }

/* Colors */
.text-primary { color: #6366f1; }
.text-secondary { color: #64748b; }
.text-success { color: #10b981; }
.text-error { color: #ef4444; }
```

---

## Component Import Template

```javascript
// Always import CSS with JSX
import ComponentName from './ComponentName';
import './ComponentName.css';

// Example
import Sidebar from './components/Sidebar';
import './components/Sidebar.css';
```

---

## Testing Checklist

### Desktop
- [ ] Viewport: 1920x1080
- [ ] Hover effects work
- [ ] Animations smooth
- [ ] All buttons clickable

### Tablet
- [ ] Viewport: 768x1024
- [ ] Responsive layout working
- [ ] Touch targets sufficient
- [ ] No overflow

### Mobile
- [ ] Viewport: 375x667
- [ ] Single column layout
- [ ] Text readable
- [ ] Buttons easily tappable

### Browsers
- [ ] Chrome/Chromium
- [ ] Firefox
- [ ] Safari
- [ ] Edge

---

## Performance Tips

1. **Use transforms for animations** - Avoid animating position/size
2. **Debounce resize events** - Prevent excessive updates
3. **Lazy load images** - Improve initial load time
4. **Minimize reflows** - Batch DOM changes
5. **Use CSS Grid for complex layouts** - Better performance than flexbox
6. **Optimize media queries** - Use mobile-first approach
7. **Cache computed values** - Avoid recalculation
8. **Use custom properties** - Reduce CSS size

---

## Resources

- [MDN CSS Reference](https://developer.mozilla.org/en-US/docs/Web/CSS)
- [Can I Use](https://caniuse.com/) - Browser compatibility
- [CSS Tricks](https://css-tricks.com/) - Advanced techniques
- [Typography Scale](https://www.typescale.com/) - Font sizing
- [Color Palettes](https://tailwindcss.com/docs/customizing-colors) - Color inspiration

---

## Quick Copy-Paste Snippets

### Loading Spinner
```html
<div class="loading-spinner"></div>
```

```css
.loading-spinner {
  display: inline-block;
  width: 16px;
  height: 16px;
  border: 3px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  border-top-color: white;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
```

### Error Toast
```html
<div class="error-toast">
  <span class="error-icon">⚠️</span>
  <span>Error message here</span>
</div>
```

```css
.error-toast {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
  border: 2px solid #fca5a5;
  border-radius: 12px;
  color: #991b1b;
}
```

---

**Last Updated**: 2024
**Version**: 1.0
