set -e
python3 -c "
lines = open('/etc/fstab').read().splitlines()
seen, out = set(), []
for ln in lines:
    if ln in seen and ln.strip():
        continue
    seen.add(ln)
    out.append(ln)
open('/tmp/fstab.new', 'w').write('\n'.join(out) + '\n')
"
sudo cp /tmp/fstab.new /etc/fstab
grep -n swap-pilot /etc/fstab
sudo systemctl daemon-reload
echo fstab-ok
