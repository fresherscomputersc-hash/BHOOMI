set -e
fc-list | grep -ci lohit || true
if ! fc-list | grep -qi lohit-odia; then
  echo "installing lohit fonts..."
  sudo apt-get update -qq
  sudo apt-get install -y -qq fonts-lohit-deva fonts-lohit-orya
  fc-cache -f >/dev/null 2>&1 || true
fi
fc-list | grep -i lohit | head -4
cd /home/ubuntu/BhuSure-pilot
./venv-pilot/bin/python tools/stress_docs.py --out data/stress
ls -la data/stress
