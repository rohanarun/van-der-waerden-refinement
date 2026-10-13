"""Build, audit proof dependencies, and exercise rejection controls.

All disposable files are under this package's ignored receipts directory.
"""
import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from generate import ROOT, verify_sources


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--lake',default=os.environ.get('LAKE','lake'))
    parser.add_argument('--git-sources',action='store_true',help='also authenticate snapshots against Git objects')
    args=parser.parse_args()
    receipts=ROOT/'receipts';receipts.mkdir(exist_ok=True)
    def run(argv,name,success=True):
        proc=subprocess.run(argv,cwd=ROOT,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        (receipts/name).write_text(proc.stdout)
        if (proc.returncode==0)!=success:
            raise RuntimeError(f'Unexpected status {proc.returncode}: {argv}\n{proc.stdout}')
        return proc.stdout
    run([sys.executable,'-B','generate.py','--check'],'source-check.txt')
    manifest=json.loads((ROOT/'SOURCES.json').read_text())
    if args.git_sources:
        for row in manifest['files']:
            raw=subprocess.check_output(['git','show',row['commit']+':'+row['path']],cwd=ROOT)
            if raw!=(ROOT/row['snapshot']).read_bytes():
                raise ValueError('Git source mismatch: '+row['snapshot'])
    names=[]
    hashes={}
    for path in sorted((ROOT/'Vdw').glob('*.lean')):
        source=path.read_text()
        if re.search(r'\b(sorry|admit|axiom|native_decide|unsafe|implemented_by)\b|#eval',source):
            raise ValueError('Forbidden proof escape in '+str(path))
        names+=re.findall(r'^theorem ([A-Za-z0-9_]+)',source,re.M)
        hashes[str(path.relative_to(ROOT))]=hashlib.sha256(path.read_bytes()).hexdigest()
    if not names or len(names)!=len(set(names)): raise ValueError('Invalid theorem inventory')
    run([args.lake,'build'],'build.txt')
    audit=receipts/'PrintAxioms.lean'
    audit.write_text('import Vdw\n'+''.join('#print axioms Vdw.'+n+'\n' for n in names))
    output=run([args.lake,'env','lean',str(audit)],'axioms.txt')
    dependencies={}
    pattern=r"'Vdw\.([^']+)' (?:depends on axioms: \[([^]]*)\]|does not depend on any axioms)"
    for name,raw in re.findall(pattern,output,re.S):
        used=[a.strip() for a in raw.split(',') if a.strip()]
        if set(used)-{'propext','Classical.choice','Quot.sound'}:
            raise ValueError(f'Unexpected proof dependency: {name}: {used}')
        dependencies[name]=used
    if set(dependencies)!=set(names): raise ValueError('Incomplete axiom audit: '+output)
    controls={
        'invalid_strict_boundary': 'example : (2*(2/5)+1/5 : ℚ)<1 := by norm_num\n',
        'invalid_dilation_direction': 'example : (100 : ℚ)≤72 := by norm_num\n',
        'invalid_endpoint_coefficient': 'example : (2*(1/8) : ℚ)<(1/2)*(1/2) := by norm_num\n',
    }
    for name,body in controls.items():
        path=receipts/(name+'.lean');path.write_text('import Vdw\n'+body)
        log=run([args.lake,'env','lean',str(path)],name+'.txt',success=False)
        if 'unsolved goals' not in log:
            raise ValueError('Control failed for an unrelated reason: '+log)
    with tempfile.TemporaryDirectory(dir=receipts,prefix='source-control-') as folder:
        folder=Path(folder);row=manifest['files'][0]
        (folder/'SOURCES.json').write_text(json.dumps({'files':[row]}))
        p=folder/row['snapshot'];p.parent.mkdir(parents=True);p.write_bytes((ROOT/row['snapshot']).read_bytes()+b'changed')
        try: verify_sources(folder)
        except ValueError: pass
        else: raise ValueError('Altered source was accepted')
    version=run([args.lake,'env','lean','--version'],'lean-version.txt').strip()
    result={'scope':'Partial formal verification of explicitly listed obligations; not the complete van der Waerden theorems',
            'lean_version':version,'theorems':len(names),'axiom_dependencies':dependencies,
            'source_files':len(manifest['files']),'git_sources_checked':args.git_sources,
            'source_manifest_sha256':hashlib.sha256((ROOT/'SOURCES.json').read_bytes()).hexdigest(),
            'proof_sha256':hashes,'negative_controls_rejected':list(controls)+['altered_source'],
            'all_passed':True}
    (receipts/'verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(f'PASS: {len(names)} kernel-checked theorems, full axiom audit, four rejection controls.')
    print('Receipt: '+str(receipts/'verification.json'))


if __name__=='__main__':main()
