# Instructor notes

These labs were validated offline (YAML schema, the script, the notebook, and the Jupyter AI start-up configuration) but not on the live cluster. **Do one full dry run the day before.**

- [ ] `kubectl get storageclass`: confirm `rook-cephfs-central` exists and that a test PVC reaches `Bound`.
- [ ] Confirm the Jupyter Pod can write to `~/work` after the Lab 2 Pod (which runs as root) has written there.
- [ ] Pull `quay.io/jupyter/scipy-notebook` once, then consider pinning that dated tag.
- [ ] Every participant gets `yes` from `kubectl auth can-i create pods`, and the namespace quota covers N × (2 CPU, 4 GiB).
- [ ] `curl -H "Authorization: Bearer $TOKEN" https://ellm.nrp-nautilus.io/v1/models` still lists `gpt-oss`.
- [ ] If a new Jupyter AI release breaks the start-up flags, pin `jupyter-ai[jupyternaut]==3.2.0`. The flags were verified against that version.

**Time savers:**
- Have people `apply` the Jupyter Pod at the start of Lab 2 so its image is pulled by Lab 3.
- In Lab 5, have them apply the Pod first, then talk through the setup while it installs.
