---
title: Home
nav_order: 1
permalink: /
---

# Computing on the National Research Platform (NRP): Hands-on Labs

| Lab | What you do | Kubernetes ideas |
|---|---|---|
| [1. ML script in a Pod](labs/01-ml-pod/README.md) | Run `ml/train.py` in an interactive Pod | Pod, image, requests and limits, `apply`/`get`/`describe`/`exec` |
| [2. Results on a PVC](labs/02-pvc/README.md) | Save results, delete the Pod, recover them | PersistentVolumeClaim, `kubectl cp` |
| [3. Jupyter in a Pod](labs/03-jupyter/README.md) | Analyze the results in JupyterLab | `port-forward`, `logs`, a PVC shared by two Pods |
| [4. Pod → Job](labs/04-job/README.md) | Run the same work unattended | Job, ConfigMap |
| [5. Jupyter AI + NRP LLMs](labs/05-jupyter-ai/README.md) | Chat with Jupyternaut backed by NRP models | Secret, environment variables |

Labs 2 to 5 share one PVC, so do Lab 2 first.

## Get the materials

```bash
git clone {{ site.github.clone_url }}
```
```bash
cd {{ site.github.repository_name }}
```

Or [download the ZIP]({{ site.github.zip_url }}) and unzip it.

## Setup (once)

You need NRP access to the workshop namespace, `kubectl` with the NRP config, and a passing `kubectl get pods -n <namespace>` ("No resources found" is a pass). Lab 5 also needs an NRP LLM token.

Run everything from the repo folder. Everyone shares one namespace, so first give your resources unique names:

```bash
kubectl config set contexts.nautilus.namespace ucla-oarc-nrp-workshop
```
The following will personalize an OWNER attribute to your resources' config files. (`# Windows PowerShell: .\personalize.ps1 jsmith`)
```bash
./personalize.sh jsmith
```
And set an environment variable for later commands (`# Windows PowerShell: $ME = "jsmith"`)
```bash
export ME=jsmith
```

The lab commands use `$ME`. Set it again in any new terminal. On Windows, WSL or Git Bash avoids PowerShell quoting quirks.

## Slurm → Kubernetes

| Slurm | NRP / Kubernetes |
|---|---|
| Waiting in a queue | Scheduler places a Pod wherever its **requests** fit; otherwise it stays `Pending` |
| `salloc` + shell | Interactive Pod + `kubectl exec -it` |
| `sbatch` | Job |
| `module load` | Container image |
| `--cpus-per-task`, `--mem`, `--gres=gpu:1` | `requests`/`limits`, `nvidia.com/gpu: 1` |
| Project directory | PVC |
| `squeue` / `scontrol` / `slurm-*.out` | `kubectl get` / `describe` / `logs` |

## NRP policies to know

- A Pod without a controller is **interactive**: 6-hour maximum, at most 2 GPUs, 32 GB RAM, and 16 cores.
- Limits must be within **20%** of requests.
- **Never `sleep` in a Job** (bannable). Deployments can't request GPUs.
- Never install pip/conda packages onto CephFS volumes.
- Delete what you aren't using.

## Debugging loop

Look for pods status (Pending / ImagePullBackOff / CrashLoopBackOff / OOMKilled)
```bash
kubectl get pods 
```
Look for events (scheduling, image pull, volumes, secrets)
```bash
kubectl describe pod <name>
```
Look for your program's output
```bash
kubectl logs <name> [--previous]
```

## Cleanup (end of workshop)

This **permanently deletes your PVC data**, so copy out anything you want to keep first:

```bash
kubectl delete pods,jobs,configmaps,secrets,pvc -l owner=$ME
```
```bash
kubectl get pods,jobs,pvc -l owner=$ME
```
You should see "No resources found"
