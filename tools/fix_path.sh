set -e
sudo sed -i 's|PATH=/home/ubuntu/Bhuverify/venv/bin"|PATH=/home/ubuntu/Bhuverify/venv/bin:/usr/local/bin:/usr/bin:/bin"|' /etc/systemd/system/bhuverify.service
sudo sed -i 's|PATH=/home/ubuntu/Bhuverify-pilot/venv-pilot/bin|PATH=/home/ubuntu/Bhuverify-pilot/venv-pilot/bin:/usr/local/bin:/usr/bin:/bin|' /etc/systemd/system/bhuverify-pilot.service
grep -h PATH /etc/systemd/system/bhuverify.service /etc/systemd/system/bhuverify-pilot.service
sudo systemctl daemon-reload
sudo systemctl restart bhuverify bhuverify-pilot
sleep 12
sudo systemctl is-active bhuverify bhuverify-pilot
cd /home/ubuntu/Bhuverify && PATH=/home/ubuntu/Bhuverify/venv/bin:/usr/local/bin:/usr/bin:/bin ./venv/bin/python -c "from app.services.ocr_service import TESSERACT_AVAILABLE, TESSERACT_VERSION, INSTALLED_LANGS; print('live-engine:', TESSERACT_AVAILABLE, TESSERACT_VERSION, tuple(INSTALLED_LANGS))"
cd /home/ubuntu/Bhuverify-pilot && PATH=/home/ubuntu/Bhuverify-pilot/venv-pilot/bin:/usr/local/bin:/usr/bin:/bin PYTHONPATH=. ./venv-pilot/bin/python -c "from app.services.ocr_service import TESSERACT_AVAILABLE, TESSERACT_VERSION, INSTALLED_LANGS; print('pilot-engine:', TESSERACT_AVAILABLE, TESSERACT_VERSION, tuple(INSTALLED_LANGS))"
