# Peace Pedagogy Similarity Search - Quick Start Guide

## What We Built

A complete semantic similarity search system for Peace Pedagogy lessons with:

✅ **OWL Ontology**: Formal knowledge representation with 36 classes  
✅ **5 Sample Lessons**: Pre-loaded pedagogical sheets  
✅ **Similarity Engine**: Multi-dimensional similarity computation  
✅ **Search Capabilities**: Find similar lessons or search by criteria  

## Project Status

### ✅ Completed Components

1. **Ontology** (`ontology/peace_pedagogy.owl`)
   - 36 classes (Lesson, Tool, Strategy, Virtue, Domain, etc.)
   - 9 object properties (hasAxis, usesTool, developsVirtue, etc.)
   - 8 data properties (title, duration, targetAge, etc.)

2. **Data Loader** (`src/data_loader.py`)
   - Loads lessons from JSON into the ontology
   - Handles relationships (axes, tools, virtues, strategies)

3. **Similarity Engine** (`src/similarity_engine.py`)
   - Computes similarity across 7 dimensions
   - Returns explainable results with breakdowns
   - Supports custom weight configurations

4. **Sample Data** (`data/sample_data.json`)
   - 5 example lessons covering different domains
   - Arts, Sciences, Ethics domains
   - Various peace axes and pedagogical tools

## How to Use

### 1. Run Tests

```bash
# Activate virtual environment
venv\Scripts\activate

# Run test suite
python test_system.py
```

### 2. Find Similar Lessons

```python
from owlready2 import get_ontology
from src.similarity_engine import SimilarityEngine

# Load ontology
onto = get_ontology("ontology/peace_pedagogy.owl").load()
engine = SimilarityEngine(onto)

# Get a lesson
lesson = list(onto.Lesson.instances())[0]

# Find similar lessons
similar = engine.find_similar(lesson, top_k=3)

for other_lesson, score, breakdown in similar:
    print(f"{other_lesson.title[0]}: {score:.3f}")
```

### 3. View All Lessons

```python
from owlready2 import get_ontology

onto = get_ontology("ontology/peace_pedagogy.owl").load()

for lesson in onto.Lesson.instances():
    print(f"- {lesson.title[0]}")
```

## Current Sample Lessons

1. **Mandala d'une assiette de riz** (Sciences)
   - Focus: Peace with Environment, Peace with Others
   - Tools: CEVQ, Project-Based Learning
   - Virtues: Gratitude, Empathy, Responsibility

2. **Community Garden Project** (Sciences)
   - Focus: Peace with Environment, Peace with Others
   - Tools: Project-Based Learning, CEVQ
   - Virtues: Responsibility, Patience

3. **Circle of Listening** (Ethics)
   - Focus: Peace with Self, Peace with Others
   - Tools: CEVQ, Meditation
   - Virtues: Empathy, Patience, Benevolence

4. **Creating Harmony Together** (Arts)
   - Focus: Peace with Self, Peace with Others
   - Tools: Artistic Expression, Project-Based Learning
   - Virtues: Patience, Benevolence, Empathy

5. **The Journey of Water** (Sciences)
   - Focus: Peace with Environment
   - Tools: Project-Based Learning, Artistic Expression
   - Virtues: Responsibility, Gratitude

## Example Results

When searching for lessons similar to "Mandala d'une assiette de riz":

```
1. Community Garden Project: 0.664
   - Peace Axes: 1.00 (100% match)
   - Tools: 1.00 (100% match)
   - Virtues: 0.33 (33% match)
   - Shared: Both focus on environmental peace and collaboration

2. The Journey of Water: 0.506
   - Peace Axes: 0.50 (50% match)
   - Tools: 0.50 (50% match)
   - Virtues: 0.67 (67% match)
   - Shared: Environmental focus and gratitude
```

## Next Steps

### To Add More Lessons

1. Edit `data/sample_data.json` or create a new JSON file
2. Add lessons following this format:

```json
{
  "id": "your_lesson_id",
  "title": "Your Lesson Title",
  "description": "Description here",
  "domain": "Sciences",
  "axes": ["peace_with_self"],
  "tools": ["meditation"],
  "virtues": ["patience"],
  "target_age_min": 8,
  "target_age_max": 12,
  "duration": 2.0,
  "group_size_min": 15,
  "group_size_max": 25
}
```

3. Run the data loader:

```bash
python src/data_loader.py
```

### To Integrate Real Pedagogical Sheets

The `FICHES PEDAGOGIQUES` folder contains 27 real pedagogical sheets in PDF format:

- **Sciences**: 12 sheets
- **Ethique**: 11 sheets  
- **Arts**: 3 sheets
- **Langues**: 2 sheets

**Future Enhancement**: Parse these PDFs and extract structured data to populate the ontology.

### To Customize Similarity Weights

Edit weights in your code:

```python
engine.weights = {
    'axes': 0.30,       # Emphasize peace axes
    'tools': 0.15,
    'virtues': 0.25,    # Emphasize virtues
    'strategies': 0.15,
    'age': 0.10,
    'duration': 0.03,
    'domain': 0.02
}
```

### To Visualize with Protégé

1. Open `Protege/Protege-5.6.7/Protege.exe`
2. File → Open → Select `ontology/peace_pedagogy.owl`
3. Explore classes, properties, and instances
4. Run reasoner for inference

## File Structure

```
Similarity Search/
├── data/
│   ├── sample_data.json          # Sample lesson data
│   └── lessons/                  # Additional lessons (empty)
├── ontology/
│   └── peace_pedagogy.owl        # Main ontology file
├── src/
│   ├── __init__.py
│   ├── ontology_builder.py       # Creates ontology
│   ├── data_loader.py            # Loads lessons
│   └── similarity_engine.py      # Similarity computation
├── FICHES PEDAGOGIQUES/          # 27 PDF pedagogical sheets
├── venv/                         # Virtual environment
├── requirements.txt              # Dependencies
├── README.md                     # Full documentation
├── QUICK_START.md               # This file
├── test_system.py               # Test suite
└── demo.py                      # Interactive demo
```

## Common Commands

```bash
# Activate environment
venv\Scripts\activate

# Run tests
python test_system.py

# Rebuild ontology
python src/ontology_builder.py

# Reload data
python src/data_loader.py

# Test similarity
python src/similarity_engine.py

# Interactive demo (optional)
python demo.py
```

## Troubleshooting

### "No module named 'owlready2'"

```bash
venv\Scripts\activate
pip install -r requirements.txt
```

### "FileNotFoundError: ontology/peace_pedagogy.owl"

```bash
python src/ontology_builder.py
python src/data_loader.py
```

### "No lessons found"

```bash
python src/data_loader.py
```

## Technical Details

**Similarity Algorithm**: Weighted Jaccard similarity across 7 dimensions

**Dimensions**:
- Peace Axes (25%)
- Tools (20%)
- Virtues (20%)
- Strategies (15%)
- Age Range (10%)
- Duration (5%)
- Domain (5%)

**Formula**: `similarity = Σ(weight_i × jaccard_i)`

## Support

For questions or issues:
1. Check `README.md` for detailed documentation
2. Run `python test_system.py` to verify installation
3. Review the guide in `similarity_project_guide.md`

---

**Built for Peace Pedagogy Education (ECP)**  
*UNICA M1 - DS4H Project*



