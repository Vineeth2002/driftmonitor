# DriftMonitor

**DriftMonitor** is a lightweight, GitHub-native AI safety & drift monitoring system designed for reproducible demos, research-ready reporting, and live presentation via GitHub Pages. It collects small daily samples from multiple public sources, evaluates texts for safety signals, computes distributional drift, and publishes static reports.

This repo is optimized for:

- Minimal resources (runs on GitHub Actions)
- Reproducibility (bundled sample data + config)
- Clear evaluation and interpretability for reviewers
- Easy demo via GitHub Pages

---

## Project highlights

- Collectors: Google Trends, Hacker News, Custom prompts (template included)
- Benchmark: small model runner (transformers optional) + rule-based fallback
- Metrics: Jensen–Shannon drift, KL divergence, toxicity statistics
- Reporting: HTML report generation + GitHub Pages publishing
- Automation: GitHub Actions for collect → evaluate → metrics → report
- Designed to be demo-ready for admissions / scholarships

---

## Quick start (local)

1. Clone the repo:
```bash
git clone https://github.com/<your-username>/DriftMonitor.git
cd DriftMonitor
