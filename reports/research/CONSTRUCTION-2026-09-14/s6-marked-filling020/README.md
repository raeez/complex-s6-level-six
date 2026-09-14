# S6 exact wording candidate

The candidate replaces one sentence in each of two complete readers:

> These formulas specify the maps in every degree.

The predecessor sentence was: “This also specifies all maps in the requested adjacent degrees.”
The two changes occur at standalone `marked-comparison.tex:129` and native `marked-filling.tex:760`.
All other source bytes are identical to the preserved 002 source closure, including every complete proof body.
The standalone reader has 17 pages. The native comparison has 45 pages.

The two fresh mathematical reviews bind predecessor manifest
`2a8df4bdac7cc8f916e055c02a083fff26fd2175f5ab7da5a5e2288962242a0b`.
Their full returns remain in `preserved/`. Their bounded mathematical verdicts retain the explicit smooth reduction hypotheses.
They are not whole-candidate verdicts for this new manifest. Root alone owns acceptance.

## Reproduction

Run the commands from the assigned worktree root. Build each source to stable references and PDF bytes:

```sh
python3 research-candidates/s6-marked-filling020/build.py --directory reports/research/CONSTRUCTION-2026-09-14/s6-marked-filling020/baseline/standalone
python3 research-candidates/s6-marked-filling020/build.py --directory reports/research/CONSTRUCTION-2026-09-14/s6-marked-filling020/baseline/native
python3 research-candidates/s6-marked-filling020/build.py --directory research-candidates/s6-marked-filling020
python3 research-candidates/s6-marked-filling020/build.py --directory reports/research/CONSTRUCTION-2026-09-14/s6-marked-filling020/native-comparison/source
python3 reports/research/CONSTRUCTION-2026-09-14/s6-marked-filling020/verify.py
```

`commands-and-versions.json` records the exact commands and installed versions.
`build-inputs.json` records every resolved recorder input, its length, and its hash.
Each build uses recorder mode and disables shell escape. All four builds converged in four passes.
Both baselines reproduce the reviewed predecessor PDFs byte-for-byte.

`source-closure.zip` contains all 13 exact source-closure files. It stores resolved style bytes for archival custody.
The live source trees retain the exact original shared-template symlinks. No template content changed.
`new-source.patch` adds all 13 source paths, including both symlinks, under the two assigned candidate trees.
`wording-only.patch` isolates the two sentence replacements against the preserved baseline.
`native-comparison/unapplied-native.patch` reconstructs the complete native comparison against preserved native018 sources.
It is not an integration patch against current principal `paper.tex`. No patch was applied to either predecessor or principal.

## Verification and limits

`verification.json`, `source-delta-check.json`, and `render-comparison.json` contain the exact checks.
All 50 complete proof environments and every label/ref/eqref command are unchanged.
The native local body equals the expanded standalone body after only its original label namespace transformation.
Both auxiliary files remain identical to their respective baselines.
PDF text changes only on standalone page 12 and native page 39, by the exact prescribed sentence.
All 60 other PDF pages are byte-identical as complete 110 dpi PNG renders.
The two changed pages and both immediate transitions were visually inspected. The inspected page hashes are recorded.
The source, PDF text, and PDF metadata scans show no task wording or private paths under the recorded patterns.

The build advisories are unchanged: disabled shell escape in both readers, and the existing amsrefs citation-form advisory in the native comparison.
No overfull or underfull boxes, unresolved references, duplicate labels, missing glyphs, or hyperref token warnings occur.

All 171 predecessor files in the two assigned input scopes remain unchanged and have an exact preserved archive.
All 360 inherited preserved-input records verify. No files were staged, committed, or pushed.
All manuscript and report writes stayed within the assigned worktree. Worktree creation used the authorized Git command.

The mathematical prerequisites and residual obligations remain unchanged: smooth reduction and commuting lift, the other finite-order filling,
cusp chains and prisms, compatible common-chain comparisons, and global integral gluing.
This wording task establishes no new existence theorem, global homology, sphere topology, or complex structure.

`candidate-manifest.json` freezes all assigned files except itself. Its exact hash belongs in the external return.
Any subsequent byte change requires a new manifest and corresponding review.
