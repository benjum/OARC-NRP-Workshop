# UCLA OARC Workshop: Computing on the National Research Platform (NRP)

Hands-on Kubernetes labs for researchers: interactive Pods, persistent storage, Jupyter, batch Jobs, and LLMs on NRP.

**📖 Workshop site: https://benjum.github.io/OARC-NRP-Workshop/**

## Quick start

```bash
git clone https://github.com/benjum/OARC-NRP-Workshop.git
cd OARC-NRP-Workshop
./personalize.sh <yourname>      # Windows: .\personalize.ps1 <yourname>
```

Then follow the labs on the workshop site, running every command from this folder.

## What's here

```
index.md, labs/*/README.md   the lab guides (also published as the website)
labs/*/*.yaml                Kubernetes manifests for each lab
ml/train.py                  the example ML script
personalize.sh / .ps1        put your name into the YAMLs
INSTRUCTOR_NOTES.md          pre-flight checklist (not published on the site)
_config.yml, Gemfile         website settings
```
