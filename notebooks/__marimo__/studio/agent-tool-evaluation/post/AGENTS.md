# HTML starter instructions

Follow the `marimo-studio` skill for notebook ownership, projection selection,
view lifecycle, and validation. This file covers the browser-native project
supplied by this starter.

## Project intent

English follow-up to the author's confusion-matrix and softmax posts, published
at /blog/agent-tool-evaluation/. Preserve the author's conversational style,
first-person parser story and practical examples. Match the previous posts'
Montserrat headings, Noto Sans body, pastel header and reading width.
Assume the reader knows the confusion-matrix post. Extend its decision-level
evaluation into multi-turn, multi-tool scenarios. Link back for precision,
recall, the four outcomes and golden-set basics; do not reteach their formulas
or repeat the reject-everything accuracy example. Explain what changes here:
multilabel representation, per-tool support, micro/macro averaging, exact
tool-set matches, repeated calls, arguments, trajectories and final state.
The notebook owns all article prose, parser outputs, calculations and controls.
The view projects named cells and repeats only a static title, date and lead.
Keep the title cell for standalone notebook reading; do not project it here.

The supplied eval_tools lab is the source. The article now uses actual model
outputs from lab0.app.run(), captured by scripts/capture-tool-evaluation.py in
the supplied lab's Python environment. The lab's six source/dependency files
stay unchanged. The capture adds observation around run_agent only; it preserves
the original prompts, schemas, parsers, model generation defaults and tool code.

notebooks/assets/tool-evaluation/lab-observed.json contains the two recorded
parser runs, five Record scenarios, final snapshots, package versions, source
hashes and original metrics. lab-traces.json contains all 22 observed turns,
raw model responses, parsed calls, tool results and errors. lab-reference.json
is the original fixture/provenance snapshot, not a source of simulated outputs.
The download ZIP includes the six original source/dependency files, capture
script, results, traces, README and hashes. No MLX or LLM weights are needed
when building or viewing the blog: metrics are recomputed from captured calls.

Do not replace observations with reference replays or invented failures. Keep
all ten Prepared parser/scenario combinations working; default to results_broken
and the first scenario. The report compares all five scenarios for both parsers
and lets readers inspect each recorded turn and final snapshot.
At the parser story, show the broken run's full expected-vs-called matrix with
all five tools plus the lab's '-' row/column, outline the three write tools'
nothing-called cells, then highlight Happy path
turn 2 with its exact raw response, malformed arguments and TypeError.
Keep run metadata (capture time, package versions, timings) in lab-observed.json,
not in captions; on the page, keep only labels needed to read a visual. Clearly
separate the model choosing status instead of records from the parser losing
the lab order. The same record is marked and open in the scenario inspector.

Per-tool scores measure presence per turn; scenario scores count occurrences;
snapshots compare selected fields. Include attempted calls even when execution
fails, matching lab0.py. Preserve arguments/order and side-effect limitations.
The report shows the full matrix first, then the per-tool 2x2 matrices. The per-tool matrices are multilabel; arbitrary pairing of missing/extra names
is not causal alignment. Zero support is a coverage gap. An expected but absent
call is FN, not TN. The longest source fixture conflicts with the system-prompt
ordering rule; mention this limitation. The alternative-route example now uses
the corrected parser's observed full-workflow trajectory, not an invented replay.
Do not claim that the corrected parser makes every model decision correct.

This view reuses the established post.css styling and native marimo outputs.
No UnoCSS runtime, icon library or custom projection JavaScript is needed.
The two hand-drawn illustrations live under notebooks/assets/tool-evaluation:
tools-matrix-sketch and parser-workflow-sketch. Keep PNG originals and use the
1200px WebP copies on the page and in standalone notebook mo.image cells.
Embed each image once in authored HTML; do not project tools_matrix_illustration
or parser_workflow_illustration into Prepared states, which would repeat image
payloads. Alt text and captions must match the notebook and the image provenance
file (illustration-provenance.json). The matrix artwork is a conceptual sketch;
all measured counts stay in the existing native report. Preserve horizontally scrollable, keyboard-focusable report tables.
Assertions in scripts/check-tool-evaluation.py protect the educational examples.

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

The page uses the established local post.css and Google Fonts stylesheet.
Native marimo projections supply all interaction; add dependencies only if needed.

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

## Visual audit conventions

Keep inline prose/footer links underlined and zero-valued matrix cells legible
against the page background. Scrollable report regions need a visible keyboard
focus outline. The small authored fragment-link script preserves the current
document path and query because the exported directory base would otherwise
turn index.html fragment links into directory navigation in the Astro dev server.
It only updates the authored contents/skip links; notebook projections stay opaque.
