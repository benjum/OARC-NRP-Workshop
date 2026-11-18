---
title: "Lab 1: ML script in a Pod"
nav_order: 2
permalink: /labs/01-ml-pod/
---

# Lab 1: Run a Python ML script in a Pod

**Goal:** start a Pod, run `ml/train.py` inside it, and see that everything you did inside disappears when the Pod is deleted.
**Slurm analogy:** `salloc` + an interactive shell, except the software comes from a container image.

### 1. Create the Pod and watch it start

```bash
kubectl apply -f labs/01-ml-pod/pod.yaml
```
To watch pod start (Pending -> ContainerCreating -> Running (Ctrl-C to stop))
```bash
kubectl get pods -w
```
To look at the NODE you landed on:
```bash
kubectl get pod ml-pod-$ME -o wide
```
To look at pod details, including events (at bottom) to explain any waiting
```bash
kubectl describe pod ml-pod-$ME
```

The scheduler places the Pod on any node with the **requested** 1 CPU and 2 GiB free. There's no queue: if nothing fits, the Pod waits in `Pending`.

### 2. Copy the script in and open a shell

```bash
kubectl cp ml/train.py "ml-pod-${ME}:/tmp/train.py"
```
```bash
kubectl exec -it ml-pod-$ME -- bash
```

### 3. Inside the container

Try to run the ML script (fails: scikit-learn isn't in this image)
```bash
python /tmp/train.py
```
```bash
pip install scikit-learn
```
Now it will work, and write ./results
```bash
python /tmp/train.py
```
```bash
exit
```

### 4. Delete, recreate, and check what survived

```bash
kubectl delete pod ml-pod-$ME
```
```bash
kubectl apply -f labs/01-ml-pod/pod.yaml
```
```bash
kubectl wait --for=condition=Ready pod/ml-pod-$ME --timeout=300s
```
Notice what remains.  train.py, results, and scikit-learn are all gone
```bash
kubectl exec ml-pod-$ME -- ls /tmp
```

**Takeaways:** every Pod starts from the clean image. Put software in the **image** and data on a **PVC** (Lab 2). Sleeping is fine in an interactive Pod (6-hour maximum), never in a Job.

**Cleanup:** `kubectl delete pod ml-pod-$ME`
