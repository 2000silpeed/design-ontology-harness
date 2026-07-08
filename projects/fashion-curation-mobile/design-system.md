# Tinge Design System

## Brand Idea

Tinge is a style calibration tool. The interface should feel like tuning color, silhouette, and restraint before shopping. It is quiet, direct, and a little editorial, but it must stay tool-like.

## Structure

- `occasion-pulse`: today's external constraints.
- `style-compass`: the primary decision object.
- `closet-tape`: owned garment memory.
- `silhouette-preview`: calibrated outfit direction.
- `accent-tray`: bounded missing-piece candidates.
- `decision-dock`: save or shortlist one accent.

## Visual Language

- Color is mixed, not monochrome: ink, oxblood, mineral teal, citron, paper, and clay.
- Typography uses a compact sans body and a restrained serif accent for calibration language.
- Surfaces are layered with fine borders and firm spacing. Avoid a wall of cards.
- Imagery must reveal garments, fabric, or silhouette, not abstract decoration.

## Component Contract

`brand_profile.component_decision.core_components` is the source of truth for actual implementation components. Product primitives describe product surfaces only; they must not choose components by rule.

Astryx and Geist are used only for state, anatomy, accessibility, and coverage checks.
