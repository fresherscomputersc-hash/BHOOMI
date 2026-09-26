set -e
grep -q /swap-pilot /etc/fstab || echo "/swap-pilot none swap sw 0 0" | sudo tee -a /etc/fstab
grep swap /etc/fstab
mkdir -p /home/ubuntu/backups
date=$(date +%Y%m%d-%H%M)
for db in /home/ubuntu/Bhuverify/data/bhuverify.db /home/ubuntu/Bhuverify-pilot/data/bhuverify.db; do
  if [ -f "$db" ]; then
    sqlite3 "$db" ".backup '/home/ubuntu/backups/$(basename $(dirname $(dirname $db)))-$date.db'" 2>/dev/null || cp "$db" "/home/ubuntu/backups/backup-$date-$(basename $(dirname $(dirname $db))).db"
  fi
done
ls -la /home/ubuntu/backups/
