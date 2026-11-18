---
title: "Lab 4: Pod to Job"
nav_order: 5
permalink: /labs/04-job/
---

# Lab 4: Convert the Pod into a batch Job

**Goal:** run the Lab 2 ML work unattended as a **Job**, the Kubernetes version of `sbatch`.

### What changes from Pod to Job

| Interactive Pod | Job | Why |
|---|---|---|
| `kind: Pod` | `apiVersion: batch/v1`, `kind: Job` | A Job is a controller: it runs Pods to completion and retries failures |
| Pod spec at the top | Pod spec under `spec.template.spec` | The Job creates Pods from this template |
| `sleep`, then you `exec` in | The command **does the work and exits** | No human in the loop. **Sleeping in a Job gets you banned on NRP** |
| `kubectl cp` the script | Script mounted from a **ConfigMap** | Inputs must exist when the container starts |
| — | `backoffLimit`, `ttlSecondsAfterFinished` | Retries and automatic cleanup |

```bash
diff labs/02-pvc/pod-with-pvc.yaml labs/04-job/job.yaml
```

### 1. Put the script in a ConfigMap and submit the Job

```bash
kubectl create configmap train-script-$ME --from-file=train.py=ml/train.py
```
```bash
kubectl label configmap train-script-$ME owner=$ME
```
```bash
kubectl apply -f labs/04-job/job.yaml
```

### 2. Follow it

```bash
kubectl get jobs,pods -l owner=$ME
```
We can look at job logs to see pip install and then the sweep.
```bash
kubectl logs -f job/ml-job-$ME          
```
The `get jobs` will show `COMPLETIONS 1/1` when done
```bash
kubectl get job ml-job-$ME              
```

### 3. Check the results on the PVC

The Job's Pod has exited, so look through any Pod that mounts the PVC: the Lab 2 Pod, or re-run the Lab 3 notebook.

```bash
kubectl apply -f labs/02-pvc/pod-with-pvc.yaml
```
```bash
kubectl exec ml-pvc-pod-$ME -- cat /data/results/job-run/metrics.json
```

To run it again, delete and re-apply the Job; Jobs can't be edited in place. Finished Jobs delete themselves after an hour, but the results on the PVC stay.

**Cleanup:** `kubectl delete job ml-job-$ME; kubectl delete configmap train-script-$ME`
