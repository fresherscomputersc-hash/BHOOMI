set -e
KEY=$(grep GROQ_API_KEY /home/ubuntu/groq.env | cut -d= -f2)
echo "--- key format:" $(echo "$KEY" | cut -c1-7)...
echo "--- models check:"
curl -s https://api.groq.com/openai/v1/models -H "Authorization: Bearer $KEY" | head -c 600; echo
install -m 600 /home/ubuntu/groq.env /home/ubuntu/Bhuverify-pilot/.env.pilot
rm -f /home/ubuntu/groq.env
grep -q EnvironmentFile /etc/systemd/system/bhuverify-pilot.service || sudo sed -i '/^Environment=TMPDIR/a EnvironmentFile=/home/ubuntu/Bhuverify-pilot/.env.pilot' /etc/systemd/system/bhuverify-pilot.service
grep -h GROQ /etc/systemd/system/bhuverify-pilot.service || grep EnvironmentFile /etc/systemd/system/bhuverify-pilot.service
sudo systemctl daemon-reload
sudo systemctl restart bhuverify-pilot
sleep 10
sudo systemctl is-active bhuverify-pilot
