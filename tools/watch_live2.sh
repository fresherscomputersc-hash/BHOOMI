set -e
cd /home/ubuntu/Bhuverify
for i in 1 2 3 4 5 6 7 8; do
  sleep 30
  code=$(curl -s -o /dev/null -w '%{http_code}' http://127.0.0.1:8000/api/v1/health)
  rev=$(git log --oneline -1)
  echo "poll $i: $code $rev"
done
sudo systemctl is-active bhusure bhuverify
