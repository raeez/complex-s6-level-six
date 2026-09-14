#!/usr/bin/env python3
"""Verify the exact wording delta and its preserved mathematical sources."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import zipfile

REPORT = Path(__file__).resolve().parent
ROOT = REPORT.parents[3]
SOURCE = ROOT / 'research-candidates/s6-marked-filling020'
NATIVE = REPORT / 'native-comparison/source'
OLD = b'This also specifies all maps in the requested adjacent degrees.'
NEW = b'These formulas specify the maps in every degree.'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def aggregate(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def main():
    composition = json.loads((REPORT / 'composition.json').read_text())
    changed = []
    proof_count = 0
    for row in composition:
        baseline = (ROOT / row['baseline']).read_bytes()
        candidate = (ROOT / row['candidate']).read_bytes()
        assert hashlib.sha256(baseline).hexdigest() == row['sha256'], row
        assert candidate == baseline.replace(OLD, NEW), row
        if baseline != candidate:
            assert baseline.count(OLD) == candidate.count(NEW) == 1
            changed.append(row['candidate'])
        proofs = lambda b: re.findall(rb'\\begin\{proof\}.*?\\end\{proof\}', b, re.S)
        assert proofs(candidate) == proofs(baseline), row
        proof_count += len(proofs(candidate))
        commands = lambda b: re.findall(rb'\\(?:label|ref|eqref)\{[^}]*\}', b)
        assert commands(candidate) == commands(baseline), row
    assert len(changed) == 2

    body = (SOURCE / 'paper.tex').read_text().split('\\end{abstract}', 1)[1].split('\\end{document}', 1)[0]
    body = re.sub(r'\\input\{([^}]+)\}', lambda m: (SOURCE / (m[1] + '.tex')).read_text(), body)
    body = re.sub(r'\\(label|ref|eqref)\{([^}]+)\}', lambda m: '\\' + m[1] + '{marked-local:' + m[2] + '}', body)
    assert body == (NATIVE / 'marked-filling.tex').read_text()

    preserved = json.loads((REPORT / 'preserved-inputs.json').read_text())
    old_root = Path(preserved['root'])
    with zipfile.ZipFile(ROOT / preserved['archive']['path']) as archive:
        for row in preserved['files']:
            path = old_root / row['path']
            assert sha(path) == row['sha256'] and len(path.read_bytes()) == row['bytes'], row
            assert archive.read(row['path']) == path.read_bytes(), row
    inherited = json.loads((old_root / 'reports/research/CONSTRUCTION-2026-09-14/s6-marked-filling002/preserved-inputs.json').read_text())['inputs']
    for row in inherited:
        path = Path(row['path'])
        assert sha(path) == row['sha256'] and len(path.read_bytes()) == row['bytes'], row

    build_comparison = json.loads((REPORT / 'build-comparison.json').read_text())
    render_comparison = json.loads((REPORT / 'render-comparison.json').read_text())
    for kind, candidate, pages, changed_page in [('standalone', SOURCE, 17, 12), ('native', NATIVE, 45, 39)]:
        baseline = REPORT / 'baseline' / kind
        assert (baseline / 'out/paper.aux').read_bytes() == (candidate / 'out/paper.aux').read_bytes()
        texts = []
        for name, folder in [('baseline', baseline), ('candidate', candidate)]:
            pdf = folder / 'out/paper.pdf'
            assert sha(pdf) == build_comparison[name + '-' + kind]['pdf_sha256']
            info = subprocess.check_output(['pdfinfo', str(pdf)], text=True)
            assert int(re.search(r'^Pages:\s+(\d+)', info, re.M)[1]) == pages
            text = subprocess.check_output(['pdftotext', '-layout', str(pdf), '-']).decode()
            assert text == (REPORT / (name + '-' + kind + '-text.txt')).read_text()
            texts.append(text)
            build = json.loads((REPORT / (name + '-' + kind + '-build.json')).read_text())
            assert build['converged'] and build['passes'][-1]['state'] == build['passes'][-2]['state']
        normal = lambda s: re.sub(r'\s+', ' ', s).strip()
        assert normal(texts[1]) == normal(texts[0]).replace(OLD.decode(), NEW.decode())
        assert render_comparison[kind]['changed_pages'] == [changed_page]
        for row in render_comparison[kind]['pages']:
            for name in ['baseline', 'candidate']:
                image = REPORT / 'render' / (name + '-' + kind) / ('page-%02d.png' % row['page'])
                assert sha(image) == row[name + '_sha256']

    manifest_path = REPORT / 'candidate-manifest.json'
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text())
        for row in manifest['all_changed_paths']:
            path = ROOT / row['path']
            assert sha(path) == row['sha256'] and len(path.read_bytes()) == row['bytes'], row
        assert aggregate(manifest['all_changed_paths']) == manifest['aggregate_changed_manifest_sha256']
        with zipfile.ZipFile(ROOT / manifest['source_archive']['path']) as archive:
            for row in manifest['source_closure']:
                assert archive.read(row['path']) == (ROOT / row['path']).read_bytes(), row
        inputs = json.loads((ROOT / manifest['build_inputs']['path']).read_text())
        for build in inputs.values():
            for row in build['inputs']:
                path = Path(row['path'])
                assert sha(path) == row['sha256'] and len(path.read_bytes()) == row['bytes'], row
            assert aggregate(build['inputs']) == build['aggregate_sha256']
    print(json.dumps({'source_files': len(composition), 'changed_reader_files': changed,
                      'complete_proof_environments_byte_identical': proof_count,
                      'predecessor_scope_files_unchanged': len(preserved['files']),
                      'inherited_preserved_inputs_unchanged': len(inherited),
                      'standalone_pages': 17, 'native_pages': 45,
                      'changed_raster_pages': {'standalone': [12], 'native': [39]},
                      'native_expansion_equal': True, 'result': 'PASS'}, indent=2))


if __name__ == '__main__':
    main()
