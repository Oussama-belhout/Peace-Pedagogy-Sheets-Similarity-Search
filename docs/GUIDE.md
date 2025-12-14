# Documentation

## System Architecture

The system uses an OWL ontology to represent pedagogical sheets and computes semantic similarity across 7 weighted dimensions.

### Components

**Ontology Builder** - Creates formal OWL ontology with classes (Lesson, Tool, Virtue, etc.) and properties  
**Data Loader** - Loads pedagogical sheets from JSON into the ontology  
**Similarity Engine** - Computes multi-dimensional similarity using Jaccard similarity and compatibility metrics  
**Query Engine** - Provides query interface with temporary lesson creation

### Similarity Dimensions

| Dimension | Weight | Method |
|-----------|--------|--------|
| Peace Axes | 0.25 | Jaccard similarity |
| Tools | 0.20 | Jaccard similarity |
| Virtues | 0.20 | Jaccard similarity |
| Strategies | 0.15 | Jaccard similarity |
| Age | 0.10 | Range overlap |
| Duration | 0.05 | Ratio comparison |
| Domain | 0.05 | Exact match |

## API Reference

### find_similar()

Find similar pedagogical sheets based on metadata.

```python
from find_similar_lessons import find_similar

results = find_similar(
    title="Lesson Title",
    description="Optional description",
    domain="Sciences|Arts|Ethics|Languages",
    axes=["peace_with_self", "peace_with_others", "peace_with_environment"],
    tools=["cevq", "meditation", "project_based_learning", "artistic_expression"],
    virtues=["gratitude", "empathy", "responsibility", "compassion", "patience"],
    target_age_min=6,
    target_age_max=14,
    duration=2.0,
    top_k=5
)
```

**Returns**: List of dictionaries with lesson metadata and similarity scores

### search_similar_lessons()

Lower-level search function with full parameter control.

```python
from query_engine import search_similar_lessons

results = search_similar_lessons(
    title="Lesson Title",
    # ... same parameters as find_similar
    min_similarity=0.3,
    ontology_path="ontology/peace_pedagogy.owl"
)
```

## Data Format

Pedagogical sheets are stored in JSON format:

```json
{
  "lessons": [
    {
      "id": "lesson_1",
      "title": "Lesson Title",
      "description": "Description",
      "domain": "Sciences",
      "discipline": "Biology",
      "axes": ["peace_with_environment"],
      "tools": ["project_based_learning"],
      "virtues": ["responsibility", "gratitude"],
      "strategies": ["experiential_learning"],
      "target_age_min": 8,
      "target_age_max": 12,
      "duration": 2.0,
      "group_size_min": 15,
      "group_size_max": 30
    }
  ]
}
```

## Extending the System

### Add New Virtues

Edit `src/ontology_builder.py`:

```python
class NewVirtue(Virtue):
    pass

new_virtue = NewVirtue("new_virtue")
```

### Add New Tools

```python
class NewTool(Tool):
    pass

new_tool = NewTool("new_tool")
new_tool.description = ["Tool description"]
new_tool.supports = [peace_with_self, peace_with_others]
```

### Adjust Similarity Weights

Edit weights in `src/similarity_engine.py`:

```python
self.weights = {
    'axes': 0.30,      # Increase axes weight
    'tools': 0.20,
    'virtues': 0.15,
    # ...
}
```
