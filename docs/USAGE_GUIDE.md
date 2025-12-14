# Usage Guide - Peace Pedagogy Similarity Search

## 🎯 Purpose

**INPUT**: Raw metadata for a NEW lesson you want to create (name, subject, age, virtues, etc.)  
**OUTPUT**: Existing similar pedagogical sheets from the database  
**NEXT STEP**: Feed similar sheets to an AI model to generate a complete new pedagogical sheet

## 📋 Workflow

```
[Your Lesson Metadata] 
        ↓
[Similarity Search]
        ↓
[Top N Similar Existing Sheets]
        ↓
[AI Model] (future)
        ↓
[Generated Complete Pedagogical Sheet]
```

## 🚀 Quick Start

### Simple Usage

```python
from find_similar_lessons import find_similar

# Describe your new lesson
results = find_similar(
    title="My Environmental Lesson",
    domain="Sciences",
    axes=["peace_with_environment"],
    tools=["project_based_learning"],
    virtues=["responsibility", "gratitude"],
    target_age_min=8,
    target_age_max=12,
    duration=2.5,
    top_k=5  # Get top 5 similar sheets
)

# Use results as examples for your AI model
for sheet in results:
    print(f"{sheet['title']}: {sheet['similarity_score']:.1%} match")
    # Feed to AI model here
```

### Run Examples

```bash
# Activate environment
venv\Scripts\activate

# See 3 complete examples
python find_similar_lessons.py
```

## 📝 Input Parameters

### Required
- **title** (str): Title of your new lesson

### Optional
- **description** (str): Brief description
- **domain** (str): Choose from:
  - `"Sciences"`
  - `"Arts"`
  - `"Ethics"`
  - `"Languages"`

- **axes** (list): Peace dimensions
  - `"peace_with_self"` - Inner peace, self-awareness
  - `"peace_with_others"` - Social harmony, collaboration
  - `"peace_with_environment"` - Environmental consciousness

- **tools** (list): Pedagogical tools
  - `"cevq"` - Cercle d'Éveil aux Vertus et aux Qualités
  - `"meditation"` - Mindfulness practices
  - `"project_based_learning"` - Project-based approach
  - `"artistic_expression"` - Arts-based learning
  - `"solution_oriented_learning"` - Problem-solving focus

- **virtues** (list): Values to develop
  - `"gratitude"`
  - `"empathy"`
  - `"responsibility"`
  - `"compassion"`
  - `"patience"`
  - `"benevolence"`

- **strategies** (list): Teaching strategies
  - `"experiential_learning"`
  - `"dialogical_approach"`
  - `"structured_questioning"`
  - `"awakening_alterity"`
  - `"collaborative_construction"`

- **target_age_min** (int): Minimum age (e.g., 6)
- **target_age_max** (int): Maximum age (e.g., 14)
- **duration** (float): Duration in hours (e.g., 2.5)
- **group_size_min** (int): Minimum group size
- **group_size_max** (int): Maximum group size
- **top_k** (int): Number of results to return (default: 5)

## 📤 Output Format

Each result contains:

```python
{
    'title': 'Lesson Title',
    'description': 'Lesson description',
    'domain': 'Sciences',
    'discipline': 'ecology',
    'axes': ['peace_with_environment', 'peace_with_others'],
    'tools': ['project_based_learning', 'cevq'],
    'virtues': ['responsibility', 'gratitude'],
    'strategies': ['experiential_learning'],
    'target_age_min': 8,
    'target_age_max': 12,
    'duration': 2.5,
    'group_size_min': 15,
    'group_size_max': 25,
    'similarity_score': 0.667,  # 66.7% match
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
        # ... more breakdowns
    }
}
```

## 💡 Usage Examples

### Example 1: Environmental Science

```python
results = find_similar(
    title="Protecting Local Wildlife",
    description="Learn about local animal species",
    domain="Sciences",
    axes=["peace_with_environment"],
    tools=["project_based_learning"],
    virtues=["responsibility", "compassion"],
    target_age_min=8,
    target_age_max=12,
    duration=2.0,
    top_k=3
)
```

**Output:**
```
[1] The Journey of Water - 63.7% match
    Best matches: Peace Axes, Tools, Age Range
    
[2] Community Garden Project - 46.5% match
    Best matches: Peace Axes, Tools, Virtues
    
[3] Mandala d'une assiette de riz - 36.4% match
    Best matches: Peace Axes, Tools, Age Range
```

### Example 2: Emotional Learning

```python
results = find_similar(
    title="Understanding Our Emotions",
    domain="Ethics",
    axes=["peace_with_self", "peace_with_others"],
    tools=["cevq", "meditation"],
    virtues=["empathy", "patience"],
    target_age_min=7,
    target_age_max=10,
    duration=1.5,
    top_k=3
)
```

**Output:**
```
[1] Circle of Listening - 74.4% match
    Perfect match on tools and axes!
    
[2] Creating Harmony Together - 53.0% match
    Strong match on axes and virtues
    
[3] Mandala d'une assiette de riz - 28.6% match
    Some overlap in tools and virtues
```

### Example 3: Arts Collaboration

```python
results = find_similar(
    title="Creating Together",
    domain="Arts",
    axes=["peace_with_others"],
    tools=["artistic_expression", "project_based_learning"],
    virtues=["benevolence", "patience"],
    target_age_min=9,
    target_age_max=13,
    duration=2.5,
    top_k=3
)
```

**Output:**
```
[1] Creating Harmony Together - 43.6% match
    Strong match on tools and peace axes
    
[2] Community Garden Project - 35.5% match
    Good match on collaboration focus
    
[3] The Journey of Water - 35.0% match
    Similar project-based approach
```

## 🔧 Advanced Usage

### Custom Weights

If you want to emphasize certain dimensions:

```python
from query_engine import LessonQuery
from owlready2 import get_ontology

onto = get_ontology("ontology/peace_pedagogy.owl").load()
query_engine = LessonQuery(onto)

# Emphasize virtues more
query_engine.engine.weights = {
    'axes': 0.20,
    'tools': 0.15,
    'virtues': 0.35,  # Increased!
    'strategies': 0.15,
    'age': 0.10,
    'duration': 0.03,
    'domain': 0.02
}

results = query_engine.query_similar_lessons(
    title="My Lesson",
    virtues=["empathy", "compassion"],
    # ... other params
)
```

### Filtering by Similarity Threshold

```python
from query_engine import search_similar_lessons

# Only return sheets with >50% similarity
results = search_similar_lessons(
    title="My Lesson",
    domain="Sciences",
    axes=["peace_with_environment"],
    top_k=10,
    # Custom filtering after getting results
)

high_similarity = [r for r in results if r['similarity_score'] > 0.5]
```

### Batch Processing

```python
lessons_to_create = [
    {
        'title': 'Lesson 1',
        'domain': 'Sciences',
        'axes': ['peace_with_environment'],
        # ...
    },
    {
        'title': 'Lesson 2',
        'domain': 'Ethics',
        'axes': ['peace_with_self'],
        # ...
    }
]

all_results = []
for lesson_meta in lessons_to_create:
    results = find_similar(**lesson_meta, top_k=3)
    all_results.append({
        'query': lesson_meta,
        'similar_sheets': results
    })
```

## 🤖 Integration with AI Model (Future)

```python
from find_similar_lessons import find_similar
# from your_ai_model import generate_pedagogical_sheet

# 1. Get similar sheets
similar_sheets = find_similar(
    title="New Lesson About Trees",
    domain="Sciences",
    axes=["peace_with_environment"],
    tools=["project_based_learning"],
    target_age_min=8,
    target_age_max=12,
    top_k=5
)

# 2. Extract examples for AI
examples = []
for sheet in similar_sheets:
    examples.append({
        'title': sheet['title'],
        'description': sheet['description'],
        'structure': 'PDF content would go here',
        'similarity': sheet['similarity_score']
    })

# 3. Generate new sheet using AI
# new_sheet = generate_pedagogical_sheet(
#     user_input={
#         'title': "New Lesson About Trees",
#         'target_age': "8-12",
#         # ...
#     },
#     examples=examples,
#     weights=[s['similarity_score'] for s in similar_sheets]
# )
```

## 📊 Understanding Similarity Scores

### Score Components

Each similarity score (0.0 to 1.0) is computed from 7 dimensions:

1. **Peace Axes** (25%): Matching peace dimensions
2. **Tools** (20%): Matching pedagogical tools
3. **Virtues** (20%): Matching values/virtues
4. **Strategies** (15%): Matching teaching strategies
5. **Age Range** (10%): Age group compatibility
6. **Duration** (5%): Similar lesson length
7. **Domain** (5%): Same subject area

### Interpreting Scores

- **0.70 - 1.00**: Excellent match - Very similar lessons
- **0.50 - 0.69**: Good match - Strong similarities
- **0.30 - 0.49**: Moderate match - Some useful similarities
- **0.00 - 0.29**: Weak match - Few similarities

### What Makes a Good Match?

High similarity means the sheets share:
- Similar pedagogical approaches (tools & strategies)
- Same peace education goals (axes)
- Compatible age groups and durations
- Similar values being cultivated

## 🔍 Current Database

The system currently contains **5 sample lessons**:

1. **Mandala d'une assiette de riz** (Sciences)
   - Peace with Environment & Others
   - CEVQ, Project-Based Learning
   - Ages 6-14, 3 hours

2. **Community Garden Project** (Sciences)
   - Peace with Environment & Others
   - Project-Based Learning, CEVQ
   - Ages 8-12, 2.5 hours

3. **Circle of Listening** (Ethics)
   - Peace with Self & Others
   - CEVQ, Meditation
   - Ages 7-15, 1.5 hours

4. **Creating Harmony Together** (Arts)
   - Peace with Self & Others
   - Artistic Expression, Project-Based Learning
   - Ages 8-14, 2 hours

5. **The Journey of Water** (Sciences)
   - Peace with Environment
   - Project-Based Learning, Artistic Expression
   - Ages 9-13, 2.5 hours

**Future**: The 27 PDF pedagogical sheets in `FICHES PEDAGOGIQUES/` will be parsed and added to expand the database.

## ❓ FAQ

### Q: What if no similar sheets are found?
A: Lower the `min_similarity` threshold or make your criteria less specific. You can also check if your input parameters match the available vocabulary.

### Q: How do I add more lessons to the database?
A: Add them to `data/sample_data.json` and run `python src/data_loader.py`

### Q: Can I search by partial criteria?
A: Yes! Only provide the parameters you care about. Others can be None.

### Q: How accurate is the similarity?
A: The system uses semantic similarity based on ontology relationships. Accuracy depends on how well the metadata captures pedagogical concepts.

### Q: Can I export results?
A: Yes! Results are Python dictionaries - easily convert to JSON:
```python
import json
with open('results.json', 'w') as f:
    json.dump(results, f, indent=2)
```

## 🛠️ Troubleshooting

### "No module named 'similarity_engine'"
```bash
cd "path/to/Similarity Search"
venv\Scripts\activate
```

### "FileNotFoundError: ontology/peace_pedagogy.owl"
```bash
python src/ontology_builder.py
python src/data_loader.py
```

### Getting empty results
- Check your input parameters match available options
- Try broader criteria
- Verify lessons are loaded: `python test_system.py`

## 📚 See Also

- `README.md` - Full technical documentation
- `QUICK_START.md` - Quick reference
- `find_similar_lessons.py` - See full examples
- `src/query_engine.py` - Core query logic

---

**For future AI integration, you now have a clean API that returns relevant example sheets based on user input!**



