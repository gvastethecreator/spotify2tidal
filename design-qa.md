# Spotify to Tidal GUI Design QA

Date: 2026-06-19

## Target

- Surface: local GUI served by `python -m spotify_to_tidal.gui`
- URL used for review: `http://127.0.0.1:8765/?demo=1`
- Source concept: `C:\Users\cristian\.codex\generated_images\019ee0df-6cb3-75b0-aa44-62f7fef2e963\ig_0ac39362f01b3dc9016a35810623508191bf33325f299079d2.png`
- Final desktop screenshot: `C:\Users\cristian\AppData\Local\Temp\spotify2tidal-redesign-qa\redesign-after-demo-sync-final.png`
- Final mobile screenshot: `C:\Users\cristian\AppData\Local\Temp\spotify2tidal-redesign-qa\redesign-mobile-full-final.png`
- Dark desktop screenshot: `C:\Users\cristian\AppData\Local\Temp\spotify2tidal-redesign-qa\theme-dark-desktop-final.png`
- Light desktop screenshot: `C:\Users\cristian\AppData\Local\Temp\spotify2tidal-redesign-qa\theme-light-desktop-final.png`
- Dark mobile screenshot: `C:\Users\cristian\AppData\Local\Temp\spotify2tidal-redesign-qa\theme-dark-mobile-final.png`
- Side-by-side comparison: `C:\Users\cristian\AppData\Local\Temp\spotify2tidal-redesign-qa\comparison-concept3-vs-final.png`
- Framer-system dark desktop screenshot: `C:\Users\cristian\AppData\Local\Temp\spotify2tidal-redesign-qa\framer-system-dark-desktop.png`
- Framer-system light desktop screenshot: `C:\Users\cristian\AppData\Local\Temp\spotify2tidal-redesign-qa\framer-system-light-desktop.png`
- Framer-system dark mobile screenshot: `C:\Users\cristian\AppData\Local\Temp\spotify2tidal-redesign-qa\framer-system-dark-mobile.png`
- Icon/border dark desktop screenshot: `C:\Users\cristian\AppData\Local\Temp\spotify2tidal-redesign-qa\icon-border-cli-dark-desktop.png`
- Icon/border light desktop screenshot: `C:\Users\cristian\AppData\Local\Temp\spotify2tidal-redesign-qa\icon-border-light-desktop.png`
- Icon/border dark mobile screenshot: `C:\Users\cristian\AppData\Local\Temp\spotify2tidal-redesign-qa\icon-border-dark-mobile.png`

## Design Direction

User selected concept 3, "Calm Review Board". The implementation now follows that direction:

- Left app navigation with active migration state.
- Readiness header and stepper.
- Account/status summary strip.
- Three-column desktop workflow: choose playlists, review duplicates, sync plan.
- Activity rail at the bottom.
- Mobile reflow into a single-column task flow without horizontal scroll.
- Tabler icon language applied consistently across navigation, actions, services, panels, plan rows, and activity.
- Framer-style design system applied: near-black canvas, charcoal surfaces, white primary pill CTA, sparse accent-blue selection/focus, Inter-compatible OpenType feature settings, and one contained gradient spotlight card.
- Generated app icon applied in the sidebar brand and favicon route; it avoids provider logos and text.
- Borders normalized to 2px with border-color opacity capped at 10% in the active GUI CSS.

## Impeccable Pass

Impeccable was installed from `pbakaus/impeccable` and used as a manual QA framework in this session. `PRODUCT.md` was added because Impeccable requires product context before design review.

Results:

- `detect.mjs --json src\spotify_to_tidal\gui_ui.py`: clean, no detector findings.
- Product register: `product`.
- Applied product UI criteria: restrained palette, standard affordances, labels with icons, no landing page framing, no decorative motion, no nested cards inside cards.
- Applied hardening/adapt checks: long playlist names, RTL/CJK text, emoji, large list, mobile viewport, demo sync safety.

## Automated Visual And Accessibility Evidence

- Playwright desktop `1440x1024`: no console errors, no horizontal overflow.
- Playwright mobile `390x900`: no console errors, no horizontal overflow.
- axe desktop after demo sync: no violations.
- axe dark desktop, light desktop, and dark mobile after theme toggle work: no violations.
- axe Framer-system dark desktop, light desktop, and dark mobile: no violations; no console errors; no horizontal overflow.
- Design-token probe: dark primary CTA is white with 100px pill radius; light primary CTA is black with 100px pill radius; duplicate-review spotlight uses a contained gradient.
- Playwright icon/border probe: `/app-icon.png` is used by the brand mark, visible border widths are 2px, border-color alpha is <= 0.10, no console errors, no horizontal overflow.
- Stress demo with 80 playlists, long text, RTL/CJK, emoji: no console errors, no horizontal overflow.
- Demo sync button in `?demo=1`: simulated only, no backend sync call.

## Fixes Made During QA

- Replaced the rough initial GUI with a calmer task board matching concept 3.
- Added real inline Tabler SVG icons with no CDN dependency.
- Added dark mode as the default, with a persisted light/dark toggle in the top action bar.
- Added `DESIGN.md` with the adapted Framer-style product UI tokens and rules.
- Applied the attached design system tokens across the app: near-pure black canvas, charcoal surface levels, white/black pill primary CTA, accent-blue selection, restrained borders, and a scarce spotlight gradient card.
- Added generated `assets/app-icon.png` and served it from `/app-icon.png` plus `/favicon.ico`.
- Added CSS-only micro-interactions: button/chip/row/card hover feedback, panel entrance, theme icon swap, and reduced-motion guardrails.
- Fixed mobile overflow by making navigation wrap and panels reflow.
- Darkened amber badge text to pass WCAG AA contrast.
- Added `aria-live` status regions for sync messages and activity.
- Corrected duplicate-name counting so the summary and review panel use the same model.
- Hardened duplicate rendering and activity cards to avoid unsafe `innerHTML` for external playlist data.
- Kept demo data safe: public demo loads illustrative playlist data and demo sync is always simulated.

## Remaining Product Gaps

- P2: Live Spotify OAuth and Tidal device login were not exercised with real credentials in this QA pass.
- P2: Tidal public playlist lookup is still simulated in demo mode; real Tidal playlist browsing remains future work.
- P3: Demo artwork uses deterministic placeholder images instead of real provider cover art.
- P3: Real brand font files are not bundled. The UI uses the configured Inter/system fallback stack and enables the requested OpenType features when available.

## Verdict

Passed for MVP GUI visual QA. The interface is usable from the first screen with mock/public demo data, visually aligned to the selected concept, responsive, accessible by axe, and safe in demo mode.
