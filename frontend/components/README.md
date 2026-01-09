# Guidance Components Documentation

This document describes the reusable guidance and notification components for the Skill Intelligence MVP.

## Components

### 1. PrototypeBanner

A dismissible banner that appears at the top of every page to inform users about the MVP/prototype status.

**Usage:**
```tsx
import PrototypeBanner from '@/components/PrototypeBanner'

// Default message
<PrototypeBanner />

// Custom message
<PrototypeBanner 
  message="⚠️ Custom prototype notice" 
  storageKey="custom-banner-key"
/>
```

**Features:**
- Automatically appears on all pages via `layout.tsx`
- Dismissible with close button
- Remembers dismissal using localStorage
- Customizable message and storage key
- Yellow/orange gradient styling

**Props:**
- `message` (string, optional): Custom banner message
- `storageKey` (string, optional): localStorage key for dismissal state (default: 'prototype-banner-dismissed')

---

### 2. InfoTooltip

A contextual tooltip that appears on hover/focus to provide additional information.

**Usage:**
```tsx
import InfoTooltip from '@/components/InfoTooltip'

// With default info icon
<InfoTooltip message="This is helpful information" position="top">
  <button>Hover me</button>
</InfoTooltip>

// Standalone with default icon
<InfoTooltip message="Some guidance text" position="right" />

// With custom trigger
<InfoTooltip message="Custom message" position="bottom">
  <span className="text-blue-500">Custom trigger</span>
</InfoTooltip>
```

**Features:**
- Appears on hover or focus (keyboard accessible)
- Automatically positions within viewport
- Arrow indicator pointing to trigger
- Dark theme support
- Responsive positioning

**Props:**
- `message` (string, required): Tooltip text content
- `position` ('top' | 'bottom' | 'left' | 'right', optional): Preferred position (default: 'top')
- `children` (ReactNode, optional): Custom trigger element (default: info icon)
- `className` (string, optional): Additional CSS classes

**Example:**
```tsx
<label className="flex items-center gap-2">
  Role *
  <InfoTooltip 
    message="Enter your job role. Some niche roles may have limited data."
    position="top"
  />
</label>
```

---

### 3. InfoBox

A styled information box for displaying important messages, warnings, or tips.

**Usage:**
```tsx
import InfoBox from '@/components/InfoBox'

// Info type (blue)
<InfoBox 
  message="This is informational content"
  type="info"
  dismissible={true}
/>

// Warning type (amber/yellow)
<InfoBox 
  message="Warning: This is a prototype"
  type="warning"
  dismissible={true}
/>

// Tip type (green)
<InfoBox 
  message="Tip: Use this feature for better results"
  type="tip"
  dismissible={false}
/>
```

**Features:**
- Three types: info, warning, tip
- Optional dismissible functionality
- Icon indicators for each type
- Color-coded styling
- Dark theme support

**Props:**
- `message` (string, required): Box content text
- `type` ('info' | 'warning' | 'tip', optional): Box type (default: 'info')
- `dismissible` (boolean, optional): Whether box can be dismissed (default: false)
- `className` (string, optional): Additional CSS classes

**Types:**
- `info`: Blue styling, informational icon
- `warning`: Amber/yellow styling, warning icon
- `tip`: Green styling, checkmark icon

---

## Implementation Examples

### Example 1: Form Field with Tooltip

```tsx
<div>
  <label 
    htmlFor="role" 
    className="block text-sm font-semibold mb-2"
  >
    <span className="flex items-center gap-2">
      Role *
      <InfoTooltip 
        message="Enter your job role (e.g., Backend Engineer, Data Scientist)"
        position="top"
      />
    </span>
  </label>
  <input
    type="text"
    id="role"
    name="role"
    className="w-full px-4 py-2 border rounded-lg"
  />
</div>
```

### Example 2: Section Header with Tooltip

```tsx
<h2 className="text-2xl font-bold mb-2 flex items-center gap-2">
  Top Skills
  <InfoTooltip 
    message="Skills ranked by demand and relevance to your search criteria"
    position="right"
  />
</h2>
```

### Example 3: Warning Box Above Form

```tsx
<div className="mb-6">
  <InfoBox
    message="Enter your role and industry. Some niche roles may not return results."
    type="warning"
    dismissible={true}
  />
</div>
```

### Example 4: Results Page Guidance

```tsx
<div className="mb-6">
  <InfoBox
    message="Top skills are based on limited sample data. Use as a reference only."
    type="warning"
    dismissible={true}
  />
</div>
```

---

## Styling

All components use Tailwind CSS and support:
- Light and dark themes
- Responsive design
- Consistent color schemes
- Smooth transitions
- Accessible focus states

## Accessibility

- **PrototypeBanner**: Close button has `aria-label`, keyboard accessible
- **InfoTooltip**: Works with keyboard (focus), `role="tooltip"`, `aria-label` on trigger
- **InfoBox**: Dismissible buttons have `aria-label`, semantic HTML

## Customization

You can customize colors and styling by:
1. Modifying Tailwind classes in component files
2. Using `className` prop where available
3. Overriding CSS variables in `globals.css`

---

## Adding New Guidance Messages

To add guidance anywhere in the app:

1. **For inline help:** Use `InfoTooltip`
```tsx
<InfoTooltip message="Your guidance text" position="top" />
```

2. **For prominent notices:** Use `InfoBox`
```tsx
<InfoBox 
  message="Your important notice" 
  type="warning" 
  dismissible={true} 
/>
```

3. **For page-wide banners:** Update `PrototypeBanner` component or add new banner

---

## Current Usage Locations

- **PrototypeBanner**: `app/layout.tsx` (all pages)
- **InfoBox**: 
  - `app/analyze/page.tsx` (form guidance)
  - `app/results/page.tsx` (results guidance)
- **InfoTooltip**:
  - `app/analyze/page.tsx` (form field labels)
  - `app/results/page.tsx` (section headers)

