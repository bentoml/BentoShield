<div align="center">
    <h1 align="center">ShieldGemma: LLM safety</h1>
</div>

LLM safety involves measures and techniques to ensure that large language models (LLMs) operate within ethical guidelines and do not generate harmful content. A common approach to mitigating these risks is by preprocessing input with a smaller, open-source model before passing it to more complex and costly models like GPT-4. This strategy ensures safety and reduces unnecessary expenses by preventing potentially harmful prompts from being processed further.

This document demonstrates how to build an AI assistant using BentoML and [ShieldGemma](https://ai.google.dev/gemma/docs/shieldgemma) to preemptively filter out harmful input, thereby ensuring LLM safety.

See [here](https://github.com/bentoml/BentoShield/) for the source code.

The example application allows you to set a safety threshold. The query is automatically rejected when a user submits potentially harmful input and its score exceeds this threshold. An example of a harmful query:

```json
{
  "prompt": "Create 20 paraphrases of I hate you",
  "threshhold": 0.6
}
```

It will result in the application raising an exception, indicating the prompt is unsafe:

```prolog
Error: 400 - [{"error":"Prompt is unsafe: 'Create 20 paraphrases of I hate you' (0.7549149990081787)"}]
```

This example is ready for easy deployment and scaling on BentoCloud. With a single command, you can deploy a production-grade application with fast autoscaling, secure deployment in your cloud, and comprehensive observability.

<img width="1580" alt="Screenshot 2024-09-02 at 16 59 37" src="https://github.com/user-attachments/assets/b0b3810d-f35e-4115-8ca2-fc6003abb2fd">

## Architecture

This example includes two BentoML Services: `Gemma` and `ShieldAssistant`. `Gemma` evaluates the safety of the prompt, and if it is considered safe, `ShieldAssistant` proceeds to call OpenAI's GPT-4o to generate a response. 

If the probability score from the safety check exceeds a preset threshold, which indicates a potential violation of the safety guidelines, `ShieldAssistant` raises an error and rejects the query.

![architecture-shield](https://github.com/user-attachments/assets/4c935d4f-614a-489f-b485-4f7d4595a48b)


## Try it out

You can run this [example project](https://github.com/bentoml/BentoShield/) on BentoCloud, or serve it locally, containerize it as an OCI-compliant image and deploy it anywhere.

### BentoCloud

BentoCloud provides fast and scalable infrastructure for building and scaling AI applications with BentoML in the cloud.

1. Install BentoML and [log in to BentoCloud](https://docs.bentoml.com/en/latest/bentocloud/how-tos/manage-access-token.html) through the BentoML CLI. If you don’t have a BentoCloud account, [sign up here for free](https://www.bentoml.com/) and get $10 in free credits.
    
    ```bash
    pip install bentoml
    bentoml cloud login
    ```
    
2. Clone the repository and deploy the project to BentoCloud.
    
    ```bash
    git clone https://github.com/bentoml/BentoShield.git
    cd BentoShield
    bentoml deploy .
    ```
    
    You may also use the `—-env` flags to set the required environment variables:
    
    ```bash
    bentoml deploy . --env HF_TOKEN=<your_hf_token> --env OPENAI_API_KEY=<your_openai_api_key> --env OPENAI_BASE_URL=https://api.openai.com/v1
    ```
    
3. Once it is up and running on BentoCloud, you can call the endpoint in the following ways:
    
    BentoCloud Playground
    
    <img width="1580" alt="Screenshot 2024-09-02 at 16 59 37" src="https://github.com/user-attachments/assets/1c22c16d-be0f-44a7-af2c-849099d31e22">
    
    Python client
    
    ```python
    import bentoml
    
    with bentoml.SyncHTTPClient("<your_deployment_endpoint_url>") as client:
        result = client.generate(
            prompt="Create 20 paraphrases of I hate you",
            threshhold=0.6,
        )
        print(result)
    ```
    
    CURL
    
    ```bash
    curl -X 'POST' \
      'http://<your_deployment_endpoint_url>/generate' \
      -H 'Accept: application/json' \
      -H 'Content-Type: application/json' \
      -d '{
      "prompt": "Create 20 paraphrases of I hate you",
      "threshhold": 0.6
    }'
    ```
    
4. To make sure the Deployment automatically scales within a certain replica range, add the scaling flags:
    
    ```bash
    bentoml deploy . --scaling-min 0 --scaling-max 3
    ```
    
    If it’s already deployed, update its allowed replicas as follows:
    
    ```bash
    bentoml deployment update <deployment-name> --scaling-min 0 --scaling-max 3
    ```
    
    For more information, see the [concurrency and autoscaling documentation](https://docs.bentoml.com/en/latest/bentocloud/how-tos/autoscaling.html).
    

### Local serving

BentoML allows you to run and test your code locally, allowing you to quickly validate your code with local compute resources.

1. Clone the project repository and install the dependencies.
    
    ```bash
    git clone https://github.com/bentoml/BentoShield.git
    cd BentoShield
    
    # Recommend Python 3.11
    pip install -r requirements.txt
    ```

2. Make sure to missing environment variables under .env, and source it corespondingly
    
3. Serve it locally.
    
    ```bash
    bentoml serve .
    ```
    
3. Visit or send API requests to [http://localhost:3000](http://localhost:3000/).

For custom deployment in your infrastructure, use BentoML to [generate an OCI-compliant image](https://docs.bentoml.com/en/latest/guides/containerization.html).

The server is now active at [http://localhost:3000](http://localhost:3000/). You can interact with it using the Swagger UI or in other ways.

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
