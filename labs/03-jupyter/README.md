---
title: "Lab 3: Jupyter in a Pod"
nav_order: 4
permalink: /labs/03-jupyter/
---

# Lab 3: JupyterLab in a Pod with port-forwarding

**Goal:** run your own JupyterLab on NRP, open it in your laptop's browser, and analyze the Lab 2 results stored on the PVC.
**Needs:** the PVC from Lab 2. Without it, this Pod stays `Pending`.

### 1. Start Jupyter and get the login token

```bash
kubectl apply -f labs/03-jupyter/jupyter-pod.yaml
kubectl wait --for=condition=Ready pod/jupyter-$ME --timeout=600s   # first image pull is slow
kubectl logs jupyter-$ME        # copy the http://127.0.0.1:8888/lab?token=... URL
```

### 2. Port-forward (in a separate terminal; leave it running)

```bash
kubectl port-forward pod/jupyter-$ME 8888:8888
```

Open the URL from step 1. The tunnel goes through the Kubernetes API with your credentials, so Jupyter isn't exposed to the internet. If local port 8888 is busy, use `8889:8888` and change the port in the URL.

### 3. Run the example notebook

In JupyterLab, open **`work/`** (your PVC) and drag `labs/03-jupyter/explore_results.ipynb` into it. Run the cells with Shift+Enter. The notebook tables and plots the results from Lab 2, then loads the saved model to classify a few digits.

Two Pods, one PVC: Lab 2 wrote the results and Jupyter reads them.

### 4. Shut down

Use **File → Shut Down**, or `kubectl delete pod jupyter-$ME`. Files in `~/work` persist; everything else in the container is lost.

| Problem | Fix |
|---|---|
| `Pending`, PVC not found | Do Lab 2 step 1 first |
| `Unable to listen on port 8888` | Use `8889:8888` |
| `Permission denied` in `work/` | `kubectl exec ml-pvc-pod-$ME -- chmod -R a+rwX /data` |
