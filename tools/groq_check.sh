set -e
KEY=$(grep GROQ_API_KEY /home/ubuntu/BhuSure-pilot/.env.pilot | cut -d= -f2)
curl -s https://api.groq.com/openai/v1/models -H "Authorization: Bearer $KEY" -o /home/ubuntu/models.json
python3 -c "import json; ids=[m['id'] for m in json.load(open('/home/ubuntu/models.json'))['data']]; print('33-70b:', 'llama-3.3-70b-versatile' in ids, '| 31-8b-instant:', 'llama-3.1-8b-instant' in ids, '| total:', len(ids))"
cd /home/ubuntu/BhuSure-pilot && PYTHONPATH=. ./venv-pilot/bin/python tools/prove_groq.py
