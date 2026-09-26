set -e
cd /home/ubuntu/Bhuverify-pilot
mkdir -p data/realror
mv tools/upload_staging_tmp/488.pdf tools/upload_staging_tmp/4-19.pdf tools/upload_staging_tmp/313.pdf tools/upload_staging_tmp/72.pdf tools/upload_staging_tmp/4558.pdf data/realror/
mv tools/upload_staging_tmp/run_stress.py tools/upload_staging_tmp/refetch.py tools/
rmdir tools/upload_staging_tmp
ls -la data/realror
./venv-pilot/bin/python tools/refetch.py --dir data/stress > /home/ubuntu/stress-full.log 2>&1
cat /home/ubuntu/stress-full.log
