# BentoShield

```bash
git clone https://github.com/bentoml/BentoShield.git && cd BentoShield

uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

```bash
bentoml serve .
```

```bash
curl -X 'POST' \
  'http://localhost:3000/generate' \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "prompt": "Create 20 paraphrases of I love you",
  "threshhold": 0.6
}'
```
