#!/usr/bin/env python3
"""Check your NRP LLM token and endpoint, independent of Jupyter AI.

Inside the Lab 5 Pod the env vars are already set. On a laptop:
    pip install openai
    export OPENAI_API_KEY=<token> OPENAI_BASE_URL=https://ellm.nrp-nautilus.io/v1
    python test_nrp_llm.py [model]
"""
import os
import sys

from openai import OpenAI

client = OpenAI(base_url=os.environ.get("OPENAI_BASE_URL", "https://ellm.nrp-nautilus.io/v1"),
                api_key=os.environ["OPENAI_API_KEY"].strip())
model = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("NRP_MODEL", "gpt-oss")

print("Models:", ", ".join(sorted(m.id for m in client.models.list())))  # 401 = bad token
reply = client.chat.completions.create(
    model=model, max_tokens=200,
    messages=[{"role": "user", "content": "In one sentence, what is a Kubernetes Pod?"}])
print(f"\n{model}: {reply.choices[0].message.content}")
