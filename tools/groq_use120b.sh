set -e
sed -i 's|^GROQ_MODEL=.*|GROQ_MODEL=openai/gpt-oss-120b|' /home/ubuntu/BhuSure-pilot/.env.pilot
grep GROQ_MODEL /home/ubuntu/BhuSure-pilot/.env.pilot
sudo systemctl restart bhusure-pilot
sleep 10
sudo systemctl is-active bhusure-pilot
cd /home/ubuntu/BhuSure-pilot && PYTHONPATH=. ./venv-pilot/bin/python tools/prove_groq.py
