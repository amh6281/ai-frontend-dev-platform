# Styling Rules

Use these rules when writing CSS, styling components, or adding visual variants. Take values from the existing design system before introducing new ones.

## Design Tokens

- Use existing tokens for color, spacing, typography, radius, shadow, z-index, motion, and breakpoints.
- Do not hard-code raw values when a token expresses the same intent.
- Add a token only when the value is reused and belongs to the system; keep one-off values local to the component.
- Prefer semantic tokens (`surface`, `muted`, `danger`) over raw palette references inside components.
- Support theming through tokens instead of per-component conditional color logic.

## Component Styling

- Follow the project's existing styling approach (CSS Modules, Tailwind, CSS-in-JS); do not introduce a second one.
- Keep styles next to the component they belong to, in the slice's `ui` segment.
- Express states through variants or data attributes rather than deeply nested selectors.
- Keep specificity flat; avoid `!important` and ID selectors.
- Do not style another component by reaching into its internals; expose a variant or slot instead.
- Prefer explicit props such as `variant`, `size`, and `tone` over open-ended `style` and `className` overrides on shared components.

## Layout And Spacing

- Prefer normal flow, flex, and grid over absolute positioning.
- Apply spacing with layout containers and `gap` instead of margins that leak across component boundaries.
- Use logical properties (`inline`, `block`) when the product supports right-to-left languages.
- Avoid fixed heights and widths for content that can grow; let text wrap and containers expand.
- Keep z-index values on a defined scale instead of inventing arbitrary large numbers.

## Responsive

- Design mobile-first and layer up with min-width breakpoints from the token scale.
- Use fluid sizing (`clamp`, percentages, `minmax`) before adding another breakpoint.
- Prefer container queries when a component's layout depends on its own available space.
- Keep interactive targets large enough for touch across layouts.
- Verify the change at the project's supported breakpoints and at 200% browser zoom.

## Motion

- Animate `transform` and `opacity`; avoid animating layout-affecting properties.
- Keep durations and easing on the token scale.
- Respect `prefers-reduced-motion` for non-essential animation.
- Tie motion to a state change users can observe; avoid decorative loops.

## Visual States

- Define hover, `focus-visible`, active, disabled, loading, selected, and error styles for interactive elements.
- Never remove focus outlines without an equally visible replacement.
- Do not rely on color alone; pair it with an icon, text, or shape.
- Keep disabled styling readable while still communicating that the control is unavailable.

## Verification

- Check contrast for text, icons, focus rings, and borders that convey state (see `accessibility.md`).
- Verify dark mode and other theme variants when the project supports them.
- Check the change at the smallest supported viewport and with unusually long content.
