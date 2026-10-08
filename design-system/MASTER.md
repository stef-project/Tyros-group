# Tyros Group, Design System (v1)

Source of truth for the visual language of tyros-group.com. It documents what the brand already is, then the rules added to make it more consistent. Implementation: `assets/tyros-ds.css`, loaded after each page's inline styles.

## 1. Identity analysis: what Tyros already is

| Dimension | What exists today | Verdict |
|---|---|---|
| Voice | Editorial, institutional, few words, large statements ("Leadership Shapes Markets.") | Keep. This is the brand. |
| Typography | Fraunces (display serif, weight 600, tight tracking) + IBM Plex Sans (body). Hero up to 7.5rem. | Keep both families. Fix scale and leading. |
| Colour | Warm paper `#FCFBF9`, near-black ink, **gold** `#A6884F` / `#C4A469`, **navy** `#152A54` reserved for CTAs and the Boards band. Full dark theme. | Keep. Fix gold and grey as *text* (contrast). |
| Line language | Hairlines (`--line`), 6px cards, 2px buttons, pill tags, numbered labels `01 02 03`, gold top rule on stats | Keep. Make it systematic. |
| Surfaces | Alternating `--bg` / `--bg-2` bands, generous whitespace, one soft shadow | Keep. |
| Motion | Reveal on scroll, slow canvas line field, small hover lifts | Keep. One timing vocabulary. |
| Imagery | None yet (CSS atmosphere only) | Open: real architecture photography is the missing tier. |

What it is **not**, and must not become: a SaaS template (no gradients-on-everything, no bento grids, no emoji icons, no rounded-2xl cards, no neon accents). The UI/UX Pro Max reference was used as a quality checklist (contrast, focus, targets, motion, minimum sizes). Its generic "luxury" font and palette suggestions were deliberately **not** adopted.

### Measured problems found (before → after, 8 page types × light/dark × desktop/mobile)

| Check | Before | After |
|---|---|---|
| Text failing WCAG AA contrast | 358 | **0** |
| Text smaller than 12px | 504 | **0** |
| Interactive targets under 44px | 112 | **0** |
| Horizontal overflow | 0 | 0 |

Header, hero imagery, logo lock-up and gradient tiles are excluded from the contrast count because their backgrounds are not flat colours; they were checked by eye.

## 2. Principles

1. **Restraint is the luxury.** One accent (gold), one action colour (navy). Gold marks *structure* (labels, hairlines, markers); navy marks *action*.
2. **Hierarchy through type, not boxes.** Size and weight of Fraunces do the work. Surfaces stay quiet.
3. **Hairlines, not shadows.** Borders and rules separate; shadow is reserved for elevation on hover.
4. **Calm motion.** Nothing bounces. Motion confirms, it never performs. Always disabled under `prefers-reduced-motion`.
5. **Accessible by default.** AA contrast on every theme, visible focus, 44px targets, no information in colour alone.

## 3. Tokens

### Colour (existing names kept)
| Token | Light | Dark | Use |
|---|---|---|---|
| `--bg` / `--bg-2` / `--panel` | `#FCFBF9` / `#F4F2EC` / `#FFF` | `#08090C` / `#0C0E13` / `#101319` | Page, alternate band, card |
| `--ink` / `--ink-soft` | `#0B0C0E` / `#3A3C42` | `#F5F4F0` / `#C7C8CE` | Headings, body |
| `--grey` | `#62646C` *(was #6C6E76)* | `#9195A0` | Secondary text (≥5.7:1) |
| `--grey-2` | `#6C6E76` *(was #9A9CA4, 2.6:1)* | `#80848F` *(was #666A76)* | Captions, labels (≥4.5:1 on `--bg-2`) |
| `--gold` | `#A6884F` | `#C4A469` | Lines, graphics, large numerals. **Not** small text on light |
| `--gold-text` *(new)* | `#7D622D` (5.1:1) | `#C4A469` | Gold used as text: eyebrows, numbers, links |
| `--gold-deep` *(new)* | `#85692F` | `#C4A469` | Gold as a fill behind white text |
| `--blue` / `--blue-2` | `#152A54` / `#1E3A70` | `#22467F` / `#2E579A` | CTAs, Boards band |

### Type scale
| Step | Size | Font | Use |
|---|---|---|---|
| Hero | `clamp(3rem, 9vw, 7.5rem)` | Fraunces 600, leading 1.0 | Home h1 only |
| Display | `clamp(2.2rem, 4.5vw, 3.6rem)` | Fraunces 600, leading 1.1 | Section h2 |
| Title | `clamp(1.5rem, 2.5vw, 2.1rem)` | Fraunces 600, leading 1.2 | Cards, h3 |
| Page h2 | `clamp(1.35rem, 2.2vw, 1.65rem)` | Fraunces 600, leading 1.2 | Editorial pages |
| Lede | `clamp(1.05rem, 1.4vw, 1.2rem)` | Plex 400 | Intro paragraphs, `text-wrap: balance` |
| Body | `1rem` / 1.6–1.7 | Plex 400 | Max measure 62ch, `text-wrap: pretty` |
| Small | `.875rem` | Plex | Secondary |
| Label | `.75rem` (floor), tracking `.14–.24em`, uppercase, weight 600 | Plex | Eyebrows, tags. **Never below 12px** |

### Spacing and layout
- Section: `clamp(4.5rem, 9vw, 8rem)`; section head to content: `clamp(2.5rem, 5vw, 4rem)`.
- Container: `max-width: 80rem`, side padding `7vw`. Editorial pages: `52rem`.
- Radius: `2px` buttons, `6px` cards, `100px` pills, `50%` icon buttons.
- Touch target: `2.75rem` (44px).

### Motion
`--ease: cubic-bezier(.2,.6,.2,1)` · `--dur-1 .15s` colour/underline · `--dur-2 .25s` surface hover · `--dur-3 .45s` reveal/theme.

## 4. Components

| Component | Rules |
|---|---|
| **Eyebrow** | Uppercase 12px, tracking .24em, `--gold-text`. On navy/ink bands: `--gold-soft`. |
| **Button primary** | Navy fill, `--blue-ink` text, 44px high, 2px radius, 1px lift on hover. One per view cluster. |
| **Button ghost** | Transparent, hairline border, gold border on hover. |
| **Nav link** | Grey text; a 1px gold underline **sweeps in from the left** on hover (150–250ms). |
| **Card / offer tile** | Hairline border, white panel. Hover signature = **2px gold hairline across the top edge** + soft background shift. Same on offers, insight cards, hub cards. |
| **Family label** (Academy) | Uppercase gold label followed by a hairline that fills the row. Makes two families read as two chapters. |
| **Pill tag** | 100px radius, hairline border, `--ink-soft` text. |
| **Editorial list** | No bullets. A **gold 1px dash** marks each item. |
| **Inline link** | Ink text, 1px gold underline, 2px on hover. |
| **Stat** | Gold top rule, Fraunces numeral, unit in gold. |
| **Focus** | 2px `--gold-text` outline, 3px offset, on every interactive element. |

## 5. Interaction rules
- Hover only ever *adds* information (underline, hairline, arrow); it is never the only way to reach something.
- Every transition 150–450ms with `--ease`. No width/height animation; transform and opacity only.
- Anchors land below the sticky header (`scroll-padding-top: 5.5rem`).
- Reduced motion: all transitions collapse to ~0ms, no hover transforms.

## 6. Do / Don't
**Do** keep headlines short and large; use gold for structure; keep navy for the one action; let whitespace carry the premium feel; keep real photography for later rather than faking it.
**Don't** add a third accent colour; use gold below 5:1 contrast for text; mix radii; use emoji or stock icons; animate on load beyond the reveal; place text under 12px.

## 7. Known open items
- Real photography (architecture, founder portrait) is the missing premium tier.
- Page-level inline CSS (~23KB per page) still duplicates the base styles. A future step is to move shared rules fully into `assets/tyros-ds.css` and delete the inline copies; this was deliberately not done in v1 to avoid regressions.
- `og:image` is still absent (social shares have no visual).
