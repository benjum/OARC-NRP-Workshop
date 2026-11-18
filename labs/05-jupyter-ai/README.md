---
title: "Lab 5: Jupyter AI + NRP LLMs"
nav_order: 6
permalink: /labs/05-jupyter-ai/
---

# Lab 5: Jupyter AI (Jupyternaut) with NRP's hosted LLMs

**Goal:** run JupyterLab with Jupyternaut connected to NRP's OpenAI-compatible endpoint (`https://ellm.nrp-nautilus.io/v1`), with your token stored as a Kubernetes **Secret**.
**Needs:** the PVC from Lab 2, and an **NRP LLM token** from the NRP portal. Your account must be in an LLM-enabled group.

### 1. Store your token as a Secret

```bash
kubectl create secret generic nrp-llm-$ME --from-literal=OPENAI_API_KEY=<YOUR_TOKEN>
kubectl label secret nrp-llm-$ME owner=$ME
```

The YAML only *references* the Secret, so the token never appears in a file.

> ⚠️ In a shared namespace, other members may be able to read Secrets. Delete yours at the end of the workshop.

### 2. Start the Pod (free port 8888 first)

```bash
kubectl delete pod jupyter-$ME --ignore-not-found
kubectl apply -f labs/05-jupyter-ai/jupyter-ai-pod.yaml
kubectl logs -f jupyter-ai-$ME     # wait ~2 min for the install, then copy the ?token= URL
```

### 3. Port-forward and chat

```bash
kubectl port-forward pod/jupyter-ai-$ME 8888:8888
```

1. Open the URL from step 2.
2. Open the Jupyter AI chat from the left sidebar.
3. The model is already set to `openai/gpt-oss`. You can check this in **Settings → Jupyternaut Settings**.
4. Mention **@Jupyternaut** in your message, for example:
   `@Jupyternaut write a cell that plots work/results/pvc-run1/sweep.csv`

Jupyternaut is an agent: it can edit files and notebooks in this Pod, so review its changes.

### If it doesn't answer

Test the token and endpoint directly:

```bash
kubectl cp labs/05-jupyter-ai/test_nrp_llm.py "jupyter-ai-${ME}:/home/jovyan/test_nrp_llm.py"
kubectl exec jupyter-ai-$ME -- python /home/jovyan/test_nrp_llm.py
```

| Symptom | Fix |
|---|---|
| `CreateContainerConfigError` | Create the Secret (step 1) |
| `401` | Bad token or pasted whitespace. Recreate the Secret |
| `403` | Account not LLM-enabled. Ask your namespace admin or NRP Matrix support |
| Model not found | Pick an ID from the test script's list and set `NRP_MODEL` in the YAML |

**Cleanup:** `kubectl delete pod jupyter-ai-$ME; kubectl delete secret nrp-llm-$ME`
