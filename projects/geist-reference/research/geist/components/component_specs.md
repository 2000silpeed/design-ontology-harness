# Geist Component Specs

- Total components: 71
- Families: action, content, data-display, feedback, form, identity, input, layout, navigation, overlay, surface
- Policy: metadata-only reference; implementation source is not vendored.

## Avatar

- Slug: `avatar`
- Family: `identity`
- Source: https://vercel.com/geist/avatar
- Role: Avatars represent a user or a team. Stacked avatars represent a group of people
- States: default, loading, empty
- Props observed: members, size, limit, overlap, username, icon, color, letter
- Sections: Group, Stacking order, Overlap, Fixed overlap, Size, Git

## Badge

- Slug: `badge`
- Family: `feedback`
- Source: https://vercel.com/geist/badge
- Role: A label that emphasizes an element that requires attention, or helps categorize with other similar elements.
- States: info, success, warning, error, loading
- Props observed: variant, contrast, size, icon, href, data-slot
- Sections: Variants, Sizes, With icons, Pill, Best Practices

## Banner

- Slug: `banner`
- Family: `feedback`
- Source: https://vercel.com/geist/banner
- Role: A prominent message that spans the full width of its container to announce important information.
- States: info, success, warning, error, loading
- Props observed: button
- Sections: Default

## Book

- Slug: `book`
- Family: `content`
- Source: https://vercel.com/geist/book
- Role: A responsive book component.
- States: default, hover, selected
- Props observed: title, variant, width, color, textColor, icon, illustration
- Sections: Default, Variants, Custom color, Custom icon, Custom illustration, Responsive

## Breadcrumbs

- Slug: `breadcrumbs`
- Family: `navigation`
- Source: https://vercel.com/geist/breadcrumbs
- Role: Navigation aid that shows the user's location within a site's hierarchy, with text and menu variants.
- States: default, hover, active, focus, disabled
- Props observed: type
- Sections: Default, Active, Disabled

## Browser

- Slug: `browser`
- Family: `content`
- Source: https://vercel.com/geist/browser
- Role: The Browser component lets you showcase website screenshots or any other content within a realistic browser-style frame.
- States: default, hover, selected
- Props observed: address
- Sections: Composition, Best Practices, When to use, Behavior, Accessibility

## Button

- Slug: `button`
- Family: `action`
- Source: https://vercel.com/geist/button
- Role: Trigger an action or event, such as submitting a form or displaying a dialog.
- States: default, hover, active, disabled, loading, focus
- Props observed: size, variant, aria-label, shape, prefix, suffix, href, active
- Sections: Sizes, All Types and Sizes in comparison, Shapes, Prefix and suffix, Rounded, Loading

## Calendar

- Slug: `calendar`
- Family: `input`
- Source: https://vercel.com/geist/calendar
- Role: Displays a calendar from which users can select a date or range of dates.
- States: default, hover, focus, disabled, error, selected
- Props observed: onChange, value, minValue, maxValue, showTimeInput, popoverAlignment, size, presets
- Sections: Default, Horizontal Layout, Sizes, Presets, Compact, Stacked

## Card

- Slug: `card`
- Family: `surface`
- Source: https://vercel.com/geist/card
- Role: A container that groups related content and actions on a surface.
- States: default, hover, selected, disabled
- Props observed: direction
- Sections: Default, Hover, Border, Border Between, Border Between Vertical, Secondary

## Checkbox

- Slug: `checkbox`
- Family: `input`
- Source: https://vercel.com/geist/checkbox
- Role: A control that toggles between two options, checked or unchecked.
- States: default, hover, focus, disabled, error, selected
- Props observed: checked, onChange
- Sections: Default, Disabled, Indeterminate, Best Practices, When to use, Behavior

## Choicebox

- Slug: `choicebox`
- Family: `input`
- Source: https://vercel.com/geist/choicebox
- Role: A larger form of Radio or Checkbox, where the user has a larger tap target and more details.
- States: default, hover, focus, disabled, error, selected
- Props observed: label, onChange, type, value, listClassName, description, title, variant
- Sections: Single-select, Multi-select, Disabled, Custom content, Best Practices, When to use

## Clearable Input

- Slug: `clearable-input`
- Family: `input`
- Source: https://vercel.com/geist/clearable-input
- Role: Text input with a clear button that resets the value on Escape.
- States: default, hover, focus, disabled, error, selected
- Props observed: aria-label, onChange, placeholder, value, label, onClear
- Sections: Default, With Label, With Cmdk, Disabled, With Clear Callback

## Code

- Slug: `code`
- Family: `content`
- Source: https://vercel.com/geist/code
- Role: Display a snippet of code with syntax highlighting.
- States: default, hover, selected
- Props observed: none extracted
- Sections: Default

## Code Block

- Slug: `code-block`
- Family: `content`
- Source: https://vercel.com/geist/code-block
- Role: Code Block component used across Vercel and Next.js.
- States: default, hover, selected
- Props observed: none extracted
- Sections: Default, No filename, Highlighted lines, Added & removed lines, Referenced lines, Language switcher

## Collapse

- Slug: `collapse`
- Family: `overlay`
- Source: https://vercel.com/geist/collapse
- Role: A set of headings, vertically stacked, that each reveal an related section of content. Commonly referred to as an accordion.
- States: closed, opening, open, dismissed
- Props observed: title, size
- Sections: Default, Question A, Question B, Expanded, Multiple, Small

## Combobox

- Slug: `combobox`
- Family: `input`
- Source: https://vercel.com/geist/combobox
- Role: Filters large lists to selectable options based on the matching query.
- States: default, hover, focus, disabled, error, selected
- Props observed: aria-label, placeholder, value, onChange, width, maxWidth, emptyMessage, prefix
- Sections: Uncontrolled, Controlled, Disabled, Errored, Custom width input, Custom width list

## Command Menu

- Slug: `command-menu`
- Family: `overlay`
- Source: https://vercel.com/geist/command-menu
- Role: Launch a set of actions as a full-screen overlay.
- States: closed, opening, open, dismissed
- Props observed: onClick, open, setOpen, placeholder, heading, callback, suffix, color
- Sections: Default, With divider, With suffix, Best Practices, When to use, Behavior

## Context Card

- Slug: `context-card`
- Family: `surface`
- Source: https://vercel.com/geist/context-card
- Role: Tooltip
- States: default, hover, selected, disabled
- Props observed: content, side, align
- Sections: Default, Alignment, Best Practices, When to use, Behavior, Content

## Context Menu

- Slug: `context-menu`
- Family: `overlay`
- Source: https://vercel.com/geist/context-menu
- Role: Displays a brief heading and subheading to communicate any additional information or context a user needs to continue.
- States: closed, opening, open, dismissed
- Props observed: onClick, value, href, prefix, suffix
- Sections: Default, Disabled items, Link items, Prefix and suffix, Best Practices, When to use

## Copy Button

- Slug: `copy-button`
- Family: `action`
- Source: https://vercel.com/geist/copy-button
- Role: A button that copies a given string to the clipboard and provides feedback when copied.
- States: default, hover, active, disabled, loading, focus
- Props observed: textToCopy, label
- Sections: Default

## Description

- Slug: `description`
- Family: `content`
- Source: https://vercel.com/geist/description
- Role: Displays a brief heading and subheading to communicate any additional information or context a user needs to continue.
- States: default, hover, selected
- Props observed: content, title, tooltip
- Sections: Default, Text right, Ellipsis, Best Practices

## Destructive Action Modal

- Slug: `destructive-action-modal`
- Family: `overlay`
- Source: https://vercel.com/geist/destructive-action-modal
- Role: Confirm destructive actions with a required type-to-confirm gate and an optional irreversibility band.
- States: closed, opening, open, dismissed
- Props observed: onClick, size, variant, confirmLabel, description, irreversibleDescription, loading, onCancel
- Sections: Default, Reversible, Loading, With error, Best Practices, When to use

## Dots Menu

- Slug: `dots-menu`
- Family: `action`
- Source: https://vercel.com/geist/dots-menu
- Role: An overflow menu triggered by a three-dot icon that reveals additional actions in a dropdown.
- States: default, hover, active, disabled, loading, focus
- Props observed: iconSize
- Sections: Default, Sizes, Disabled, Disabled Menu Item

## Drawer

- Slug: `drawer`
- Family: `overlay`
- Source: https://vercel.com/geist/drawer
- Role: Display content in a separate view from the existing context.
- States: closed, opening, open, dismissed
- Props observed: onClick, onDismiss, show, height
- Sections: Default, Custom height, Best Practices, When to use, Behavior, Content

## Empty State

- Slug: `empty-state`
- Family: `feedback`
- Source: https://vercel.com/geist/empty-state
- Role: Fill spaces when no content has been added yet, or is temporarily empty due to the nature of the feature and should be designed to prevent confusion.
- States: info, success, warning, error, loading
- Props observed: description, icon, size, title, variant, data-zone, href, type
- Sections: Empty state Design framework, Blank slate, Informational, Best Practices, When to use, Behavior

## Entity

- Slug: `entity`
- Family: `identity`
- Source: https://vercel.com/geist/entity
- Role: Displays up-to-two columns of content. The left column can contain arbitrary content, and the right column typically contains controls or actions related to the content in the left column.
- States: default, loading, empty
- Props observed: left, size, username, right, description, title, height, width
- Sections: Default, Entity with Skeleton, Entity with List, Entity with List and Checkbox, Entity with Fill, Entity with Column ClassNames

## Error

- Slug: `error`
- Family: `feedback`
- Source: https://vercel.com/geist/error
- Role: Good error design is clear, useful, and friendly. Designing concise and accurate error messages unblocks users and builds trust by meeting people where they are.
- States: info, success, warning, error, loading
- Props observed: label, size, error
- Sections: Default, Custom label, No label, Sizes, With an error property, Best Practices

## Error Card

- Slug: `error-card`
- Family: `feedback`
- Source: https://vercel.com/geist/error-card
- Role: A card used to communicate an error state with a title and message.
- States: info, success, warning, error, loading
- Props observed: message, title
- Sections: Default, No credits left

## Feedback

- Slug: `feedback`
- Family: `feedback`
- Source: https://vercel.com/geist/feedback
- Role: Gather text feedback with an associated emotion.
- States: info, success, warning, error, loading
- Props observed: label, type, metadata, prefix, suffix
- Sections: Default, Inline, Feedback with Select, Feedback with metadata, Feedback with prefix, Feedback with suffix

## Fieldset

- Slug: `fieldset`
- Family: `form`
- Source: https://vercel.com/geist/fieldset
- Role: Groups related form controls inside a bordered card with optional footer actions.
- States: default, focus, disabled, error
- Props observed: href, variant, size, type
- Sections: Default, Disabled, With Long Content, Multiple Fieldsets, Without Footer, Without Title

## File Tree

- Slug: `file-tree`
- Family: `content`
- Source: https://vercel.com/geist/file-tree
- Role: Display a hierarchical directory structure with expandable folders and files, useful for illustrating project layouts.
- States: default, hover, selected
- Props observed: name, href, type
- Sections: Default

## Gauge

- Slug: `gauge`
- Family: `data-display`
- Source: https://vercel.com/geist/gauge
- Role: A circular visual for conveying a percentage.
- States: default, loading, empty, error, selected
- Props observed: size, value, colors, arcPriority
- Sections: Default, Label, Default color scale, Custom color range, Custom secondary color, Arc priority

## Grid

- Slug: `grid`
- Family: `layout`
- Source: https://vercel.com/geist/grid
- Role: Display elements in a grid layout.
- States: default, responsive
- Props observed: guideWidth, columns, height, rows, column, row, hideGuides
- Sections: Grid, Basic grid, Solid cells, Responsive grid, Responsive Grid with responsive guide clipping cells, Grid with hidden row guides

## Input

- Slug: `input`
- Family: `input`
- Source: https://vercel.com/geist/input
- Role: Retrieve text input from a user.
- States: default, hover, focus, disabled, error, selected
- Props observed: aria-labelledby, placeholder, size, prefix, suffix, prefixStyling, suffixStyling, suffixContainer
- Sections: Default, Prefix and suffix, Disabled, Search, ⌘K, Error

## Keyboard Input

- Slug: `keyboard-input`
- Family: `input`
- Source: https://vercel.com/geist/keyboard-input
- Role: Display keyboard input that triggers an action.
- States: default, hover, focus, disabled, error, selected
- Props observed: none extracted
- Sections: Modifiers, Combination, Small, Best Practices

## Label

- Slug: `label`
- Family: `form`
- Source: https://vercel.com/geist/label
- Role: Accessible text label for form controls.
- States: default, focus, disabled, error
- Props observed: id, value, aria-labelledby, placeholder
- Sections: Default, With Input, Bypass Casing

## Load More Button

- Slug: `load-more-button`
- Family: `action`
- Source: https://vercel.com/geist/load-more-button
- Role: A full-width button used to append more items to a paginated list, with loading and styling variants.
- States: default, hover, active, disabled, loading, focus
- Props observed: none extracted
- Sections: Default, Loading, No Gap, No Border Radius, Custom Text

## Loading Dots

- Slug: `loading-dots`
- Family: `feedback`
- Source: https://vercel.com/geist/loading-dots
- Role: Indicate an action running in the background.
- States: info, success, warning, error, loading
- Props observed: size
- Sections: Default, With text, Best Practices, When to use, Behavior, Accessibility

## Menu

- Slug: `menu`
- Family: `navigation`
- Source: https://vercel.com/geist/menu
- Role: Dropdown menu opened via button. Supports typeahead and keyboard navigation.
- States: default, hover, active, focus, disabled
- Props observed: width, onClick, href, type, variant, text, size, username
- Sections: Default, With chevron, Disabled items, Locked items, Link items, Custom trigger

## MiddleTruncate

- Slug: `middle-truncate`
- Family: `content`
- Source: https://vercel.com/geist/middle-truncate
- Role: Truncates text in the middle, preserving the start and end of the string for maximum readability.
- States: default, hover, selected
- Props observed: key, value, max, min, onValueChange, disabled, checked, onChange
- Sections: Examples, Best Practices, When to use, Behavior, Accessibility

## Modal

- Slug: `modal`
- Family: `overlay`
- Source: https://vercel.com/geist/modal
- Role: Display popup content that requires attention or provides additional information.
- States: closed, opening, open, dismissed
- Props observed: onClick, size, active, onClickOutside, variant, prefix, initialFocusRef, ref
- Sections: Default, Sticky, Single button, Disabled actions, Inset, Control initial focus

## Multi Select

- Slug: `multi-select`
- Family: `input`
- Source: https://vercel.com/geist/multi-select
- Role: A keyboard-navigable dropdown for selecting multiple items with advanced focus management.
- States: default, hover, focus, disabled, error, selected
- Props observed: none extracted
- Sections: Select Actions, Keyboard Navigation, Controlled State, Best Practices, When to use, Behavior

## Note

- Slug: `note`
- Family: `feedback`
- Source: https://vercel.com/geist/note
- Role: Display text that requires attention or provides additional information.
- States: info, success, warning, error, loading
- Props observed: size, action, type, href, data-zone, key
- Sections: Default, Action, Success, Error, Warning, Secondary

## Pagination

- Slug: `pagination`
- Family: `navigation`
- Source: https://vercel.com/geist/pagination
- Role: Navigate to the previous or next page.
- States: default, hover, active, focus, disabled
- Props observed: next, previous
- Sections: Default, Best Practices

## Phone

- Slug: `phone`
- Family: `content`
- Source: https://vercel.com/geist/phone
- Role: The Phone component lets you showcase website screenshots or other content within a realistic phone-style frame.
- States: default, hover, selected
- Props observed: address
- Sections: Composition, Best Practices, When to use, Behavior, Accessibility

## Progress

- Slug: `progress`
- Family: `feedback`
- Source: https://vercel.com/geist/progress
- Role: Display progress relative to a limit or related to a task.
- States: info, success, warning, error, loading
- Props observed: value, max, colors, onClick, size, variant, type, stops
- Sections: Default, Custom max, Dynamic colors, Themed, With Stops, Widths

## Project Banner

- Slug: `project-banner`
- Family: `feedback`
- Source: https://vercel.com/geist/project-banner
- Role: Used for temporary, project-wide notifications that require resolution
- States: info, success, warning, error, loading
- Props observed: callToAction, key, icon, label, text, variant
- Sections: Default, Success, Warning, Error, Best Practices, When to use

## Radio

- Slug: `radio`
- Family: `input`
- Source: https://vercel.com/geist/radio
- Role: Provides single user input from a selection of options.
- States: default, hover, focus, disabled, error, selected
- Props observed: label, onChange, value, size, aria-label, checked
- Sections: Default, Radio disabled, Radio required, Radio headless, Radio standalone, Best Practices

## Relative Time Card

- Slug: `relative-time-card`
- Family: `surface`
- Source: https://vercel.com/geist/relative-time-card
- Role: Popover to show a given date in local time.
- States: default, hover, selected, disabled
- Props observed: date, side
- Sections: Default, Best Practices

## Scroller

- Slug: `scroller`
- Family: `navigation`
- Source: https://vercel.com/geist/scroller
- Role: Display an overflowing list of items.
- States: default, hover, active, focus, disabled
- Props observed: height, overflow, width, key, childrenContainerClassName
- Sections: Vertical, Horizontal, Free, Vertical with buttons, Horizontal with buttons, Best Practices

## Search Input

- Slug: `search-input`
- Family: `input`
- Source: https://vercel.com/geist/search-input
- Role: Pre-configured search input with a magnifying glass icon and clear button.
- States: default, hover, focus, disabled, error, selected
- Props observed: aria-label, onChange, placeholder, value, prefix
- Sections: Default, With Cmdk, Disabled, Loading, Custom Prefix

## Select

- Slug: `select`
- Family: `input`
- Source: https://vercel.com/geist/select
- Role: Display a dropdown list of items.
- States: default, hover, focus, disabled, error, selected
- Props observed: aria-label, placeholder, size, prefix, suffix, error, label, value
- Sections: Sizes, Prefix and suffix, Disabled, Error, Label, With options

## Separator

- Slug: `separator`
- Family: `layout`
- Source: https://vercel.com/geist/separator
- Role: A visual divider that separates content into distinct sections, with support for horizontal and vertical orientations.
- States: default, responsive
- Props observed: orientation, decorative
- Sections: Horizontal, Section 1, Section 2, Vertical, Orientation Variants, Accessibility Variants

## Sheet

- Slug: `sheet`
- Family: `overlay`
- Source: https://vercel.com/geist/sheet
- Role: Display content in a side panel that slides in from the edge of the screen.
- States: closed, opening, open, dismissed
- Props observed: noOverlay, variant, key, side
- Sections: Default, With Side, Best Practices, When to use, Behavior, Content

## Show more

- Slug: `show-more`
- Family: `content`
- Source: https://vercel.com/geist/show-more
- Role: Styling component to show expanded or collapsed content.
- States: default, hover, selected
- Props observed: expanded, onClick
- Sections: Default, Expanded, No border, Best Practices

## Skeleton

- Slug: `skeleton`
- Family: `feedback`
- Source: https://vercel.com/geist/skeleton
- Role: Display a skeleton whilst another component is loading.
- States: info, success, warning, error, loading
- Props observed: width, boxHeight, show, height, animated, variant
- Sections: Default with set width, Default with box height, Wrapping children, Wrapping children with fixed size, Pill, Rounded

## Slider

- Slug: `slider`
- Family: `input`
- Source: https://vercel.com/geist/slider
- Role: Input to select a value from a given range.
- States: default, hover, focus, disabled, error, selected
- Props observed: onValueChange, value
- Sections: Default, Range with inputs, Disabled range with inputs, Best Practices

## Snippet

- Slug: `snippet`
- Family: `content`
- Source: https://vercel.com/geist/snippet
- Role: Display a snippet of copyable code for the command line.
- States: default, hover, selected
- Props observed: text, width, prompt, onCopy, type
- Sections: Default, Inverted, Multi line, No prompt, Callback, Variants

## Spinner

- Slug: `spinner`
- Family: `feedback`
- Source: https://vercel.com/geist/spinner
- Role: Indicate an action running in the background. Unlike the loading dots, this should generally be used to indicate loading feedback in response to a user action, like for buttons, pagination, etc.
- States: info, success, warning, error, loading
- Props observed: size
- Sections: Default size, Sizes, Colors, Best Practices, When to use, Behavior

## Split Button

- Slug: `split-button`
- Family: `action`
- Source: https://vercel.com/geist/split-button
- Role: A button that offers a primary interaction coupled with a dropdown menu offering additional actions.
- States: default, hover, active, disabled, loading, focus
- Props observed: key, buttonProps, menuButtonLabel, menuItems, description, menuItemProps, title, menuProps
- Sections: Default, Menu Alignment, Icon, Title with Icon, Best Practices

## Status Dot

- Slug: `status-dot`
- Family: `feedback`
- Source: https://vercel.com/geist/status-dot
- Role: Display an indicator of deployment status.
- States: info, success, warning, error, loading
- Props observed: state
- Sections: Default, Label, Best Practices, When to use, Behavior, Content

## Switch

- Slug: `switch`
- Family: `input`
- Source: https://vercel.com/geist/switch
- Role: Choose between a set of options.
- States: default, hover, focus, disabled, error, selected
- Props observed: name, label, value, size, text, icon
- Sections: Default, Disabled, Sizes, Full width, Tooltip, Icon

## Table

- Slug: `table`
- Family: `data-display`
- Source: https://vercel.com/geist/table
- Role: A semantic HTML table component
- States: default, loading, empty, error, selected
- Props observed: key, colSpan, item
- Sections: Basic table, Striped table, Bordered table, Interactive table, Full featured table, Virtualized table

## Tabs

- Slug: `tabs`
- Family: `navigation`
- Source: https://vercel.com/geist/tabs
- Role: Display tab content.
- States: default, hover, active, focus, disabled
- Props observed: selected, setSelected, tabs, variant
- Sections: Default, Disabled, Disable specific tabs, With icons, Secondary, Best Practices

## Text With Copy Button

- Slug: `text-with-copy-button`
- Family: `action`
- Source: https://vercel.com/geist/text-with-copy-button
- Role: Display text alongside a button that copies the text to the clipboard.
- States: default, hover, active, disabled, loading, focus
- Props observed: successMessage, textLabel, textToCopy
- Sections: Default, With Small and Tertiary

## Textarea

- Slug: `textarea`
- Family: `input`
- Source: https://vercel.com/geist/textarea
- Role: Retrieve multi-line user input.
- States: default, hover, focus, disabled, error, selected
- Props observed: aria-label, placeholder, defaultValue, error, size, rows
- Sections: Default, Disabled, Error, Sizes, Read Only, Rows

## Theme Switcher

- Slug: `theme-switcher`
- Family: `input`
- Source: https://vercel.com/geist/theme-switcher
- Role: Component that allows users to switch between light and dark themes.
- States: default, hover, focus, disabled, error, selected
- Props observed: none extracted
- Sections: Default, Small, Disabled, Best Practices

## Toast

- Slug: `toast`
- Family: `feedback`
- Source: https://vercel.com/geist/toast
- Role: A succinct message that is displayed temporarily.
- States: info, success, warning, error, loading
- Props observed: onClick, data-zone, href, isDifferentZone
- Sections: Default, Multi-line, With jsx, With a link, Preserve, Action

## Toggle

- Slug: `toggle`
- Family: `input`
- Source: https://vercel.com/geist/toggle
- Role: Displays a boolean value.
- States: default, hover, focus, disabled, error, selected
- Props observed: aria-label, checked, onChange, size, color, icon, direction
- Sections: Default, Disabled, Sizes, Custom Color, With Label, Best Practices

## Tooltip

- Slug: `tooltip`
- Family: `overlay`
- Source: https://vercel.com/geist/tooltip
- Role: A set of headings, vertically stacked, that each reveal an related section of content. Commonly referred to as an accordion.
- States: closed, opening, open, dismissed
- Props observed: text, position, delay, boxAlign, type, size, tip, center
- Sections: Default, No delay, Box align, Custom content, Custom type, Components

## Video

- Slug: `video`
- Family: `content`
- Source: https://vercel.com/geist/video
- Role: Embed a video with built-in playback controls and lazy loading support.
- States: default, hover, selected
- Props observed: height, lazy, src, width, loop, controls
- Sections: Default, No Loop, No Controls
