set -e
KEY=$(grep GROQ_API_KEY /home/ubuntu/Bhuverify-pilot/.env.pilot | cut -d= -f2)
curl -s https://api.groq.com/openai/v1/models -H "Authorization: Bearer $KEY" -o /home/ubuntu/models.json
python3 -c "import json; [print(m['id'], m.get('context_window')) for m in json.load(open('/home/ubuntu/models.json'))['data']]"
