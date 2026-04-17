# Design System: High-End Editorial Real Estate

## 1. Overview & Creative North Star
**Creative North Star: "The Curated Monolith"**

This design system moves away from the "catalog" feel of traditional real estate platforms. It is built on the philosophy of a high-end architectural journal. We are not just listing properties; we are curating experiences. The "Curated Monolith" aesthetic relies on **intentional asymmetry**, where large-scale imagery is balanced by "over-sized" whitespace and staggered typography. We break the grid by allowing elements—like a property title or a gold-accented button—to bleed across the boundaries of a container, creating a sense of physical depth and bespoke craftsmanship.

## 2. Colors: Tonal Depth & Soul
The palette is a dialogue between the weight of Deep Charcoal and the luminescence of Soft Gold.

*   **Primary (`#0a0a0a`):** Used for the "Monolith" effect—heavy, grounding elements and authoritative text.
*   **Secondary (`#775a19`):** Our Soft Gold. This is not a utility color; it is an accent of light. Use it for signature moments: a property status, a bespoke icon, or a hover state that feels like a glimmer.
*   **Neutral Surfaces (`#f9f9f9` to `#ffffff`):** These provide the "Crisp White" canvas.

### The "No-Line" Rule
**Designers are strictly prohibited from using 1px solid borders to separate sections.**
Structural definition must be achieved through background shifts. For instance, a property description in `surface` should transition into a "Property Features" section using `surface-container-low`. This creates a seamless, architectural flow rather than a boxed-in "template" look.

### Surface Hierarchy & Nesting
Treat the UI as stacked sheets of fine gallery paper. 
*   **The Gallery Floor:** Use `surface` (`#f9f9f9`) as your base.
*   **The Pedestal:** Place property cards or search modules on `surface-container-lowest` (`#ffffff`) to create a natural, soft lift.
*   **The Inset:** Use `surface-container-high` (`#e8e8e8`) for utility areas (like a sidebar filter) to "recede" into the page.

### Signature Textures: The Gold Gradient
To provide a "professional polish" that flat colors lack, use a subtle linear gradient for primary CTAs or hero overlays:
*   **CTA Gradient:** Transition from `secondary` (`#775a19`) to `secondary_container` (`#fed488`) at a 135-degree angle. This mimics the way light hits a metallic gold leaf.

## 3. Typography: The Editorial Voice
We utilize a high-contrast pairing to evoke the feeling of a luxury magazine.

*   **Display & Headlines (Noto Serif / Sophisticated Serif):**
    These are your "hero" moments. Use `display-lg` (3.5rem) with tighter letter-spacing (-0.02em) to create an authoritative, "editorial" impact.
*   **Body & UI (Manrope / Clean Sans-Serif):**
    Manrope provides a geometric clarity that balances the serif’s ornamentation. Use `body-lg` (1rem) for property descriptions with a generous line-height (1.6) to ensure the text feels "expensive" and readable.
*   **The Label Intent:** 
    Use `label-md` in all-caps with increased letter-spacing (0.1em) for metadata like "SQUARE FOOTAGE" or "LOCATION." This adds a layer of technical precision to the elegant backdrop.

## 4. Elevation & Depth: Tonal Layering
Traditional drop shadows are too "software-like" for this brand. We use **Ambient Depth**.

*   **The Layering Principle:** Avoid shadows for static content. If a card needs to stand out, use a color shift (e.g., `surface-container-lowest` on a `surface` background).
*   **Ambient Shadows:** For floating elements (e.g., a "Schedule Viewing" sticky card), use a shadow with a 40px blur and only 4% opacity of the `on-surface` color. It should feel like a soft glow, not a dark smudge.
*   **The "Ghost Border":** If a boundary is required for accessibility, use the `outline-variant` token at **15% opacity**. This creates a "suggestion" of a line that disappears upon casual glance.
*   **Glassmorphism:** For navigation bars or image overlays, use `surface` at 80% opacity with a `20px` backdrop-blur. This allows the property photos to bleed through the UI, making the experience feel integrated and immersive.

## 5. Components

### Buttons: The Statement Pieces
*   **Primary:** High-contrast. `primary` background with `on-primary` text. Sharp corners (`sm` - 0.125rem) to maintain a modern, architectural feel.
*   **Secondary (The Gold Standard):** Use the Gold Gradient mentioned in Section 2. Reserved for high-conversion actions like "Inquire Now."
*   **Tertiary:** `on-surface` text with a 1px "Ghost Border" that transitions to a full `secondary` border on hover.

### Cards: The Property Showcase
*   **Styling:** No borders. Use `surface-container-lowest`. 
*   **Imagery:** Use a slight 1.05x scale on hover to give the property "life."
*   **Content:** Forbid divider lines. Separate the price, bed/bath, and location using vertical whitespace and `label-sm` typography.

### Input Fields: Minimalist Intention
*   **Style:** Underline only (using `outline-variant`) or a very subtle `surface-container-high` fill. 
*   **Focus State:** The underline transitions to `secondary` (Gold). No "blue glow" or thick strokes.

### Additional Component: The Property "Aperture"
*   A bespoke image gallery component that uses asymmetrical aspect ratios (e.g., a tall vertical image next to two small squares) to break the standard carousel format.

## 6. Do’s and Don’ts

### Do:
*   **Do** use asymmetrical layouts where text overlaps image edges by 20-40px.
*   **Do** lean into extreme whitespace. If a section feels "full," add 32px of extra padding.
*   **Do** use `secondary_fixed_dim` for subtle icons to keep them from competing with text.

### Don't:
*   **Don't** use standard "Material" blue for links. Everything is Charcoal, Gold, or White.
*   **Don't** use rounded corners above `0.5rem` (`lg`). High-end real estate is defined by clean, sharp architectural lines, not "bubbly" UI.
*   **Don't** use 100% black. Use the `primary` (`#0a0a0a`) Deep Charcoal to maintain softness and depth.