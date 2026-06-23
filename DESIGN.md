# Design System

## Source

Use the attached Framer-style system as the visual reference, adapted for this local product UI.

## Tokens

- Canvas: near-black `#050505`.
- Surface 1: charcoal `#111111`.
- Surface 2: lifted charcoal `#1a1a1a`.
- Ink: white `#ffffff`.
- Muted ink: `#999999`.
- Accent: blue `#0099ff`, only for focus, selection, and control accents.
- Primary CTA: white pill on dark canvas.
- Secondary CTA: charcoal pill.
- Cards: 15-20px radius.
- Spotlight card: one scarce gradient card, 30px radius.
- Borders: 2px, max 10% opacity.
- App icon: generated PNG at `assets/app-icon.png`; no provider logos or text.
- Body font: Inter/system fallback with OpenType variants enabled when available.

## Rules

- Dark is the default brand mode.
- Keep gradients inside individual cards, never as page backgrounds.
- Use surface lift for hierarchy before adding color.
- Keep CTAs pill-shaped.
- Do not add extra accent colors for decoration.
- Preserve accessibility: AA contrast, visible focus, reduced-motion support.
