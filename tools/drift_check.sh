set -e
cd /home/ubuntu/Bhuverify-pilot
drift=""
while read -r hash path; do
  path="${path%$'\r'}"
  [ -z "$path" ] && continue
  if [ ! -f "$path" ]; then
    echo "MISSING $path"
    drift="$drift $path"
  elif [ "$(tr -d '\r' < "$path" | md5sum | cut -d' ' -f1)" != "$hash" ]; then
    echo "DRIFT $path"
    drift="$drift $path"
  fi
done < /home/ubuntu/ec2_manifest.txt
echo "DRIFTED:$drift"
