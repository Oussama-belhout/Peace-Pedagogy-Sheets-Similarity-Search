# API Reference

## Main Function: `find_similar()`

```python
from find_similar_lessons import find_similar

results = find_similar(
    title: str,                    # Required
    description: str = "",         # Optional
    domain: str = None,           # Optional
    axes: list = None,            # Optional
    tools: list = None,           # Optional
    virtues: list = None,         # Optional
    strategies: list = None,      # Optional
    target_age_min: int = None,   # Optional
    target_age_max: int = None,   # Optional
    duration: float = None,       # Optional
    group_size_min: int = None,   # Optional
    group_size_max: int = None,   # Optional
    top_k: int = 5                # Optional
) -> List[Dict]
```

## Input Parameters

| Parameter | Type | Required | Description | Example Values |
|-----------|------|----------|-------------|----------------|
| `title` | str | ✅ Yes | Title of the new lesson | "My Environmental Lesson" |
| `description` | str | No | Brief description | "Students learn about..." |
| `domain` | str | No | Academic domain | "Sciences", "Arts", "Ethics", "Languages" |
| `axes` | list[str] | No | Peace dimensions | ["peace_with_self", "peace_with_others", "peace_with_environment"] |
| `tools` | list[str] | No | Pedagogical tools | ["cevq", "meditation", "project_based_learning", "artistic_expression"] |
| `virtues` | list[str] | No | Values to develop | ["gratitude", "empathy", "responsibility", "compassion", "patience", "benevolence"] |
| `strategies` | list[str] | No | Teaching strategies | ["experiential_learning", "dialogical_approach", "structured_questioning"] |
| `target_age_min` | int | No | Minimum age | 6, 7, 8, etc. |
| `target_age_max` | int | No | Maximum age | 12, 14, 16, etc. |
| `duration` | float | No | Duration in hours | 1.5, 2.0, 3.0, etc. |
| `group_size_min` | int | No | Minimum group size | 10, 15, 20, etc. |
| `group_size_max` | int | No | Maximum group size | 20, 25, 30, etc. |
| `top_k` | int | No | Number of results | 3, 5, 10, etc. (default: 5) |

## Output Format

Returns a list of dictionaries, each containing:

```python
{
    # Lesson Information
    'title': str,                    # Lesson title
    'description': str,              # Lesson description
    'domain': str,                   # Academic domain
    'discipline': str,               # Specific discipline
    
    # Pedagogical Elements
    'axes': List[str],              # Peace axes
    'tools': List[str],             # Pedagogical tools
    'virtues': List[str],           # Virtues developed
    'strategies': List[str],        # Teaching strategies
    
    # Practical Details
    'target_age_min': int,          # Minimum age
    'target_age_max': int,          # Maximum age
    'duration': float,              # Duration in hours
    'group_size_min': int,          # Min group size
    'group_size_max': int,          # Max group size
    
    # Similarity Information
    'similarity_score': float,      # Overall score (0.0 - 1.0)
    'similarity_breakdown': {
        'axes': {
            'score': float,         # Dimension score (0.0 - 1.0)
            'contribution': float,  # Contribution to total
            'shared': List[str]     # Shared elements
        },
        'tools': { ... },
        'virtues': { ... },
        'strategies': { ... },
        'age': { ... },
        'duration': { ... },
        'domain': { ... }
    }
}
```

## Usage Examples

### Minimal Example

```python
results = find_similar(
    title="My Lesson"
)
```

### Typical Example

```python
results = find_similar(
    title="Environmental Awareness",
    domain="Sciences",
    axes=["peace_with_environment"],
    tools=["project_based_learning"],
    target_age_min=8,
    target_age_max=12,
    top_k=5
)
```

### Complete Example

```python
results = find_similar(
    title="Collaborative Music Project",
    description="Students create music together",
    domain="Arts",
    discipline="music",
    axes=["peace_with_self", "peace_with_others"],
    tools=["artistic_expression", "project_based_learning"],
    virtues=["patience", "benevolence", "empathy"],
    strategies=["experiential_learning", "collaborative_construction"],
    target_age_min=8,
    target_age_max=14,
    duration=2.0,
    group_size_min=15,
    group_size_max=30,
    top_k=3
)

# Process results
for result in results:
    print(f"{result['title']}: {result['similarity_score']:.1%}")
```

## Available Values

### Domains
- `"Sciences"`
- `"Arts"`
- `"Ethics"`
- `"Languages"`

### Peace Axes
- `"peace_with_self"` - Inner peace, self-awareness
- `"peace_with_others"` - Social harmony, collaboration
- `"peace_with_environment"` - Environmental consciousness

### Tools
- `"cevq"` - Cercle d'Éveil aux Vertus et aux Qualités
- `"meditation"` - Mindfulness and inner calm practices
- `"project_based_learning"` - Collaborative project-based approach
- `"artistic_expression"` - Arts-based learning
- `"solution_oriented_learning"` - Problem-solving focus

### Virtues
- `"gratitude"` - Appreciation and thankfulness
- `"empathy"` - Understanding others' feelings
- `"responsibility"` - Accountability and duty
- `"compassion"` - Caring for others
- `"patience"` - Tolerance and calmness
- `"benevolence"` - Kindness and goodwill

### Strategies
- `"experiential_learning"` - Learning through experience
- `"dialogical_approach"` - Learning through dialogue
- `"structured_questioning"` - Guided inquiry
- `"awakening_alterity"` - Understanding others/diversity
- `"collaborative_construction"` - Building knowledge together

## Return Value Examples

### Single Result

```python
{
    'title': 'The Journey of Water',
    'description': 'Understanding water cycle...',
    'domain': 'sciences',
    'discipline': 'environmental_science',
    'axes': ['peace_with_environment'],
    'tools': ['project_based_learning', 'artistic_expression'],
    'virtues': ['responsibility', 'gratitude'],
    'strategies': ['experiential_learning', 'structured_questioning'],
    'target_age_min': 9,
    'target_age_max': 13,
    'duration': 2.5,
    'group_size_min': 15,
    'group_size_max': 25,
    'similarity_score': 0.667,
    'similarity_breakdown': {
        'axes': {
            'score': 0.50,
            'contribution': 0.125,
            'shared': ['peace_with_environment']
        },
        'tools': {
            'score': 1.00,
            'contribution': 0.200,
            'shared': ['project_based_learning']
        },
        'virtues': {
            'score': 1.00,
            'contribution': 0.200,
            'shared': ['gratitude', 'responsibility']
        },
        # ... other dimensions
    }
}
```

## Advanced API

### Using QueryEngine Directly

```python
from src.query_engine import LessonQuery
from owlready2 import get_ontology

# Load ontology
onto = get_ontology("ontology/peace_pedagogy.owl").load()

# Create query engine
query_engine = LessonQuery(onto)

# Customize weights
query_engine.engine.weights = {
    'axes': 0.30,
    'tools': 0.20,
    'virtues': 0.25,
    'strategies': 0.10,
    'age': 0.10,
    'duration': 0.03,
    'domain': 0.02
}

# Query
results = query_engine.query_similar_lessons(
    title="My Lesson",
    domain="Sciences",
    axes=["peace_with_environment"],
    top_k=5
)
```

### Using search_similar_lessons()

```python
from src.query_engine import search_similar_lessons

results = search_similar_lessons(
    title="My Lesson",
    domain="Sciences",
    axes=["peace_with_environment"],
    tools=["project_based_learning"],
    top_k=5,
    ontology_path="ontology/peace_pedagogy.owl"  # Custom path
)
```

## Error Handling

```python
try:
    results = find_similar(
        title="My Lesson",
        domain="InvalidDomain",  # Will be ignored
        axes=["invalid_axis"],    # Will be ignored
        top_k=5
    )
    
    if not results:
        print("No similar lessons found")
    else:
        print(f"Found {len(results)} similar lessons")
        
except FileNotFoundError:
    print("Ontology file not found. Run: python src/ontology_builder.py")
    
except Exception as e:
    print(f"Error: {e}")
```

## Performance Notes

- **Loading Time**: First call loads ontology (~1-2 seconds)
- **Query Time**: Subsequent queries are fast (~0.1 seconds)
- **Scalability**: Linear with number of lessons in database
- **Optimization**: Consider caching ontology for multiple queries

## Best Practices

1. **Be Specific**: Provide as many relevant parameters as possible
2. **Use Lists**: Multiple values increase matching opportunities
3. **Adjust top_k**: Request more results than you need, then filter
4. **Check Scores**: Use `similarity_score` to filter quality
5. **Review Breakdown**: Use `similarity_breakdown` to understand matches

## Integration Pattern

```python
# Typical workflow
def create_lesson_from_template(user_input):
    # 1. Find similar sheets
    similar = find_similar(
        title=user_input['title'],
        domain=user_input['domain'],
        axes=user_input['axes'],
        tools=user_input['tools'],
        target_age_min=user_input['age_min'],
        target_age_max=user_input['age_max'],
        top_k=5
    )
    
    # 2. Filter by quality
    high_quality = [s for s in similar if s['similarity_score'] > 0.5]
    
    # 3. Extract key information
    examples = [{
        'title': s['title'],
        'structure': extract_structure(s),
        'content': extract_content(s),
        'weight': s['similarity_score']
    } for s in high_quality]
    
    # 4. Generate new lesson (future AI integration)
    # new_lesson = ai_model.generate(user_input, examples)
    
    return examples  # For now, return examples
```



