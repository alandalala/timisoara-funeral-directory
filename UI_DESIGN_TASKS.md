# 🎨 UI/UX Design Task List - Compassionate Design System

**Project:** Funeral Services Directory Romania  
**Goal:** Calming, trustworthy interface for users under high cognitive load (grief)  
**Created:** December 10, 2025  
**Status:** ✅ ALL PHASES COMPLETE

---

## 📋 Task Checklist

### Phase 1: Color Palette - "Serene Trust" Theme ✅ COMPLETE

- [x] **Task 1.1:** Update CSS variables with new color palette
  ```
  Primary Action:     #4A5D6B (Muted Navy - buttons, links)
  Secondary Brand:    #6B7B8A (Soft Slate - headers, footers)
  Background:         #F8F6F3 (Warm Cream - main content)
  Text Color:         #2D3436 (Charcoal - body text, high readability)
  Card Background:    #FFFFFF (Pure White)
  Border Color:       #E8E4DF (Warm Grey)
  Success:            #7A9E7E (Muted Sage Green - softened)
  Alert/Warning:      #C4A574 (Warm Sand - not jarring)
  Error:              #A67F7F (Dusty Rose - softened red)
  Hover State:        #3D4F5C (Darker Navy)
  ```

- [x] **Task 1.2:** Update Tailwind config with custom colors
- [x] **Task 1.3:** Replace all blue-500, green-600 etc. with semantic color names
- [x] **Task 1.4:** Test color contrast ratios (WCAG AA minimum)

---

### Phase 2: Typography - Dignified & Modern ✅ COMPLETE

- [x] **Task 2.1:** Install Google Fonts
  ```
  Headers: "Playfair Display" (serif, dignified, traditional)
  Body:    "Inter" (sans-serif, readable, modern)
  ```

- [x] **Task 2.2:** Update font configuration in layout.tsx
- [x] **Task 2.3:** Set typography scale:
  ```
  H1: 2.5rem (40px) - Page titles
  H2: 1.75rem (28px) - Section headers
  H3: 1.25rem (20px) - Card titles
  Body: 1rem (16px) - Paragraph text
  Small: 0.875rem (14px) - Captions
  Line height: 1.6 for body text (comfortable reading)
  ```

- [x] **Task 2.4:** Ensure font weights are appropriate (400 body, 600 headers)

---

### Phase 3: Imagery Guidelines

- [ ] **Task 3.1:** Define approved imagery styles:
  ```
  ✅ DO USE:
  - Abstract nature: soft clouds, calm water, gentle light
  - Botanical: olive branches, white flowers (not lilies), greenery
  - Soft focus landscapes: meadows, sunrise/sunset
  - Warm candlelight (non-religious context)
  - Hands holding (comfort, support)
  
  ❌ AVOID:
  - Direct funeral imagery (coffins, cemeteries)
  - Religious symbols (unless company-specific)
  - Dark or moody photography
  - Stock photos with fake smiles
  - Clinical/hospital imagery
  ```

- [ ] **Task 3.2:** Create placeholder image set for development
- [ ] **Task 3.3:** Design icon style guide (line icons, rounded, 2px stroke)

---

### Phase 4: Component Styling - Soft & Approachable ✅ COMPLETE

#### 4.1 Company Cards
- [x] **Task 4.1.1:** Update card styling:
  ```css
  Border radius: 16px (rounded-2xl) - soft, not clinical
  Shadow: 0 2px 8px rgba(0,0,0,0.06) - subtle, not harsh
  Border: 1px solid #E8E4DF - warm grey, not cold
  Padding: 24px - generous spacing
  Hover: Gentle lift (translateY -2px), shadow increase
  Transition: 300ms ease - smooth, not abrupt
  ```

- [x] **Task 4.1.2:** Update card hover states (subtle, not dramatic)
- [x] **Task 4.1.3:** Add gentle icon styling (rounded, not sharp)

#### 4.2 Buttons
- [x] **Task 4.2.1:** Primary button styling:
  ```css
  Background: #4A5D6B (Muted Navy)
  Text: #FFFFFF
  Border radius: 12px
  Padding: 12px 24px
  Font weight: 500
  Hover: #3D4F5C (slightly darker)
  Transition: 200ms ease
  No harsh shadows
  ```

- [x] **Task 4.2.2:** Secondary/outline button styling
- [x] **Task 4.2.3:** CTA buttons (phone call) - use sage green, not bright green

#### 4.3 Form Elements
- [x] **Task 4.3.1:** Input field styling:
  ```css
  Border: 1px solid #E8E4DF
  Border radius: 10px
  Background: #FFFFFF
  Focus: Border color #4A5D6B, subtle glow
  Placeholder: #9CA3AF (medium grey)
  ```

- [x] **Task 4.3.2:** Dropdown styling (match inputs)
- [x] **Task 4.3.3:** Form validation messages (use soft colors)

---

### Phase 5: Layout & Spacing ✅ COMPLETE

- [x] **Task 5.1:** Increase whitespace throughout:
  ```
  Section padding: 48px - 64px
  Card gaps: 24px
  Content max-width: 1200px (not too wide)
  ```

- [x] **Task 5.2:** Reduce visual clutter on homepage
- [x] **Task 5.3:** Simplify navigation (fewer choices = less cognitive load)
- [x] **Task 5.4:** Add breathing room between sections

---

### Phase 6: Micro-interactions & Feedback ✅ COMPLETE

- [x] **Task 6.1:** Loading states - gentle pulse/shimmer animation
- [x] **Task 6.2:** Hover states - subtle card lift, button press
- [x] **Task 6.3:** Success messages - soft green with checkmark
- [x] **Task 6.4:** Error messages - dusty rose, supportive language
- [x] **Task 6.5:** Transitions - 200-300ms, ease curves
- [x] **Task 6.6:** Staggered fade-in for card grids
- [x] **Task 6.7:** Link underline animations
- [x] **Task 6.8:** Input focus glow effects
- [x] **Task 6.9:** Loading spinner component
- [x] **Task 6.10:** Respect prefers-reduced-motion

---

### Phase 7: Accessibility & Comfort ✅ COMPLETE

- [x] **Task 7.1:** Ensure all text passes WCAG AA contrast (4.5:1)
- [x] **Task 7.2:** Add focus indicators for keyboard navigation
- [x] **Task 7.3:** Add skip-to-content link for screen readers
- [x] **Task 7.4:** Ensure touch targets are 44px minimum
- [x] **Task 7.5:** Add "reduce motion" media query support
- [x] **Task 7.6:** Add ARIA landmarks (main, nav, banner, contentinfo)
- [x] **Task 7.7:** Add aria-labels to interactive elements
- [x] **Task 7.8:** Add screen-reader-only (.sr-only) utility class
- [x] **Task 7.9:** Add high contrast mode support
- [x] **Task 7.10:** Ensure proper label associations for form inputs

---

### Phase 8: Page-Specific Updates ✅ COMPLETE

#### Homepage
- [x] **Task 8.1:** Update header gradient/background
- [x] **Task 8.2:** Soften search bar styling
- [x] **Task 8.3:** Update filter buttons
- [x] **Task 8.4:** Soften map markers

#### Company Detail Page
- [x] **Task 8.5:** Update card styling
- [x] **Task 8.6:** Soften CTA buttons
- [x] **Task 8.7:** Update badge styling

#### Static Pages (About, Contact, GDPR)
- [x] **Task 8.8:** Apply new typography
- [x] **Task 8.9:** Update form styling

#### Final Polish (Added)
- [x] **Task 8.10:** Mobile responsive typography
- [x] **Task 8.11:** Mobile spacing adjustments
- [x] **Task 8.12:** Safe area support for notched devices
- [x] **Task 8.13:** Print styles
- [x] **Task 8.14:** Consistent animations across all pages
- [x] **Task 8.15:** All pages use unified focus/hover states

---

## 🎨 Quick Reference - Final Palette

| Element | Color | Hex Code |
|---------|-------|----------|
| Primary Action | Muted Navy | `#4A5D6B` |
| Secondary Brand | Soft Slate | `#6B7B8A` |
| Background | Warm Cream | `#F8F6F3` |
| Card Background | White | `#FFFFFF` |
| Text (Body) | Charcoal | `#2D3436` |
| Text (Secondary) | Medium Grey | `#6B7280` |
| Border | Warm Grey | `#E8E4DF` |
| Success | Sage Green | `#7A9E7E` |
| Warning | Warm Sand | `#C4A574` |
| Error | Dusty Rose | `#A67F7F` |
| Hover | Dark Navy | `#3D4F5C` |

---

## 📝 Design Principles Summary

1. **Calm over Exciting** - No bright colors, gentle transitions
2. **Trust over Trendy** - Classic typography, professional appearance
3. **Simple over Complex** - Reduce choices, clear hierarchy
4. **Warm over Cold** - Cream backgrounds, soft shadows
5. **Supportive over Clinical** - Rounded corners, generous spacing

---

**Next Step:** Start with Phase 1 (Color Palette) and Phase 2 (Typography) as they cascade to all other components.
