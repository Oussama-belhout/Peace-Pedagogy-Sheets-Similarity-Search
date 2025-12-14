# Peace Pedagogy Similarity Search

Semantic search system for finding similar pedagogical sheets based on Peace Pedagogy principles.

## Overview

Finds similar pedagogical sheets using ontology-based similarity across multiple dimensions:
- Peace axes (self, others, environment)
- Pedagogical tools (CEVQ, meditation, project-based learning)
- Virtues (gratitude, empathy, responsibility)
- Teaching strategies
- Age ranges and duration

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```python
from find_similar_lessons import find_similar

results = find_similar(
    title="My Lesson Title",
    domain="Sciences",
    axes=["peace_with_environment"],
    tools=["project_based_learning"],
    virtues=["responsibility"],
    target_age_min=8,
    target_age_max=12,
    top_k=3
)

for result in results:
    print(f"{result['title']}: {result['similarity_score']:.2%}")
```

## Quick Start

```bash
python find_similar_lessons.py    # Run examples
python run_complete_demo.py        # Full demonstration
```

## Project Structure

```
├── src/
│   ├── ontology_builder.py    # OWL ontology creation
│   ├── similarity_engine.py   # Similarity computation
│   ├── data_loader.py         # Load lessons from JSON
│   └── query_engine.py        # Query interface
├── data/
│   └── pedagogical_sheets.json
├── ontology/
│   └── peace_pedagogy.owl
├── find_similar_lessons.py    # Main API
└── run_complete_demo.py       # Demo with 27 real sheets
```

## Documentation

See [docs/README.md](docs/README.md) for detailed documentation.
