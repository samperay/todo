from pathlib import Path
import re,ast,sys
root=Path(__file__).resolve().parent
mds=list(root.rglob('*.md'));errors=[]
for f in mds:
 s=f.read_text()
 for m in re.finditer(r'(?<!!)\[[^]]+\]\(([^)]+)\)',s):
  target=m.group(1).split('#')[0]
  if target and not target.startswith(('https:','http:','mailto:')) and not (f.parent/target).exists():errors.append(f'{f.relative_to(root)} broken link: {target}')
 for token in ('{commands}','{outcome}','{failure}','{caveat}','{i:02}','{slug}'):
  if token in s:errors.append(f'{f.relative_to(root)} unresolved: {token}')
for p in (root/'labs/module-experiments').glob('*.py'):
 try:ast.parse(p.read_text())
 except SyntaxError as e:errors.append(f'{p}: {e}')
print('Markdown files:',len(mds),'module experiments:',len(list((root/'labs/module-experiments').glob('*.py'))),'issues:',len(errors))
for e in errors[:50]:print(e)
sys.exit(bool(errors))
