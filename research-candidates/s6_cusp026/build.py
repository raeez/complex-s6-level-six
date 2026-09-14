"""Build the mathematical module and record exact inputs and diagnostics."""
import hashlib
import json
import os
from pathlib import Path
import subprocess

source = Path(__file__).resolve().parent
report = source.parents[1] / "reports/research/s6_cusp026"
output = report / "build"
output.mkdir(parents=True, exist_ok=True)
environment = os.environ.copy()
environment.update(SOURCE_DATE_EPOCH="1789344000", FORCE_SOURCE_DATE="1")
command = ["pdflatex", "-no-shell-escape", "-recorder", "-interaction=nonstopmode",
           "-halt-on-error", "-file-line-error", "-output-directory=" + str(output), "paper.tex"]
previous = None
passes = []
for number in range(1, 7):
    process = subprocess.run(command, cwd=source, env=environment,
                             stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    (output / f"pass-{number:02d}.log").write_bytes(process.stdout)
    if process.returncode:
        raise SystemExit(process.stdout.decode(errors="replace")[-8000:])
    state = {name: hashlib.sha256((output / name).read_bytes()).hexdigest()
             for name in ["paper.aux", "paper.out", "paper.pdf"] if (output / name).exists()}
    passes.append({"number": number, "exit_code": process.returncode, "state": state})
    if number >= 2 and state == previous:
        break
    previous = state
else:
    raise SystemExit("References and PDF did not converge in six passes")
log = (output / "paper.log").read_text(errors="replace")
fatal = ["undefined references", "multiply defined", "destination with the same identifier",
         "Missing character", "LaTeX Error", "Token not allowed", "Overfull"]
diagnostics = [line for line in log.splitlines() if any(item in line for item in fatal)]
if diagnostics:
    raise SystemExit("\n".join(diagnostics))
inputs = {}
for line in (output / "paper.fls").read_text().splitlines():
    if line.startswith("INPUT "):
        path = Path(line[6:])
        if not path.is_absolute():
            path = source / path
        path = path.resolve()
        if path.is_file() and not path.is_relative_to(output):
            inputs[str(path)] = hashlib.sha256(path.read_bytes()).hexdigest()
record = {"command": command, "source": str(source), "output": str(output),
          "environment": {key: environment[key] for key in ["SOURCE_DATE_EPOCH", "FORCE_SOURCE_DATE"]},
          "passes": passes, "input_sha256": inputs, "diagnostics": diagnostics,
          "pdf_sha256": state["paper.pdf"]}
(report / "build.json").write_text(json.dumps(record, indent=2) + "\n")
print(json.dumps({"passes": len(passes), "pdf_sha256": state["paper.pdf"],
                  "input_count": len(inputs), "diagnostics": diagnostics}, indent=2))
