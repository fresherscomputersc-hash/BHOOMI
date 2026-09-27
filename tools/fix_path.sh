set -e
sudo sed -i 's|PATH=/home/ubuntu/BhuSure/venv/bin"|PATH=/home/ubuntu/BhuSure/venv/bin:/usr/local/bin:/usr/bin:/bin"|' /etc/systemd/system/bhusure.service
sudo sed -i 's|PATH=/home/ubuntu/BhuSure-pilot/venv-pilot/bin|PATH=/home/ubuntu/BhuSure-pilot/venv-pilot/bin:/usr/local/bin:/usr/bin:/bin|' /etc/systemd/system/bhusure-pilot.service
grep -h PATH /etc/systemd/system/bhusure.service /etc/systemd/system/bhusure-pilot.service
sudo systemctl daemon-reload
sudo systemctl restart bhusure bhusure-pilot
sleep 12
sudo systemctl is-active bhusure bhusure-pilot
cd /home/ubuntu/BhuSure && PATH=/home/ubuntu/BhuSure/venv/bin:/usr/local/bin:/usr/bin:/bin ./venv/bin/python -c "from app.services.ocr_service import TESSERACT_AVAILABLE, TESSERACT_VERSION, INSTALLED_LANGS; print('live-engine:', TESSERACT_AVAILABLE, TESSERACT_VERSION, tuple(INSTALLED_LANGS))"
cd /home/ubuntu/BhuSure-pilot && PATH=/home/ubuntu/BhuSure-pilot/venv-pilot/bin:/usr/local/bin:/usr/bin:/bin PYTHONPATH=. ./venv-pilot/bin/python -c "from app.services.ocr_service import TESSERACT_AVAILABLE, TESSERACT_VERSION, INSTALLED_LANGS; print('pilot-engine:', TESSERACT_AVAILABLE, TESSERACT_VERSION, tuple(INSTALLED_LANGS))"
