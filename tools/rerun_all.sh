set -e
cd /home/ubuntu/BhuSure-pilot
sed -i 's/^GROQ_ENABLED=.*/GROQ_ENABLED=0/' .env.pilot
sudo systemctl restart bhusure-pilot
sleep 12
sudo systemctl is-active bhusure-pilot
./venv-pilot/bin/python tools/run_stress.py --dir data/stress --glob "stress_*" > /home/ubuntu/stress-run2.log 2>&1
tail -3 /home/ubuntu/stress-run2.log
./venv-pilot/bin/python tools/refetch.py --dir data/stress > /home/ubuntu/stress-full3.log 2>&1
./venv-pilot/bin/python tools/run_stress.py --dir data/realror --glob "*" > /home/ubuntu/realror-run2.log 2>&1
tail -3 /home/ubuntu/realror-run2.log
./venv-pilot/bin/python tools/refetch.py --dir data/realror > /home/ubuntu/realror-full2.log 2>&1
tail -5 /home/ubuntu/realror-full2.log
sed -i 's/^GROQ_ENABLED=.*/GROQ_ENABLED=1/' .env.pilot
sudo systemctl restart bhusure-pilot
sleep 10
sudo systemctl is-active bhusure-pilot
