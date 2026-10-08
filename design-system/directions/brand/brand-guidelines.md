# Tyros Group Brand Guidelines v1.0

> Last updated: 2026-10-08
> Status: Derived from the live site (tyros-group.com) and the founder's validated decisions. Every colour, font and quoted phrase was checked against the site.

## Quick Reference

| Element | Value |
|---------|-------|
| Primary Color | #152A54 |
| Secondary Color | #A6884F |
| Primary Font | Fraunces |
| Voice | Institutional, Direct, Discreet, Precise |

---

## 1. Color Palette

### Primary Colors

| Name | Hex | RGB | Usage |
|------|-----|-----|-------|
| Tyros Navy | #152A54 | rgb(21,42,84) | Action only: primary CTA, Boards band |
| Tyros Navy Light | #1E3A70 | rgb(30,58,112) | CTA hover |
| Tyros Gold | #A6884F | rgb(166,136,79) | Structure: hairlines, large numerals, markers. Not small text on light |
| Tyros Gold Text | #7D622D | rgb(125,98,45) | Gold used as small text on light surfaces (5.1:1) |
| Tyros Gold Soft | #C4A469 | rgb(196,164,105) | Gold on dark surfaces |

### Secondary Colors

| Name | Hex | RGB | Usage |
|------|-----|-----|-------|
| Ink | #0B0C0E | rgb(11,12,14) | Headlines, dark bands |
| Ink Soft | #3A3C42 | rgb(58,60,66) | Body text |

### Neutral Palette

| Name | Hex | RGB | Usage |
|------|-----|-----|-------|
| Background | #FCFBF9 | rgb(252,251,249) | Page, warm paper |
| Surface | #F4F2EC | rgb(244,242,236) | Alternate band |
| Panel | #FFFFFF | rgb(255,255,255) | Card |
| Text Secondary | #62646C | rgb(98,100,108) | Secondary text |
| Caption | #6C6E76 | rgb(108,110,118) | Labels, captions |
| Border | #E7E4DC | rgb(231,228,220) | Hairlines |

### Semantic Colors

The site has no success or error states. None are defined. Informational and caution cues reuse the brand navy and gold.

| State | Hex | Usage |
|-------|-----|-------|
| Info | #152A54 | Information uses the brand navy |
| Caution | #A6884F | Cautions use the brand gold |

### Accessibility

- Ink on paper: 18:1 (AAA)
- Gold Text on paper: 5.1:1 (AA); Gold on paper: 3.2:1, large type and graphics only
- White on Navy: 13:1 (AAA)
- Dark theme: Gold Soft on #08090C 8.4:1

---

## 2. Typography

### Font Stack

```css
--font-heading: 'Fraunces', Georgia, serif;
--font-body: 'Plex Sans', -apple-system, 'Segoe UI', sans-serif;
```

### Type Scale

| Element | Size (Desktop) | Size (Mobile) | Weight | Line Height |
|---------|----------------|---------------|--------|-------------|
| H1 | 120px | 48px | 600 | 0.98 |
| H2 | 58px | 35px | 600 | 1.05 |
| H3 | 34px | 24px | 600 | 1.2 |
| Body | 16px | 16px | 400 | 1.6 |
| Body Large | 19px | 18px | 400 | 1.6 |
| Small | 14px | 14px | 400 | 1.5 |
| Label | 12px | 12px | 600 | 1.4 |

---

## 3. Logo Usage

### Variants

| Variant | File | Use Case |
|---------|------|----------|
| Wordmark TYROS + GROUP | inline SVG in header | Header, footer, documents |
| Ring monogram | favicon (data URI) | Favicon, small spaces |

### Clear Space

Minimum clear space = height of the ring letter (the O).

### Don'ts

- Do not recolour the gold arc
- Do not add shadows or effects
- Do not place on busy backgrounds
- Do not restyle the letterspacing

---

## 4. Voice & Tone

### Brand Personality

| Trait | Description |
|-------|-------------|
| **Institutional** | Speaks to boards, CROs, CCOs, L&D directors; sober and exact |
| **Direct** | Short sentences, one idea per line, no filler |
| **Discreet** | Confidentiality is the product; never boastful |
| **Precise** | Regulatory and technical terms used correctly; no invented figures |

### Voice Chart

| Trait | We Are | We Are Not |
|-------|--------|------------|
| Institutional | Sober, exact | Corporate-speak, LinkedIn coach |
| Direct | Short, concrete | Wordy, vague |
| Discreet | Confidential, measured | Boastful, name-dropping |
| Precise | Correct, sourced | Hyped, approximate |

### Tone by Context

| Context | Tone | Example |
|---------|------|---------|
| Home / hero | Statement, confident | "Leadership Shapes Markets." |
| Academy | Practical, transmissive | "Practical skills for people who hire, manage, develop and advise." |
| Regulatory content | Careful, dated | "It is not an official certification." |
| CTA | Discreet invitation | "Book a Confidential Discussion" |

### Prohibited Terms

| Avoid | Reason |
|-------|--------|
| Libérez votre potentiel | LinkedIn-coach register |
| Devenez la meilleure version de vous-même | LinkedIn-coach register |
| Révélez le leader qui sommeille en vous | LinkedIn-coach register |
| Acheter maintenant | Wrong register for the offer |
| AI Act certification | Not a certification; use Evidence Pack |
| Qualiopi, CPD accredited | Not demonstrated |

---

## 5. Imagery Guidelines

### Photography Style

- **Lighting:** Natural, slightly desaturated, elegant contrast
- **Subjects:** Architecture details, work tables, notebooks, partial human gestures
- **Color treatment:** Warm palette kept; never heavily filtered
- **Composition:** Strong negative space; one strong image beats three weak ones

### Illustrations

- Style: None. Typography and hairlines carry the identity.
- No gradients, no glassmorphism, no neon, no 3D charts.

### Icons

- Style: Outlined, 1.4px stroke, used sparingly

---

## 6. Design Components

### Buttons

| Type | Background | Text | Border Radius |
|------|------------|------|---------------|
| Primary | #152A54 | #F6F8FC | 0px |
| Secondary | Transparent | #0B0C0E | 0px |

### Spacing Scale

| Token | Value | Usage |
|-------|-------|-------|
| xs | 4px | Tight spacing |
| sm | 8px | Compact elements |
| md | 16px | Standard spacing |
| lg | 24px | Gutters |
| xl | 32px | Large gaps |
| 2xl | 48px | Block spacing |
| 3xl | 96px | Section spacing |

### Border Radius

| Element | Radius |
|---------|--------|
| Buttons | 0px |
| Cards | 0px |
| Pills/Tags | 0px |

---

## AI Image Generation

Not used for photography. No AI-generated image is ever presented as a real photograph.
