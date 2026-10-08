# Tyros Group, Photo and visual direction (v1)

Status: direction and placement plan. **No photograph has been produced or published.** Photographs must be real (commissioned or properly licensed); see section 6.

## 1. The idea

Visuals exist to reinforce three ideas: **expertise, decision, movement**. They are never decoration. If an image could sit unchanged on the site of Deloitte, Accenture, Revolut, a fintech SaaS or a generic recruitment firm, it is not Tyros enough.

Register: editorial, sober, European. A high-end economic magazine or an independent specialist house. A real, cultured, precise, demanding world. Never stock corporate.

## 2. What to shoot

Prefer:
- Institutional contemporary architecture, **details rather than whole buildings**: facades, stone, metal, glass, geometric lines.
- Real financial districts (City of London, La Défense, Canary Wharf, European business quarters) treated editorially, never as a skyline.
- Close-ups of documents, files, notes, notebooks, work tables, without staging.
- Human details: hands, movement, partial silhouettes, conversation, arriving at a building. Never "stock portraits".
- Strong composition with **negative space**.
- Slightly desaturated, natural light, elegant contrast.
- Palette: black, cream, stone, warm brown, grey, deep blue, with a discreet trace of Tyros gold.

Avoid, without exception: arms-crossed businessman, handshake, artificially posed multicultural group around a laptop, woman in front of a hologram dashboard, robot or digital brain or circuits, padlock or cyber imagery, generic blue skyline, growth arrows or 3D charts, saturated images, "American SaaS" stock, futuristic effects, purple gradients, neon, glassmorphism. Do not illustrate "risk" literally (no padlock, no chessboard). No close-up CVs.

## 3. By activity

| Activity | Ideas to carry | Shot ideas |
|---|---|---|
| Executive Search | selection, decision, trajectory, expertise, leadership | A door held half open; a staircase seen from below; a hand placing one document apart from a pile; a corridor with a single figure partly out of frame |
| Academy | transmission, reflection, discussion, group work | Open notebook with handwriting, hands partial; a sober training room seen from the back, no faces; a table with annotated printouts and two cups |
| Risk / Compliance / Consulting | rigour, institution, working detail | Stone facade detail with strong shadow line; archive boxes and a ruled notebook; a pen resting on a signed page |
| Business Development | opening a market, relationships, movement | A revolving door in motion (blurred), a hall with a visitor arriving, two coats on a chair at a discussion table, a city street at an angle |

## 4. Composition rule

**One strong image beats three weak ones.** Do not add an image to every section. Pages stay mostly typographic. Images are *breathing spaces* or *points of tension*, not illustrations.

Planned placements (mockups in `design-system/photo/`):

| Slot | Where | Format | Verdict from the mockups |
|---|---|---|---|
| **A** | Home, between Industries and Intelligence: full-bleed band | 21:9 desktop, 5:4 mobile | **Recommended first.** Clean rhythm, hero stays purely Tyros. |
| **C** | Academy programme pages, between hero and body | 16:7, column width | Good second step, one image reused per family, not per page. |
| **B** | Home hero, partial vertical image bleeding off the right edge | 4:5 | **Not recommended at 30% width:** it cuts the end of the headline ("Markets"). If tested, it must stay under about 22% of the width and sit beyond the headline's right edge, which makes it a narrow strip. The hero should stay typographic. |

## 5. Treatment

- No rounded corners by default. No heavy shadows. Straight, decisive crops. Very tight crops are welcome.
- Wide or vertical editorial formats.
- Keep the warm palette. A photo may be slightly desaturated or warmed, never heavily filtered.
- Optional hairline: 1px `--line` frame only if the image sits on a same-tone background.
- Caption (optional), label style 12px, `--grey-2`: place and year only.

Delivery spec:
- Export AVIF and WebP (JPEG fallback), widths 640 / 1200 / 2000, under about 200 KB each at 1200.
- Always set `width` and `height` (no layout shift), `loading="lazy"` below the fold, `decoding="async"`.
- Meaningful `alt` in the page language, factual and short; decorative images get `alt=""`.
- Self-hosted in `/assets/img/`. The CSP already allows same-origin images.

Component (to add to `assets/tyros-ds.css` when the first photo exists):

```css
.ed-figure{margin:0;}
.ed-figure img{display:block;width:100%;height:auto;border-radius:0;box-shadow:none;}
.ed-figure.band img{aspect-ratio:21/9;object-fit:cover;}
@media (max-width:820px){.ed-figure.band img{aspect-ratio:5/4;}}
.ed-figure figcaption{font-size:var(--fs-label);letter-spacing:.14em;text-transform:uppercase;color:var(--grey-2);margin-top:.8rem;}
```

## 6. Sourcing and honesty

Tyros's positioning is honesty (no invented logos, statistics or testimonials). The same rule applies to imagery.
1. **Best:** commission one photographer for a half-day shoot using the shot list. Everything is then real, ownable and consistent.
2. **Acceptable:** license from a curated editorial source (check usage rights for commercial web use and for social sharing; keep the licence file with the asset).
3. **Not recommended:** AI-generated images presented as photographs. They tend toward the generic look this brief rules out, and they undermine the "real, precise world" the brand claims. If used at all, only as an internal moodboard, never published.
4. Real photographs of people need written consent. Never imply a client relationship through an image.

## 7. Open graph (share) images, done

Typographic only, using site fonts and colours (no photo), 1200 x 630, under 70 KB each. Source: `design-system/og/og.html`. Files in `assets/og/`.

| File | Used on | Content |
|---|---|---|
| `og-tyros-group.png` | Home, expertise pages (default) | TYROS GROUP, "Financial Services", "Consulting · Recruitment · Executive Education" |
| `og-tyros-academy.png` | Academy pages (DORA, AI Literacy and the four Management programmes, FR and EN) | "Executive Education for Financial Services" on ink |
| `og-executive-search.png` | Executive Search, CRO, CCO, Boards pages (FR and EN) | "Leadership Shapes Markets." |
| `og-tyros-insights.png` | Insights hub and articles (FR and EN) | "Intelligence, leadership, regulation." on navy |

Each page now declares `og:image` (1200 x 630, with alt text) and `twitter:card = summary_large_image`. After publication, refresh the previews in LinkedIn's Post Inspector and Facebook's Sharing Debugger, since platforms cache the old card.
