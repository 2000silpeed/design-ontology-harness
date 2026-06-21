# Mode Signal Fashion Magazine Spec

## Product Goal

Build a responsive editorial web surface for a fashion magazine. The first screen should feel like an active issue desk: hero story, runway pulse, trend rail, and editorial utility controls must all be present without becoming a generic blog grid.

## Primary Views

- Homepage / Today edition
- Runway report feed
- Trend radar
- Shopping edit
- Saved stories panel

## Core UI Requirements

- A visual hero package with a large fashion image, issue label, headline, dek, byline, and save action.
- A top navigation bar with issue sections: Runway, Trends, Beauty, Culture, Shopping, Archive.
- A topic filter row for Fashion Week, Street Style, Interviews, New Designers, Accessories.
- A runway contact sheet rail that supports horizontal scanning.
- A dense but legible article feed with image cards, section labels, reading time, and editorial priority.
- A right-side editor panel on desktop with must-read links, newsletter signup, and live fashion week notes.
- A mobile layout that keeps the hero, filters, and runway rail usable without horizontal page overflow.
- Clear focus states for links, buttons, filters, and save actions.

## Content Model

- Story: title, dek, author, section, published time, image, tags, saved state.
- Runway look: designer, city, season, look number, image, short note.
- Trend signal: name, confidence, source count, related stories.
- Newsletter: title, value proposition, email field, subscribe action.

## Visual Direction

- Editorial rather than commercial landing page.
- Strong display typography with measured body text.
- Imagery should carry the fashion subject; no abstract gradients or empty media boxes.
- Use black, white, red, and cool green/blue accents in a balanced way.
- Cards should be restrained, square or slightly rounded, and dense enough for repeated browsing.

## Interaction Notes

- Filters should update active state.
- Save buttons should toggle state.
- The newsletter form should accept input and show a subscribed state.
- The runway rail should support previous/next controls.
