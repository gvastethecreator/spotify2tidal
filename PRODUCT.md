# Product

## Register

product

## Users

People migrating or periodically synchronizing personal Spotify libraries into Tidal from a local machine. They may be comfortable enough to run a Python tool, but the GUI should remove the need to copy playlist IDs, edit YAML for common actions, or remember command-line flags. They are likely checking playlist names, favorites, duplicates, and sync behavior before allowing anything to write to Tidal.

## Product Purpose

Spotify to Tidal is a local sync tool that wraps the existing CLI with a safer, clearer migration workspace. Success means a user can connect accounts, choose Spotify playlists from a visual list, review duplicate names, configure sync behavior, and run or simulate a sync with confidence from the first screen.

## Brand Personality

Calm, trustworthy, practical. The interface should feel like a careful local utility: professional enough to trust with a music library, friendly enough for non-CLI use, and restrained enough that the workflow stays obvious.

## Anti-references

Avoid a raw command wrapper, a generic admin dashboard, a marketing landing page, or a visually cold form dump. Avoid decorative SaaS tropes, nested cards, over-rounded components, low-contrast gray text, and playful visuals that make a library migration feel less safe. The UI should not look like a toy, a terminal skin, or a settings page with the main task hidden.

## Design Principles

1. Put the migration decision first: account status, playlist selection, duplicate review, and sync plan should be visible together on desktop.
2. Make every write action explicit: demo mode must never trigger a real sync, and the UI should state that nothing will be deleted.
3. Prefer direct manipulation over command knowledge: users should pick playlists, filters, duplicate handling, and config options from the screen.
4. Keep density useful, not cramped: this is a working tool, so lists and controls can be compact, but labels and states must remain readable.
5. Preserve the CLI as the source of truth: the GUI improves setup, selection, and review without hiding the underlying sync behavior.

## Accessibility & Inclusion

Target WCAG AA contrast for body text, controls, focus states, and muted helper text. Support keyboard access through native controls, avoid color-only status communication, keep motion minimal, and maintain responsive layouts without horizontal scrolling on common mobile widths.
