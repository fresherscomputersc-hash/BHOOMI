set -e
sed -i 's|^GROQ_MODEL=.*|GROQ_MODEL=openai/gpt-oss-120b|' /home/ubuntu/Bhuverify-pilot/.env.pilot
grep GROQ_MODEL /home/ubuntu/Bhuverify-pilot/.env.pilot
sudo systemctl restart bhuverify-pilot
sleep 10
sudo systemctl is-active bhuverify-pilot
cd /home/ubuntu/Bhuverify-pilot && PYTHONPATH=. ./venv-pilot/bin/python tools/prove_groq.py
