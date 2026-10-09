# Accessibility statement

Zeta Zeros Lab is designed toward WCAG 2.2 Level AA, matching this maintainer's other
laboratories. This statement covers the public interactive site built from `site/`.

## What is supported

- Semantic landmarks, ordered headings, a skip link, descriptive page title, and visible
  keyboard focus.
- Full keyboard operation: every control is a native `<button>`; there is no drag-only interaction.
- The "which row is random?" exercise announces its result through `role="status" aria-live="polite"`,
  and the three rows have a text description, so the lesson does not depend on seeing the points.
- Every chart has a full accessible data table (histogram and pair correlation), always present in the
  DOM behind a keyboard-focusable disclosure, not hidden behind a script-only graphic.
- Verdicts are text ("Within GUE scatter", "Beyond GUE scatter", "GUE is closer"), never colour alone;
  the three series are distinguished by line style and a labelled legend as well as colour.
- The limitations panel appears **before** any chart, mirroring the reading-order discipline of this
  maintainer's other laboratories.
- High-contrast and forced-colour support; reduced-motion support; reflow to 320 CSS pixels and 200% text
  zoom without hiding navigation destinations.
- No autoplay, no flashing content, no time limits, no authentication walls.

## Verification

Every change passes semantic HTML assertions and `eslint-plugin-jsx-a11y`. The release
checklist also covers keyboard order, focus visibility, non-text alternatives, labels, zoom/
reflow, reduced motion, target size, and color-independent meaning. Automated checks cannot
prove accessibility or compatibility with every assistive-technology combination.

## Known limitations

- The charts are inherently visual; the data tables and the statistics table are the non-visual
  equivalents.
- Mathematical notation is expressed as Unicode and plain text rather than MathML.
- The interface and documentation are currently in English.

## Feedback

Open an accessibility issue at
https://github.com/lindgreendavid/zeta-zeros-lab/issues/new and include the page section,
browser, assistive technology, and expected behavior when possible. Security-sensitive reports
should use the private process in [`SECURITY.md`](SECURITY.md).

## Standard

The target is the W3C Web Content Accessibility Guidelines 2.2 Level AA:
https://www.w3.org/TR/WCAG22/. Conformance language is intentionally bounded: this is an
engineering statement and testing record, not a third-party accessibility certification.
