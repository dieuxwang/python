# AI Project Management WBS - Project Intent Input Model

This repository defines the pre-WBS **Project Intent Input Model**:

- JSON Schema: `project_intent_input.schema.json`
- Example input: `examples/pharma_hybrid_cloud_modernization.intent-input.json`
- Conversion logic (Input -> Normalized Intent): `src/intent_normalizer.py`
- Design notes / field impact map: `docs/project_intent_input_model.md`

## Quick use

```python
import json
from src.intent_normalizer import normalize_intent_input

with open("examples/pharma_hybrid_cloud_modernization.intent-input.json", "r", encoding="utf-8") as f:
    payload = json.load(f)

normalized = normalize_intent_input(payload)
print(json.dumps(normalized, indent=2, ensure_ascii=False))
```
