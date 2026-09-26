set -e
cd /home/ubuntu/Bhuverify-pilot
sudo systemctl restart bhuverify-pilot
sleep 15
sudo systemctl is-active bhuverify-pilot
curl -s -o /dev/null -w "health:%{http_code}\n" http://127.0.0.1:8001/api/v1/health
./venv-pilot/bin/python -m pytest tests/ -q 2>&1 | tail -2
./venv-pilot/bin/python tools/run_stress.py --dir data/stress_hindi --glob "*" > /home/ubuntu/hindi-run.log 2>&1
tail -6 /home/ubuntu/hindi-run.log
./venv-pilot/bin/python tools/refetch.py --dir data/stress_hindi > /home/ubuntu/hindi-full.log 2>&1
tail -3 /home/ubuntu/hindi-full.log
./venv-pilot/bin/python tools/run_stress.py --dir data/stress_english --glob "*" > /home/ubuntu/eng-run.log 2>&1
tail -6 /home/ubuntu/eng-run.log
./venv-pilot/bin/python tools/refetch.py --dir data/stress_english > /home/ubuntu/eng-full.log 2>&1
tail -3 /home/ubuntu/eng-full.log
