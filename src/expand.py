# Expand source-link macros against pinned repo trees, failing loudly on any path that does not exist.
#   {{s:owner/repo:path|label}}  file or directory at the pinned commit
#   {{r:owner/repo|label}}       repository home
#   {{w:owner/repo|label}}       Google Code Wiki page for the repository
import re, sys, os
T = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'trees')
cache, missing = {}, []
def load(repo):
    if repo not in cache:
        f = os.path.join(T, repo.replace('/', '_'))
        if not os.path.exists(f + '.sha'):
            missing.append('NO TREE ' + repo); cache[repo] = None
        else:
            full, sha = open(f + '.sha').read().split()
            paths = [p for p in open(f + '.txt').read().split('\n') if p]
            cache[repo] = (full, sha, set(paths), paths)
    return cache[repo]
def sub(m):
    kind, body = m.group(1), m.group(2)
    target, _, label = body.partition('|')
    if kind == 's':
        repo, _, path = target.partition(':')
        info = load(repo)
        if not info: return label
        full, sha, pset, plist = info
        path = path.rstrip('/')
        if path not in pset:
            missing.append(f'{repo}:{path}'); return label
        is_dir = any(p.startswith(path + '/') for p in plist)
        return f'<a class="src" href="https://github.com/{full}/{"tree" if is_dir else "blob"}/{sha}/{path}">{label}</a>'
    info = load(target)
    full = info[0] if info else target
    if kind == 'r':
        return f'<a class="src repo" href="https://github.com/{full}">{label}</a>'
    return f'<a class="src cw" href="https://codewiki.google/github.com/{full}">{label}</a>'
src = sys.stdin.read()
out = re.sub(r'\{\{([srw]):([^}]+)\}\}', sub, src)
if missing:
    sys.stderr.write('MISSING:\n  ' + '\n  '.join(missing) + '\n'); sys.exit(1)
sys.stdout.write(out)
