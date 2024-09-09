# BentoShield

<div align="center">
    <h1 align="center">Gated LLM with ShieldGemma, served with BentoML</h1>
</div>

This is a BentoML example project, showing you how to use ShieldGemma for safe generations.

See [here](https://github.com/bentoml/BentoML?tab=readme-ov-file#%EF%B8%8F-what-you-can-build-with-bentoml) for a full list of BentoML example projects.

## Prerequisites

- You have installed Python 3.9+ and `pip`. See the [Python downloads page](https://www.python.org/downloads/) to learn more.
- You have a basic understanding of key concepts in BentoML, such as Services. We recommend you read [Quickstart](https://docs.bentoml.com/en/1.2/get-started/quickstart.html) first.
- If you want to test the Service locally, we recommend you to have a Nvidia GPU with 80G VRAM.
- (Optional) We recommend you create a virtual environment for dependency isolation for this project. See the [Conda documentation](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html) or the [Python documentation](https://docs.python.org/3/library/venv.html) for details.

## Install dependencies

```bash
git clone https://github.com/bentoml/BentoShield.git && cd BentoShield

uv venv
cp .env.template .env
source .venv/bin/activate
uv pip install -r requirements.txt
```

Edit `.env` and set `OPENAI_API_KEY` and `OPENAI_BASE_URL`:

```
HF_TOKEN=hf_x
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
OPENAI_BASE_URL=https://api.openai.com/v1
```

## Run the BentoML Service

We have defined a BentoML Service in `service.py`. Run `bentoml serve` in your project directory to start the Service.

```bash
bentoml serve .
```

The server is now active at [http://localhost:3000](http://localhost:3000/). You can interact with it using the Swagger UI or in other different ways.

<details>

<summary>CURL</summary>

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

</details>

<details>

<summary>Python client</summary>

```python
import bentoml

with bentoml.SyncHTTPClient("http://localhost:3000") as client:
    response = client.generate(
        prompt="Create 20 paraphrases of I love you",
        threshhold=0.6,
    )
```

</details>
