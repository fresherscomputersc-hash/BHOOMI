set -e
cd /home/ubuntu/BhuSure-pilot
sed -i 's/^GROQ_ENABLED=.*/GROQ_ENABLED=0/' .env.pilot
grep GROQ_ENABLED .env.pilot
sudo systemctl restart bhusure-pilot
sleep 12
sudo systemctl is-active bhusure-pilot
./venv-pilot/bin/python tools/run_stress.py --dir data/realror --glob "*" > /home/ubuntu/realror-run.log 2>&1
tail -6 /home/ubuntu/realror-run.log
./venv-pilot/bin/python tools/refetch.py --dir data/realror > /home/ubuntu/realror-full.log 2>&1
tail -30 /home/ubuntu/realror-full.log
sed -i 's/^GROQ_ENABLED=.*/GROQ_ENABLED=1/' .env.pilot
sudo systemctl restart bhusure-pilot
sleep 10
sudo systemctl is-active bhusure-pilot
grep GROQ_ENABLED .env.pilot
