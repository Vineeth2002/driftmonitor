
---

### File: `DriftMonitor/docs/ETHICS.md`
```markdown
# Ethics, Data, and Limitations — DriftMonitor

DriftMonitor is intended as a research/demo system to surface safety signals and distributional changes. It is **not** a production safety product.

## Data sources
- Public sources (Hacker News, Google Trends, Wikipedia, etc.) are used only via public APIs or bundled samples.
- No personal/private data is collected or stored in the repository.
- If you enable collectors that access external APIs, respect rate limits and terms of service.

## Privacy & compliance
- Do not commit API keys or secrets to the repository.
- If using external content that contains personal data, ensure lawful basis & redaction if needed.

## Limitations
- Small-sample approach: results are illustrative, not exhaustive.
- Rule-based toxicity detection is simplistic and may have false positives/negatives.
- Sentiment signals are proxies; they do not equate to harm measurement.
- JSD on unigram distributions is a coarse drift indicator and should be complemented with task-specific metrics.

## Responsible use
- Use DriftMonitor as a research/demo tool; do not deploy decisions that impact people without further validation.
- Clearly document the system’s limitations when presenting results.
- When publishing analyses, include provenance, sampling strategy, and ethical considerations.

