#!/usr/bin/env python3
"""Build a supplied manuscript to stable references without shell escape."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess

parser=argparse.ArgumentParser()
parser.add_argument('--directory',type=Path,default=Path(__file__).resolve().parent)
args=parser.parse_args()
source=args.directory.resolve()
output=source/'out'
output.mkdir(exist_ok=True)
environment=os.environ.copy()
environment.update(SOURCE_DATE_EPOCH='1789344000',FORCE_SOURCE_DATE='1')
command=['pdflatex','-no-shell-escape','-recorder','-interaction=nonstopmode',
         '-halt-on-error','-file-line-error','-output-directory=out','paper.tex']
previous=None
passes=[]
for turn in range(1,7):
    result=subprocess.run(command,cwd=source,env=environment,stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT)
    (output/('pass-%02d.log'%turn)).write_bytes(result.stdout)
    if result.returncode:
        raise SystemExit(result.stdout.decode(errors='replace')[-5000:])
    state={name:hashlib.sha256((output/name).read_bytes()).hexdigest()
           for name in ['paper.aux','paper.out','paper.toc','paper.pdf'] if (output/name).exists()}
    passes.append({'pass':turn,'exit_code':result.returncode,'state':state})
    if turn>=2 and state==previous:
        break
    previous=state
else:
    raise SystemExit('Reference/PDF state did not converge in six passes')
log=(output/'paper.log').read_text(errors='replace')
fatal=['undefined references','multiply defined','destination with the same identifier',
       'Missing character','LaTeX Error','Package hyperref Warning: Token not allowed']
bad=[line for line in log.splitlines() if any(item in line for item in fatal)]
if bad:
    raise SystemExit('\n'.join(bad))
print(json.dumps({'directory':str(source),'command':command,'environment':
                 {key:environment[key] for key in ['SOURCE_DATE_EPOCH','FORCE_SOURCE_DATE']},
                 'passes':passes,'converged':True,'final_pdf_sha256':state['paper.pdf']},indent=2))
