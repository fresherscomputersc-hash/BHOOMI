curl -s http://169.254.169.254/latest/meta-data/instance-id; echo
grep -h PATH /etc/systemd/system/bhusure.service /etc/systemd/system/bhusure-pilot.service
cd /home/ubuntu/BhuSure && PATH=/home/ubuntu/BhuSure/venv/bin ./venv/bin/python -c "import shutil; print('live-PATH-which:', shutil.which('tesseract'))"
cd /home/ubuntu/BhuSure-pilot && PATH=/home/ubuntu/BhuSure-pilot/venv-pilot/bin ./venv-pilot/bin/python -c "import shutil; print('pilot-PATH-which:', shutil.which('tesseract'))"
