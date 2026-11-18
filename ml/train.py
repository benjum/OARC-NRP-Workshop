#!/usr/bin/env python3
"""
NRP workshop example: tiny CPU-only ML run (a few seconds).

Trains random forests of a few sizes on scikit-learn's bundled digits dataset
and writes metrics.json, sweep.csv and best_model.joblib to --output-dir.

    python train.py --output-dir /data/results/run1
"""
import argparse
import csv
import json
import os
import socket
import sys
from pathlib import Path


def log(msg):
    print(msg, flush=True)  # flush so lines show up in `kubectl logs` right away


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--output-dir", default="results")
    p.add_argument("--n-estimators", default="50,100,200")
    p.add_argument("--seed", type=int, default=42)
    args = p.parse_args()

    try:
        import joblib
        from sklearn.datasets import load_digits
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.model_selection import train_test_split
    except ImportError:
        log("ERROR: scikit-learn is not installed. Fix: pip install scikit-learn")
        return 1

    # os.cpu_count() reports the whole node, not your Kubernetes CPU limit,
    # so take the core count from N_JOBS (set in the YAML to match the request).
    n_jobs = int(os.environ.get("N_JOBS", "1"))
    out = Path(args.output_dir)
    out.mkdir(parents=True, exist_ok=True)
    log(f"pod={socket.gethostname()}  n_jobs={n_jobs}  output={out.resolve()}")

    X, y = load_digits(return_X_y=True)
    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.25,
                                              random_state=args.seed, stratify=y)
    sweep, best = [], None
    for n in [int(s) for s in args.n_estimators.split(",")]:
        clf = RandomForestClassifier(n_estimators=n, random_state=args.seed, n_jobs=n_jobs)
        acc = clf.fit(X_tr, y_tr).score(X_te, y_te)
        sweep.append({"n_estimators": n, "test_accuracy": round(acc, 4)})
        log(f"n_estimators={n:<4d} accuracy={acc:.4f}")
        if best is None or acc > best[1]:
            best = (clf, acc, n)

    joblib.dump(best[0], out / "best_model.joblib")
    with open(out / "sweep.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["n_estimators", "test_accuracy"])
        w.writeheader()
        w.writerows(sweep)
    (out / "metrics.json").write_text(json.dumps(
        {"best_n_estimators": best[2], "best_test_accuracy": round(best[1], 4),
         "sweep": sweep, "seed": args.seed, "pod": socket.gethostname()}, indent=2))
    log(f"best: n_estimators={best[2]} accuracy={best[1]:.4f}  -> wrote {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
