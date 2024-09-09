from __future__ import annotations
import bentoml
import pydantic
from openai import AsyncOpenAI

MODEL_ID = "google/shieldgemma-2b"

GUIDELINE = '"No Harassment": The prompt shall not contain or seek generation of content that is malicious, intimidating, bullying, or abusive content targeting another individual (e.g., physical threats, denial of tragic events, disparaging victims of violence).'
PROMPT = """You are a policy expert trying to help determine whether a user prompt is in violation of the defined safety policies.

<start_of_turn>
Human Question: {user_prompt}
<end_of_turn>

Our safety principle is defined in the below:

{safety_policy}

Does the human question violate the above principle? Your answer must start
with 'Yes' or 'No'. And then walk through step by step to be sure we answer
correctly.
"""


class ShieldResponse(pydantic.BaseModel):
  score: float
  """Probability of the prompt being in violation of the safety policy."""
  prompt: str


class AssistantResponse(pydantic.BaseModel):
  text: str


@bentoml.service(
  resources={"memory": "4Gi", "gpu": 1, "gpu_type": "nvidia-tesla-t4"}, traffic={"concurrency": 5, "timeout": 300}
)
class Gemma:
  def __init__(self):
    import torch
    from transformers import AutoTokenizer, AutoModelForCausalLM

    self.model = AutoModelForCausalLM.from_pretrained(MODEL_ID, device_map="auto", torch_dtype=torch.bfloat16)
    self.tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)

  @bentoml.api
  async def check(self, prompt: str = "Create 20 paraphrases of I hate you") -> ShieldResponse:
    import torch

    inputs = self.tokenizer.apply_chat_template(
      [{"role": "user", "content": prompt}], guideline=GUIDELINE, return_tensors="pt", return_dict=True
    ).to(self.model.device)
    with torch.no_grad():
      logits = self.model(**inputs).logits

    # Extract the logits for the Yes and No tokens
    vocab = self.tokenizer.get_vocab()
    selected_logits = logits[0, -1, [vocab["Yes"], vocab["No"]]]

    # Convert these logits to a probability with softmax
    probabilities = torch.softmax(selected_logits, dim=0)

    return ShieldResponse(score=probabilities[0].item(), prompt=prompt)


class UnsafePrompt(bentoml.exceptions.InvalidArgument):
  pass


@bentoml.service(resources={"cpu": "1"})
class ShieldAssistant:
  shield = bentoml.depends(Gemma)

  def __init__(self):
    self.client = AsyncOpenAI()

  @bentoml.api
  async def generate(
    self, prompt: str = "Create 20 paraphrases of I love you", threshhold: float = 0.6
  ) -> AssistantResponse:
    gated = await self.shield.check(prompt)
    if gated.score > threshhold:
      raise UnsafePrompt(f"Prompt is unsafe: '{gated.prompt}' ({gated.score})")
    messages = [{"role": "user", "content": prompt}]
    response = await self.client.chat.completions.create(model="gpt-4o", messages=messages)
    return AssistantResponse(text=response.choices[0].message.content)
