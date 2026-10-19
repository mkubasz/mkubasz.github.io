# Verification — 2026-10-19

## Source checks

- `scripts/check-from-data-to-model.py`: passed; 26 executed cells, six Prepared
  combinations, approximately 2,674 narrative/source words including examples.
- Confirmed manually specified promotion partitions, preservation of all 12 row
  IDs, six crossing groups in the intentionally bad split and none in the
  group/time split, chronological cutoffs and the three checkpoint decisions.
- `marimo check` and `git diff --check`: passed.
- The personal `mkubasz-technical-blog` skill passed skill-creator's validator.

## Build and export

- Prepared preflight verified all six combinations with no delivery diagnostics.
- `npm run notebooks`: passed for all four notebooks. An initial attempt during
  authoring stopped at the old confusion-matrix post with `notebook_changed`;
  the complete retry after source edits finished passed without changing old posts.
- `npm run build`: passed; Astro check reported zero errors/warnings/hints.
  Vite emitted an unused-import warning inside Astro's installed dependencies.
- Final static site served from `dist` at
  `http://127.0.0.1:4321/blog/from-data-to-model-1/`.

## Browser checks

- Exercised all six combinations in a staged export at 390 × 844. Verified the
  changed verdict, outlined ancestor, computed counts, partition sizes and all
  12 records after each update. No horizontal page overflow.
- Inspected desktop screenshots at 1280 × 900 and mobile screenshots at 390 × 844.
  Process map, checkpoint tree and dataset columns stack on mobile; body text
  remains 16px. Inspected both optimized illustrations.
- Verified native select focus, Tab/Shift+Tab traversal and keyboard type-ahead
  followed by Tab updating the checkpoint decision. Arrow-only automation did
  not commit an option; the committed keyboard path did.
- Final built route loaded with both images, default controls and the same
  presentation revision as the fully exercised export:
  `a28cd87d6ddc3aa9e477f7bf21612107a1c9b13f196bded9ebe90d345190ff35`.
- Contents links preserve the nested route and navigate to their target. No
  uncaught browser errors were reported. Later series parts are planned text.

Local browser-state evidence, export logs and inspected screenshots remain in
the ignored `.output/from-data-to-model-1-qa/` directory. The Astro development
server required `index.html` for this static asset; verification of the clean
directory route used the built site on a static HTTP server.

## Follow-up — model, tokenizer and dataset-split illustrations

- Added three original imagegen scenes, PNG originals and 1200 × 800 WebP
  delivery assets (481,448 bytes combined). Full prompts, alt text, captions
  and SHA-256 hashes are recorded in `illustration-prompts.json`.
- The view embeds all five illustrations exactly once. Standalone notebook
  image cells remain unprojected. The tokenizer caption distinguishes the paper
  metaphor from actual token boundaries; the split caption explains each role.
- Source checker passed: 31 executed cells, six combinations and approximately
  2,773 narrative/source words. `marimo check` and `git diff --check` passed.
- A full `npm run notebooks` attempt prepared the unchanged confusion-matrix
  post's 21 states but stopped while shutting down its managed marimo server.
  The changed post was then exported separately and passed all six Prepared
  states, with 19 projections and no delivery diagnostics. Astro build passed
  with zero check errors/warnings; the existing dependency import warning remains.
- The actual built HTTP route passed all six control combinations again.
  Inspected all three new illustrations and their captions at 1280 × 1000 and
  390 × 844: loaded at native width 1200, readable and without page overflow.
  Preserved 12 displayed records, the correct ancestor highlight, leakage counts,
  partition sizes and time status in every state.
- Verified presentation revision:
  `41df432008cb466daf626344d36179531c1c74e181f9fda2fadd7362fea8ab9c`.
  Evidence: `extra-illustrations-browser.json` and six `extra-*.png` screenshots
  in the same ignored QA directory.

## Follow-up — technical process visualizations

- Added notebook-owned figures for decoder-only inference, actual tokenization
  and promotion-family assignments. Model/tokenizer illustrations are optional
  native disclosures; the split process shares the existing dataset control.
- Reproduced the tokenizer fixture from an immutable SmolLM2-135M revision using
  tokenizers 0.22.1. SHA-256, IDs, offsets, individual pieces and complete decode
  agree. This loads a tokenizer and config only; no model inference or training.
- Expanded the source checker to verify rendered diagram assignments against
  partitions, family time order, tokenizer provenance and its round trip.
  Passed: 35 executed cells and all six Prepared combinations. `marimo check`
  and `git diff --check` passed.
- Export of the changed post passed: six Prepared states, 22 projections and no
  delivery diagnostics. `npm run build` passed; Astro check reported zero errors
  and warnings. The previously noted dependency import warning remains.
- Inspected the actual built HTTP page at 1280 × 1000 and 390 × 844. Verified
  four model stages become one column, ten token tiles wrap to two rows, and
  six promotion families stack vertically. No horizontal page overflow.
- Exercised all six combinations and checked every one of the twelve diagram
  assignments, the six/zero crossing families, partition sizes, row preservation
  and checkpoint ancestor. Token tiles match all ten saved IDs and pieces.
- Keyboard Enter opens/closes an illustrated analogy; type-ahead plus Tab changes
  the checkpoint. Contents links preserve the nested route and query.
- Verified presentation revision:
  `168c3c2b6f1ef92a8997e03da85d53e4b8c406d64d6e8e32359c86ccf2aa4924`.
  Evidence is in `technical-process-browser.json`, the export/build logs and
  inspected viewport screenshots whose filenames end in `-visible.png`.

## Follow-up — handwritten inference and CPT

- Added two imagegen technical sketches: input token IDs → fixed-weight model →
  decoded result, and domain text → next-token loss → parameter update W to W'.
  Manually checked labels, token IDs, arrow direction, identical CPT graph
  topology and conceptual weight changes. No measured weights/results appear.
- PNG originals, 1536 × 1024 WebPs, full prompts, captions, alt text and hashes
  are stored with the article. The seven illustration assets agree with their
  manifest and are embedded once each. New delivery images total 391,394 bytes.
- Split CPT/SFT prose so the CPT sketch sits after its introduction and before
  SFT. The detailed HTML inference flow remains available beneath the new
  sketch through a native keyboard-accessible disclosure.
- Source checks passed: 38 cells, six Prepared combinations, about 2,905 prose
  words. Fixed an extra opening newline flagged by marimo's Markdown linter;
  the final `marimo check --strict` has no diagnostics.
- Verified both new sketches over HTTP at 1280 × 1000 and 390 × 844, plus all
  six control combinations, seven illustration nodes, twelve data records and
  twelve diagram assignments. Confirmed CPT precedes SFT and Enter toggles the
  detailed inference flow in both layouts. Evidence: `handwritten-browser.json`
  and four `handwritten-desktop/mobile-*.png` screenshots.
- Small raster labels on phones can be inspected through Enlarge diagram.
  The presentation-only native modal retains the full 1536px image width in a
  scrollable viewport. Verified both diagrams on both viewport sizes: initial
  focus, Tab into the canvas, arrow-key scrolling, Escape/Close, focus return,
  background-scroll cleanup and absence of horizontal page overflow. Inspected
  `handwritten-mobile-zoom.png` and verified reactive split updates afterward.
- Final export reused the verified Prepared snapshot: 23 projections, with no
  delivery diagnostics. Final Astro build passed with zero check errors and
  warnings; the existing Vite dependency import warning remains.
- Final presentation revision:
  `3b86cd9402a57e4829796262338e049a23afabcf402f43e206fe22574db2071c`.
  Final modal evidence is in `handwritten-zoom-browser.json`; export/build logs
  use the `handwritten-zoom-` prefix in the ignored QA directory.

## Follow-up — review fixes (2026-10-19)

Applied the eleven review fixes. SFT and CPT get a one-sentence gloss at first
use in section 2; the inference figure says logits and section 6 defines them.
Section 6 now keeps its decision prose, the HTML inference flow inline, the
real token strip and the CPT sketch. The inference sketch and the model and
tokenizer scenes are no longer embedded in the notebook or view; their files
stay on disk. The split keeps the family diagram and counters, drops the three
record columns and shows data-split.webp inline above the control. Token tiles
are coloured by word, with a palette border per word so the groups stay
distinguishable. Section texts gained the deliberate worst-case sentence, the
Dwork et al. 2015 citation, "statistical precision", named metrics, the new
section 1 heading, the Pepper gloss and a 20–25 min reading time. "Fictional"
now appears four times, and captions without numbers no longer repeat "no
training/inference was run". A pre-existing markdown-indentation warning in
next_parts was fixed so `marimo check --strict` is clean. Source checker passed
with 35 cells, six combinations and about 2,824 prose words. The post export
prepared all six states with 23 projections and no delivery diagnostics;
`npm run build` reported zero errors, warnings and hints. On the `dist` preview
at 1280 × 900 and 390 × 844, every checkpoint and split combination produced the
expected ancestor, verdict, twelve assignments and six/zero crossing families,
with no horizontal overflow and no console errors. The CPT Enlarge dialog still
opens, closes and returns focus. Presentation revision:
`d14bd48403ae138999d10fed08db66c6a1c974cd62bee62a1b6e6fc035692e54`. Logs use the
`review-fixes-` prefix in the ignored QA directory.

## Follow-up — CPT for language adaptation (2026-10-19)

Section 6 now explains that CPT is the standard way to teach a checkpoint a
language and domain it saw rarely, tied to the four-piece *Czajnik* encoding.
Bielik 7B v0.1 is the worked example, read from its paper: Mistral 7B continued
on Polish text mixed with English, original tokenizer kept, SFT afterwards.
Elhady et al., ACL 2025 supports the forgetting caveat. No numbers or replay
shares are given, and sources.md has the new claim row. Two stale sources.md
lines about removed figures were corrected. Checker, `marimo check --strict`,
the post export with six states and no diagnostics, and `npm run build` with
zero errors, warnings and hints all passed. The paragraph and both links render
on the `dist` preview at 1280 × 900 and 390 × 844 without horizontal overflow or
console errors. Presentation revision:
`bd3c3a0a7b1c0fe37f1368802b0bb8fbca8c895c20fae11e7e059164601aea13`.
