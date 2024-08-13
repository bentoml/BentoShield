# BentoShield

```bash
git clone https://github.com/bentoml/BentoShield.git && cd BentoShield

uv venv
cp .env.template .env
source .venv/bin/activate
uv pip install -r requirements.txt
```

edit `.env` and set `OPENAI_API_KEY` and `OPENAI_BASE_URL`:

```
HF_TOKEN=hf_x
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
OPENAI_BASE_URL=https://api.openai.com/v1
```

Start the server:

```bash
bentoml serve .
```

The server will be available at `http://localhost:3000`. An example request:

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
