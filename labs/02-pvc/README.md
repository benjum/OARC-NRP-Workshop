---
title: "Lab 2: Results on a PVC"
nav_order: 3
permalink: /labs/02-pvc/
---

# Lab 2: Keep ML results on a PersistentVolumeClaim (~12 min)

**Goal:** write results to a PVC, delete the Pod, and recover the results from a new Pod and on your laptop.
**Slurm analogy:** the PVC is your project directory. You **claim** it once and **mount** it into each Pod.

Ways to move data:
- `kubectl cp` for small files to and from your laptop.
- A PVC for anything that must outlive a Pod.
- The image for software.
- NRP's object storage for large datasets.

> NRP rule: never `pip`/`conda install` onto CephFS volumes. Use them only for data and results.

### 1. Create the PVC, then a Pod that mounts it

```bash
kubectl apply -f labs/02-pvc/pvc.yaml
kubectl get pvc ml-data-$ME            # STATUS Bound (or Pending until a Pod uses it)
kubectl apply -f labs/02-pvc/pod-with-pvc.yaml
kubectl wait --for=condition=Ready pod/ml-pvc-pod-$ME --timeout=300s
```

The `volumeMounts` + `volumes` pair in the YAML is how any Pod, Job, or Jupyter server gets storage.

### 2. Put the script on the PVC and write results there

```bash
kubectl exec ml-pvc-pod-$ME -- mkdir -p /data/code
kubectl cp ml/train.py "ml-pvc-pod-${ME}:/data/code/train.py"
kubectl exec -it ml-pvc-pod-$ME -- bash
# inside:
pip install --root-user-action=ignore scikit-learn     # into the container, NOT /data
python /data/code/train.py --output-dir /data/results/pvc-run1
exit
```

### 3. Delete the Pod and check the data from a new one

```bash
kubectl delete pod ml-pvc-pod-$ME
kubectl apply -f labs/02-pvc/pod-with-pvc.yaml
kubectl wait --for=condition=Ready pod/ml-pvc-pod-$ME --timeout=300s
kubectl exec ml-pvc-pod-$ME -- cat /data/results/pvc-run1/metrics.json
```

The results survived, even if the new Pod landed on a different node. scikit-learn did not, because it lived in the container.

### 4. Copy the results to your laptop

```bash
kubectl cp "ml-pvc-pod-${ME}:/data/results/pvc-run1" ./results-pvc-run1
```

**Takeaway:** Pods are disposable compute; the PVC holds your data. **Keep the PVC.** Labs 3 to 5 use it.

**Cleanup:** `kubectl delete pod ml-pvc-pod-$ME`. Delete the PVC only at the end of the workshop.
