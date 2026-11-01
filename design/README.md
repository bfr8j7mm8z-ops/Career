# Job Hunt design system

The look of the Job Hunt app (`app/job-hunt-app.html`) and any future pages in this repo. It is our
own system: calm navy ink, one cobalt accent, soft rounded cards, generous space. It takes general
inspiration from modern SaaS dashboards but contains no third-party brand, logo or assets.
Do not add employer or client brand files here (see `CLAUDE.md`).

Published in Claude as a Design System artifact: https://claude.ai/artifact/7je5i12YABFLVtS8kNHERu
(a mirror of this folder; update both when the look changes).

## Files
- `tokens.css`: colours (light and dark), type, radius, spacing, motion. The source of truth.
- `preview.html`: every component on one page. Open it locally to check a change.

## Principles
1. **Status is the only loud thing.** Mint for good, amber for waiting, red for problems. Everything
   else is navy, grey and white, with cobalt for the one action that matters on a screen.
2. **Phone first.** Every screen works at 390px wide with thumb-sized targets (44px).
3. **Numbers in mono.** Scores, counts and dates use JetBrains Mono so they line up.
4. **Soft, not fussy.** 12px radius on controls, 20px on cards, one light shadow, no gradients.

## Type
| Role | Font | Size |
| --- | --- | --- |
| Page title | Bricolage Grotesque 700 | 28px |
| Section title | Bricolage Grotesque 600 | 20px |
| Body | Manrope 400/600 | 15px, line height 1.55 |
| Small | Manrope | 13px |
| Label / eyebrow | JetBrains Mono 500, capitals, +8% tracking | 10.5px |

## Colour
| Token | Light | Dark | Use |
| --- | --- | --- | --- |
| `--ink` | #101A3C | #E8ECF7 | Text |
| `--mute` | #4A5578 | #96A0C0 | Secondary text |
| `--bg` / `--surface` | #F4F6FB / #FFFFFF | #070D24 / #0F1836 | Page / cards |
| `--line` | #E2E6F0 | #24305A | Borders |
| `--accent` | #2F6FEB | #6E9BFF | Primary action, focus, links |
| `--ok` / `--warn` / `--bad` | #0E7C5E / #8F6200 / #B03030 | #3FD3A8 / #F2C066 / #F28585 | Status text, with matching `-bg` tints |

## Components
Buttons (primary, default, ghost, danger), cards, chips (neutral, ok, warn, bad), tabs, inputs and
selects, banners, score badge, process steps, nav. See `preview.html`.

## Changing the look
Edit `tokens.css`, check `preview.html`, then copy the semantic tokens into the `:root` blocks at
the top of `app/job-hunt-app.html` and republish the app from that file.
