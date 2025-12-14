# Peace Pedagogy Similarity Search System

A semantic similarity search system for pedagogical sheets based on Peace Pedagogy (ECP - Éducation à la Culture de Paix) principles using ontology-based knowledge representation.

## Project Overview

This system creates a formal ontology for Peace Pedagogy lessons and provides semantic similarity search capabilities to find related lessons based on multiple pedagogical dimensions including:

- **Peace Axes**: Peace with Self, Peace with Others, Peace with Environment
- **Pedagogical Tools**: CEVQ, Meditation, Project-Based Learning, etc.
- **Virtues**: Gratitude, Empathy, Responsibility, Compassion, etc.
- **Teaching Strategies**: Experiential Learning, Dialogical Approach, etc.
- **Age Ranges**: Target age groups for lessons
- **Duration**: Lesson duration compatibility
- **Academic Domains**: Sciences, Arts, Ethics, Languages

## Features

✅ **Ontology-Based Knowledge Representation**: Formal OWL ontology built with Owlready2  
✅ **Multi-Dimensional Similarity**: Weighted similarity across 7 pedagogical dimensions  
✅ **Explainable Results**: Breakdown of similarity scores by dimension  
✅ **Flexible Search**: Find similar lessons or search by specific criteria  
✅ **Extensible**: Easy to add new lessons, tools, virtues, and strategies  

## Project Structure

```
peace-pedagogy-similarity/
├── data/
│   ├── lessons/              # Additional lesson data
│   └── sample_data.json      # Sample lesson data
├── ontology/
│   └── peace_pedagogy.owl    # OWL ontology file
├── src/
│   ├── __init__.py
│   ├── ontology_builder.py   # Creates the ontology
│   ├── similarity_engine.py  # Similarity computation
│   └── data_loader.py        # Loads lessons into ontology
├── tests/                    # Unit tests
├── notebooks/                # Jupyter notebooks for analysis
├── FICHES PEDAGOGIQUES/      # Pedagogical sheets (PDF)
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

## Installation

### Prerequisites

- Python 3.8 or higher
- Java (for Protégé visualization - optional)

### Setup

1. **Clone or download the project**

2. **Create virtual environment**:
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate
   
   # Mac/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Quick Start

### 1. Create the Ontology

```bash
python src/ontology_builder.py
```

This creates the Peace Pedagogy ontology with:
- 36 classes (Lesson, Tool, Strategy, Virtue, Domain, etc.)
- 9 object properties (hasAxis, usesTool, developsVirtue, etc.)
- 8 data properties (title, duration, targetAgeMin, etc.)

### 2. Load Lesson Data

```bash
python src/data_loader.py
```

This loads sample lessons from `data/sample_data.json` into the ontology.

### 3. Test Similarity Search

```bash
python src/similarity_engine.py
```

This demonstrates finding similar lessons with detailed similarity breakdowns.

## Usage Examples

### Finding Similar Lessons

```python
from owlready2 import get_ontology
from src.similarity_engine import SimilarityEngine

# Load ontology
onto = get_ontology("ontology/peace_pedagogy.owl").load()

# Create similarity engine
engine = SimilarityEngine(onto)

# Get a lesson
lessons = list(onto.Lesson.instances())
target_lesson = lessons[0]

# Find 5 most similar lessons
similar = engine.find_similar(target_lesson, top_k=5, min_similarity=0.3)

for lesson, score, breakdown in similar:
    print(f"{lesson.title[0]}: {score:.3f}")
    print(f"  Shared axes: {breakdown['axes']['shared']}")
    print(f"  Shared tools: {breakdown['tools']['shared']}")
```

### Searching by Criteria

```python
# Find lessons for peace with environment, ages 8-12
matching = engine.search_by_criteria(
    axes=["peace_with_environment"],
    age_min=8,
    age_max=12
)

for lesson in matching:
    print(f"- {lesson.title[0]}")
```

### Custom Similarity Weights

```python
# Adjust weights for different dimensions
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

## Sample Output

```
Found 5 lessons in ontology

Finding lessons similar to: Mandala d'une assiette de riz
================================================================================

1. Community Garden Project
   Overall Similarity: 0.664
   - Peace Axes: 1.00 (shared: ['peace_with_others', 'peace_with_environment'])
   - Tools: 1.00 (shared: ['cevq', 'project_based_learning'])
   - Virtues: 0.33 (shared: ['responsibility'])
   - Strategies: 0.33

2. The Journey of Water
   Overall Similarity: 0.506
   - Peace Axes: 0.50 (shared: ['peace_with_environment'])
   - Tools: 0.50 (shared: ['project_based_learning'])
   - Virtues: 0.67 (shared: ['gratitude', 'responsibility'])
   - Strategies: 0.33
```

## Data Format

Lessons are stored in JSON format:

```json
{
  "lessons": [
    {
      "id": "mandala_rice",
      "title": "Mandala d'une assiette de riz",
      "description": "Awakening to interdependence...",
      "domain": "Sciences",
      "discipline": "économie de la nature",
      "axes": ["peace_with_environment", "peace_with_others"],
      "tools": ["cevq", "project_based_learning"],
      "strategies": ["experiential_learning", "awakening_alterity"],
      "virtues": ["gratitude", "empathy", "responsibility"],
      "objectives": ["understand_interdependence", "develop_gratitude"],
      "target_age_min": 6,
      "target_age_max": 14,
      "duration": 3.0,
      "group_size_min": 15,
      "group_size_max": 25
    }
  ]
}
```

## Similarity Algorithm

The system computes semantic similarity using a weighted multi-dimensional approach:

1. **Peace Axes** (25%): Jaccard similarity of peace dimensions
2. **Tools** (20%): Jaccard similarity of pedagogical tools
3. **Virtues** (20%): Jaccard similarity of cultivated virtues
4. **Strategies** (15%): Jaccard similarity of teaching strategies
5. **Age Range** (10%): Overlap of target age ranges
6. **Duration** (5%): Ratio of lesson durations
7. **Domain** (5%): Same academic domain or not

**Final Score** = Σ(dimension_weight × dimension_similarity)

### Jaccard Similarity

For categorical dimensions (axes, tools, virtues, strategies):

```
J(A,B) = |A ∩ B| / |A ∪ B|
```

## Visualizing with Protégé

1. Download Protégé from the `Protege` folder or [official website](https://protege.stanford.edu/)
2. Open Protégé
3. File → Open → Select `ontology/peace_pedagogy.owl`
4. Explore:
   - **Entities** tab: View class hierarchy
   - **Object Properties**: View relationships
   - **Individuals**: View lesson instances
5. Run reasoner: Reasoner → Pellet → Start Reasoner

## Extending the System

### Adding New Lessons

Add to `data/sample_data.json` or create a new JSON file, then:

```bash
python src/data_loader.py
```

### Adding New Virtues or Tools

Edit `src/ontology_builder.py` to add new classes:

```python
class NewVirtue(Virtue):
    pass

new_virtue = NewVirtue("new_virtue")
```

Then rebuild the ontology:

```bash
python src/ontology_builder.py
```

## Technical Details

### Dependencies

- **owlready2**: OWL ontology manipulation
- **rdflib**: RDF graph operations
- **numpy**: Numerical computations
- **pandas**: Data manipulation
- **scikit-learn**: Machine learning utilities

### Ontology Structure

**Main Classes**:
- `EducationalComponent`: Base class for educational elements
  - `Lesson`: Specific lessons
  - `Tool`: Pedagogical tools
  - `Strategy`: Teaching strategies
  - `Domain`: Academic domains
- `PeaceComponent`: Peace-related concepts
  - `PeaceAxis`: Three peace relationships
  - `Virtue`: Cultivated values
- `LearningObjective`: Learning goals

**Key Properties**:
- `hasAxis`: Links lessons to peace axes
- `usesTool`: Links lessons to tools
- `developsVirtue`: Links lessons to virtues
- `employsStrategy`: Links lessons to strategies
- `belongsToDomain`: Links lessons to domains

## Troubleshooting

### Import Errors

If you get `ModuleNotFoundError`, ensure virtual environment is activated:
```bash
# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

Then reinstall:
```bash
pip install -r requirements.txt
```

### Path Too Long (Windows)

If installation fails with path length errors, enable long paths:
1. Run as Administrator: `gpedit.msc`
2. Navigate to: Local Computer Policy → Computer Configuration → Administrative Templates → System → Filesystem
3. Enable "Enable Win32 long paths"

Or install packages individually:
```bash
pip install owlready2 rdflib numpy pandas scikit-learn
```

## Future Enhancements

- [ ] Web interface for similarity search
- [ ] Natural language query processing
- [ ] Integration with real pedagogical sheets (PDF parsing)
- [ ] Recommendation system for lesson sequences
- [ ] Collaborative filtering based on teacher feedback
- [ ] Export results to various formats (CSV, JSON, PDF)
- [ ] Visualization of lesson similarity networks
- [ ] Multi-language support

## Contributing

To contribute to this project:

1. Add new lessons to `data/` folder
2. Extend ontology classes in `src/ontology_builder.py`
3. Improve similarity metrics in `src/similarity_engine.py`
4. Add tests in `tests/` folder

## License

This project is part of the Peace Pedagogy initiative at UNICA M1.

## References

- Peace Pedagogy (ECP - Éducation à la Culture de Paix)
- OWL 2 Web Ontology Language
- Owlready2 Documentation: https://owlready2.readthedocs.io/
- Protégé: https://protege.stanford.edu/

## Contact

For questions or collaboration opportunities regarding Peace Pedagogy, please reach out to the DS4H project team.

---

**Built with ❤️ for Peace Education**



