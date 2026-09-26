curl -s http://169.254.169.254/latest/meta-data/instance-id; echo
grep -h PATH /etc/systemd/system/bhuverify.service /etc/systemd/system/bhuverify-pilot.service
cd /home/ubuntu/Bhuverify && PATH=/home/ubuntu/Bhuverify/venv/bin ./venv/bin/python -c "import shutil; print('live-PATH-which:', shutil.which('tesseract'))"
cd /home/ubuntu/Bhuverify-pilot && PATH=/home/ubuntu/Bhuverify-pilot/venv-pilot/bin ./venv-pilot/bin/python -c "import shutil; print('pilot-PATH-which:', shutil.which('tesseract'))"
