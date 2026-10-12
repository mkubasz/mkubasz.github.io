# HTML starter instructions

Follow the `marimo-studio` skill for notebook ownership, projection selection,
view lifecycle, and validation. This file covers the browser-native project
supplied by this starter.

## Project intent

English blog post for mkubasz.github.io, exported to /blog/agent-confusion-matrix/.
The notebook owns the entire article, synthetic fixtures, controls, metrics,
matrices and SVG charts. Project named cells into this view; do not duplicate
analytical prose in HTML. The static header repeats only the title, date and a
one-line lead so they survive without JavaScript; the notebook's `title` cell is
not projected. Preserve the author's conversational, practical style.
Match the previous softmax post: Montserrat headings, Noto Sans body and a pastel
header. Educational sketches use Caveat handwriting, navy irregular SVG strokes,
pastel blue/green/coral panels and responsive grids, as in the softmax post.
Sketch geometry and all numerical examples belong to notebook cells. Prose must remain available when the notebook is opened without Studio.
Define predictions on rows and reference labels on columns. ROC uses every
unique score; the slider selects an operating point without changing AUC.
The static examples share 20 positive and 80 negative toy cases. The interactive
example uses patient admission only, with one threshold slider (sticky in the
view, starting at 0.35), a score strip, a compact matrix, four metric cards
(recall, precision, FPR, accuracy) and ROC. Keep the illustrations before
numerical tables. Each sketch board and cartoon has one visible caption; do not
repeat it in prose. Avoid fixture metadata and cost charts. Section 7 has one
five-row decision log; add no other ledger.
Exercises sit in `/// details` blocks. Numbers quoted in prose and answers are
asserted in scripts/check-agent-evaluation.py; update both together.
Keep Markdown formulas on their own lines. Scope navigation classes to authored
navigation; the native Markdown output also uses a `contents` class.
Present the four decisions in each example under a `Decision` label, with one
bullet per outcome explaining the action, reference and consequence. The
investment example gives only TP and leaves the other three as an exercise.
Permission is a deterministic gate before email relevance scoring, and must be
rechecked before sending; its sketch lives in section 7, not in the email
section. Admission, relevance and suitability have distinct
reference labels. All scores are explicitly illustrative.
Prepare all 21 threshold positions for the single patient example. Numerical code stays in the notebook; the view only supplies layout.
Keep the notebook assets under notebooks/assets/agent-evaluation, including the
original cartoons and provenance. The standalone notebook renders cartoons with mo.image; the Studio view embeds
the same static cartoons once in HTML. Both use the 1200px WebP copies
(`cwebp -q 80 -resize 1200 0`), never the PNG originals; keep alt text and
captions identical in both places. Do not project the three comic cells into
Prepared states: repeating the large image payloads exhausts repository limits. No custom browser rendering or icon package is needed.

## Use the supplied Studio integration

`index.html` starts with one `<marimo-cell>` host for each enabled notebook cell
that may display output, including literal Markdown. Keep, reorder, group, or
replace those hosts as the page design develops. Their generated names remain
stable Studio targets for the notebook cells.

The starter defines `observeMarimoValue` inside the `index.html` module script.
Keep it inline or move it to a JavaScript file referenced directly from the
entry document. Use it when page JavaScript consumes a notebook value or eager
dataframe. Keep the corresponding `mo-value` host in authored HTML so Studio
can inspect and authorize its selector.

```html
<span id="rows-data" hidden mo-value="rows"></span>
```

```js
const source = document.querySelector("#rows-data");
if (source) {
  const stop = observeMarimoValue(source, {
    onValue: (rows) => renderRows(rows),
    onError: (error) => renderError(error.message),
  });
  window.addEventListener("pagehide", stop, { once: true });
}
```

Eager dataframes arrive as a shared Flechette `Table`. Use
[https://github.com/uwdata/flechette](https://github.com/uwdata/flechette) as
the table API reference. Treat the table as immutable. Keep data columnar with
`getChild()`, `select()`, and `toColumns()`. Call `toArray()` when browser code
needs row objects.

## Add dependencies

Add a browser dependency by referencing its URL from `index.html`, with a
`<script src>` tag or an `import` statement in a module script. Studio publishes
the page as written, so the next build picks up the new URL.

`index.html` loads two pinned browser dependencies from jsDelivr:

- [UnoCSS runtime](https://unocss.dev/integrations/runtime) with its default
  Wind3 preset. Use utility classes directly in authored HTML. The
  runtime observes DOM changes and generates matching styles in the browser.
- [Iconify Icon web component](https://iconify.design/docs/iconify-icon/).
  Add named icons with the registered `iconify-icon` element:

```html
<button type="button" class="inline-flex items-center gap-2">
  <iconify-icon inline icon="lucide:download" aria-hidden="true"></iconify-icon>
  Download
</button>
```

The scripts and Iconify API requests require browser network access. Configure
the hosting content security policy with `script-src` access to jsDelivr,
`connect-src` access to the configured Iconify API, and `style-src` permission
for the inline `<style>` element generated by UnoCSS. The style rule typically
requires `'unsafe-inline'`. Use precompiled project CSS when the hosting policy
permits only nonce or hash styles. Update the pinned URL and its integrity hash
together when changing either dependency.

Use these small defaults before adding another styling or icon dependency:

- Compose ordinary layout, spacing, responsive behavior, typography, borders,
  and states with UnoCSS utilities in the HTML.
- Keep authored CSS for the view's tokens, projection variables, complex
  selectors, data visualizations, keyframes, and print behavior.
- Use Iconify for interface icons. Keep repeated SVG markup and decorative
  Unicode characters out of controls. Keep a visible label or an accessible
  name on interactive controls.

Aim for a short stylesheet whose remaining rules express the view's own visual
system. Avoid copying utility-equivalent declarations into large selector
blocks.

Import browser-ready ESM modules at the top of the module script. Prefer a
versioned URL for maintained project source:

```js
import * as d3 from "https://cdn.jsdelivr.net/npm/d3@7/+esm";
```

Choose the URL form that matches the dependency source:

- Latest npm release for deliberate experiments:
  `import * as d3 from "https://cdn.jsdelivr.net/npm/d3/+esm";`
- Versioned npm package:
  `import * as d3 from "https://cdn.jsdelivr.net/npm/d3@7/+esm";`
- Concise statistical charts:
  `import * as Plot from "https://cdn.jsdelivr.net/npm/@observablehq/plot@0.6/+esm";`
- Tabular transformation:
  `import * as aq from "https://cdn.jsdelivr.net/npm/arquero@8/+esm";`
- Modular charting from an exported package subpath:
  `import * as echarts from "https://cdn.jsdelivr.net/npm/echarts@6/core/+esm";`
- CSV parsing from JSR through esm.sh:
  `import { parse as parseCsv } from "https://esm.sh/jsr/@std/csv";`

Remote modules require browser network access and a hosting content security
policy that allows the selected CDN. Keep all dependency origins explicit and
prefer versioned imports when the same source must rebuild consistently.

## Work within the HTML project

- Keep the document structure and projection hosts in `index.html`.
- Keep styles and browser behavior inline for a compact page, or reference CSS
  through `<link rel="stylesheet">` and JavaScript through `<script src>`
  directly from `index.html`. Studio copies these exact `.css`, `.js`, and
  `.mjs` source files into the browser artifact.
- Keep each direct source as a leaf file. Bundle or inline local CSS `url()` and
  `@import` dependencies and local JavaScript imports or re-exports. Explicit
  HTTPS, data, and fragment references remain available.
- Leave `<base href>` out of the entry document. HTTP and HTTPS dependency URLs
  need `//` and a host.
- Choose a provider that builds the JavaScript module graph for import maps,
  computed imports, and source-phase imports.
- Keep direct JavaScript within the pinned parser's accepted grammar. Inspection
  fails closed when it cannot establish the dependency boundary.
- End `break` and `continue` with `;` when another statement follows. The pinned
  grammar rejects a following regex statement when automatic semicolon
  insertion separates it from the restricted statement.
- The pinned grammar rejects import attributes on re-export statements. Import
  the remote module with its attributes, then use
  `export { value as default }` to preserve a default re-export. Enumerate named
  exports or choose a graph-building provider for a wildcard re-export.
- Keep projection hosts inside `#app-shell`.
- Inline project-owned images and fonts with the document. External HTTP URLs
  and `data:` URLs remain available.
- Use browser APIs for focused interaction. Choose the React or Svelte starter
  when the page needs component compilation, a local import graph, or separate
  browser assets.

Studio publishes the entry document and its declared local sources after
validating the HTML and projection hosts. Treat the built artifact as the
acceptance boundary for the page.

## Link custom results to notebook inputs

Keep projection hosts explicit in authored source. Custom regions need every
kernel input, a readable label, and a rendering-source reference such as
`{"path":"index.html"}`. Keep these attributes on authored elements outside
native output subtrees. Follow the installed Studio skill's
`references/projections.md` for the shared contract:

```python
import marimo_studio

print(marimo_studio.agent.skill().file("references/projections.md").read_text())
```

## Maintain project ignore rules

You own this view project's `.gitignore`. When adding libraries, extensions, or
build tools, ignore their generated files, caches, local configuration, and
secrets. Keep authored source, dependency manifests, and lockfiles tracked.
Studio supplies workspace rules for its own artifacts and locks. Check
`git status --short --ignored` after running new tooling and update the view's
ignore rules before committing.
