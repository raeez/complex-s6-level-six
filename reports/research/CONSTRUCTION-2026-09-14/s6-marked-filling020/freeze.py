#!/usr/bin/env python3
"""Record the exact assigned candidate without changing reader sources."""
import hashlib
import json
import os
from pathlib import Path
import subprocess

REPORT = Path(__file__).resolve().parent
ROOT = REPORT.parents[3]
SOURCE = ROOT / 'research-candidates/s6-marked-filling020'
NATIVE = REPORT / 'native-comparison/source'


def row(path):
    item = {'path': str(path.relative_to(ROOT)), 'bytes': len(path.read_bytes()),
            'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}
    if path.is_symlink():
        item.update(kind='symlink', target=os.readlink(path))
    return item


def aggregate(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


base = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
branch = subprocess.check_output(['git', 'branch', '--show-current'], cwd=ROOT, text=True).strip()
assert base == '5d9f632b5d9795e51075a9c15e2ee58d4cfb40af'
assert branch == 'intake/resume-s6-wording-020-20260914'
assert not subprocess.check_output(['git', 'diff', '--cached', '--name-only'], cwd=ROOT)
assert not subprocess.check_output(['git', 'diff', '--name-only'], cwd=ROOT)
manifest_path = REPORT / 'candidate-manifest.json'
files = sorted([row(p) for folder in [SOURCE, REPORT] for p in folder.rglob('*')
                if p.is_file() and p != manifest_path], key=lambda x: x['path'])
composition = json.loads((REPORT / 'composition.json').read_text())
inputs = json.loads((REPORT / 'build-inputs.json').read_text())
manifest = {
    'id': 's6-marked-filling020-wording-001', 'base_commit': base, 'branch': branch, 'worktree': str(ROOT),
    'predecessor_manifest_sha256': '2a8df4bdac7cc8f916e055c02a083fff26fd2175f5ab7da5a5e2288962242a0b',
    'reader_sources': [row(p) for folder in [SOURCE, NATIVE] for p in sorted(folder.glob('*.tex'))],
    'source_closure': [row(ROOT / x['candidate']) for x in composition],
    'source_archive': row(REPORT / 'source-closure.zip'),
    'source_patch': row(REPORT / 'new-source.patch'),
    'wording_patch': row(REPORT / 'wording-only.patch'),
    'native_patch': row(REPORT / 'native-comparison/unapplied-native.patch'),
    'pdf': row(SOURCE / 'out/paper.pdf'), 'page_count': 17,
    'native_comparison_pdf': row(NATIVE / 'out/paper.pdf'), 'native_comparison_pages': 45,
    'build_inputs': row(REPORT / 'build-inputs.json'),
    'build_input_aggregates': {k: v['aggregate_sha256'] for k, v in inputs.items()},
    'all_changed_paths': files, 'aggregate_changed_manifest_sha256': aggregate(files),
    'writer_verification': row(REPORT / 'verification.json'),
    'full_return': row(REPORT / 'full-return.md'),
    'preserved_scope_file_count': 171, 'preserved_inherited_input_count': 360,
    'scope': 'Two prescribed sentence replacements only. All other reader bytes and mathematical hypotheses are unchanged.',
    'mathematical_review_boundary': 'The preserved two-lane reviews bind the predecessor manifest. No new whole-candidate acceptance is asserted.',
    'independent_acceptance': 'Pending root review of this exact manifest.',
    'limits': 'No new existence, other-filling, cusp, common-chain, global-homology, sphere-topology, or complex-structure conclusion.',
    'self_hash_rule': 'Manifest excluded from its own list; exact SHA-256 reported externally.'}
manifest_path.write_text(json.dumps(manifest, sort_keys=True, indent=2) + '\n')
print(json.dumps({'manifest_sha256': hashlib.sha256(manifest_path.read_bytes()).hexdigest(),
                  'aggregate_changed_manifest_sha256': manifest['aggregate_changed_manifest_sha256'],
                  'changed_paths': len(files), 'reader_sources': len(manifest['reader_sources'])}, indent=2))
