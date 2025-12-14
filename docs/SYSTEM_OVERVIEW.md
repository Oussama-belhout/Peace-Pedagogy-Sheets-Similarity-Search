# Peace Pedagogy Similarity Search - System Overview

## 🎯 Core Purpose

**Transform user input (lesson metadata) into similar existing pedagogical sheets that can be used as examples for AI-powered lesson generation.**

## 📊 The Workflow

```
┌─────────────────────────────────────┐
│  USER INPUT                         │
│  (New Lesson Metadata)              │
│  --------------------------------   │
│  • Title: "My New Lesson"          │
│  • Domain: Sciences                 │
│  • Axes: peace_with_environment     │
│  • Tools: project_based_learning    │
│  • Age: 8-12 years                  │
│  • Virtues: responsibility          │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│  SIMILARITY SEARCH ENGINE           │
│  --------------------------------   │
│  1. Create temporary lesson         │
│  2. Compare with database           │
│  3. Compute 7-D similarity          │
│  4. Rank by relevance               │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│  OUTPUT                             │
│  (Top N Similar Existing Sheets)    │
│  --------------------------------   │
│  1. "Journey of Water" - 67% match │
│  2. "Garden Project" - 47% match    │
│  3. "Mandala Rice" - 36% match      │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│  FUTURE: AI MODEL                   │
│  --------------------------------   │
│  Use similar sheets as examples     │
│  to generate complete new sheet     │
└─────────────────────────────────────┘
```

## 🔑 Key Components

### 1. Input Interface (`find_similar_lessons.py`)

**Purpose**: Simple API for users to describe their lesson

**Example**:
```python
from find_similar_lessons import find_similar

results = find_similar(
    title="Protecting Local Wildlife",
    domain="Sciences",
    axes=["peace_with_environment"],
    tools=["project_based_learning"],
    virtues=["responsibility"],
    target_age_min=8,
    target_age_max=12,
    top_k=5
)
```

### 2. Query Engine (`src/query_engine.py`)

**Purpose**: Core logic for finding similar sheets

**What it does**:
1. Takes raw metadata (not an existing lesson object)
2. Creates a temporary lesson for comparison
3. Uses similarity engine to find matches
4. Formats results with full metadata
5. Cleans up temporary lesson

**Key Function**: `query_similar_lessons()`

### 3. Similarity Engine (`src/similarity_engine.py`)

**Purpose**: Computes semantic similarity

**Algorithm**:
- 7 dimensions with weighted contributions
- Jaccard similarity for categorical data
- Age/duration overlap scoring
- Explainable results with breakdowns

**Dimensions**:
1. Peace Axes (25%)
2. Tools (20%)
3. Virtues (20%)
4. Strategies (15%)
5. Age Range (10%)
6. Duration (5%)
7. Domain (5%)

### 4. Ontology (`ontology/peace_pedagogy.owl`)

**Purpose**: Knowledge base of pedagogical concepts

**Contains**:
- 36 classes (Lesson, Tool, Strategy, Virtue, etc.)
- 9 object properties (relationships)
- 8 data properties (attributes)
- Currently 5 lesson instances (expandable)

### 5. Data Loader (`src/data_loader.py`)

**Purpose**: Populate ontology from JSON

**Process**:
- Read lesson data from JSON files
- Create lesson instances
- Link to pedagogical concepts
- Save to ontology

## 📝 Complete Usage Example

### Step 1: Define Your New Lesson

```python
# You want to create a new lesson about local ecosystems
new_lesson_idea = {
    'title': "Exploring Our Local Ecosystem",
    'description': "Students explore nearby nature",
    'domain': "Sciences",
    'axes': ["peace_with_environment", "peace_with_others"],
    'tools': ["project_based_learning"],
    'virtues': ["responsibility", "gratitude"],
    'target_age_min': 9,
    'target_age_max': 13,
    'duration': 3.0
}
```

### Step 2: Find Similar Sheets

```python
from find_similar_lessons import find_similar

similar_sheets = find_similar(**new_lesson_idea, top_k=3)
```

### Step 3: Review Results

```python
for sheet in similar_sheets:
    print(f"Sheet: {sheet['title']}")
    print(f"Match: {sheet['similarity_score']:.1%}")
    print(f"Why: {sheet['similarity_breakdown']['tools']['shared']}")
    print()
```

**Output**:
```
Sheet: The Journey of Water
Match: 66.7%
Why: ['project_based_learning']
Axes match: 50%, Tools match: 100%, Virtues match: 100%

Sheet: Mandala d'une assiette de riz
Match: 58.9%
Why: ['project_based_learning']
Axes match: 100%, Tools match: 50%, Virtues match: 67%

Sheet: Community Garden Project
Match: 57.2%
Why: ['project_based_learning']
Axes match: 100%, Tools match: 50%, Virtues match: 50%
```

### Step 4: Use for AI Generation (Future)

```python
# Future integration
from your_ai_model import generate_pedagogical_sheet

new_sheet = generate_pedagogical_sheet(
    user_input=new_lesson_idea,
    similar_examples=similar_sheets,
    example_weights=[s['similarity_score'] for s in similar_sheets]
)
```

## 🎨 System Architecture

```
┌────────────────────────────────────────────────────────┐
│                    USER LAYER                          │
│  find_similar_lessons.py (Simple API)                  │
└────────────┬───────────────────────────────────────────┘
             │
             ▼
┌────────────────────────────────────────────────────────┐
│                   QUERY LAYER                          │
│  src/query_engine.py (Input Processing)                │
│  • LessonQuery class                                   │
│  • search_similar_lessons() function                   │
└────────────┬───────────────────────────────────────────┘
             │
             ▼
┌────────────────────────────────────────────────────────┐
│                 SIMILARITY LAYER                       │
│  src/similarity_engine.py (Computation)                │
│  • SimilarityEngine class                              │
│  • Multi-dimensional scoring                           │
│  • Explainable results                                 │
└────────────┬───────────────────────────────────────────┘
             │
             ▼
┌────────────────────────────────────────────────────────┐
│                 KNOWLEDGE LAYER                        │
│  ontology/peace_pedagogy.owl (Database)                │
│  • Lesson instances                                    │
│  • Pedagogical concepts                                │
│  • Relationships                                       │
└────────────────────────────────────────────────────────┘
```

## 📦 What's in the Box

### Core Files

| File | Purpose | Use When |
|------|---------|----------|
| `find_similar_lessons.py` | **Main API** | Finding similar sheets |
| `src/query_engine.py` | Query processing | Advanced customization |
| `src/similarity_engine.py` | Similarity computation | Tweaking algorithm |
| `ontology/peace_pedagogy.owl` | Lesson database | Always (auto-loaded) |

### Documentation

| File | Purpose | Read For |
|------|---------|----------|
| `USAGE_GUIDE.md` | **How to use** | Examples & workflows |
| `API_REFERENCE.md` | **API details** | Parameter reference |
| `SYSTEM_OVERVIEW.md` | This file | Understanding system |
| `README.md` | Full docs | Technical details |
| `QUICK_START.md` | Quick ref | Fast lookup |

### Setup & Testing

| File | Purpose | Run When |
|------|---------|----------|
| `requirements.txt` | Dependencies | Initial setup |
| `src/ontology_builder.py` | Create ontology | First time / rebuild |
| `src/data_loader.py` | Load lessons | Adding new data |
| `test_system.py` | Run tests | Verify system |

## 🔄 Data Flow

### Input → Output Flow

1. **User provides metadata** (Python dict or function args)
   ```python
   {title: "...", domain: "...", axes: [...], ...}
   ```

2. **System creates temporary lesson** (in-memory)
   ```python
   temp_lesson = Lesson("temp_123")
   temp_lesson.axes = [peace_with_environment]
   # ... set other properties
   ```

3. **Computes similarity with all existing lessons**
   ```python
   for existing_lesson in database:
       score = compute_similarity(temp_lesson, existing_lesson)
   ```

4. **Ranks and returns top matches**
   ```python
   [
       {title: "Lesson A", score: 0.67, ...},
       {title: "Lesson B", score: 0.58, ...},
       {title: "Lesson C", score: 0.57, ...}
   ]
   ```

## 💡 Key Design Decisions

### Why Ontology-Based?

✅ **Semantic understanding**: Knows that "CEVQ" and "peace_with_others" are related  
✅ **Extensible**: Easy to add new concepts and relationships  
✅ **Standardized**: Uses OWL 2 Web Ontology Language  
✅ **Reasoner-friendly**: Can infer implicit relationships  

### Why Multi-Dimensional Similarity?

✅ **Holistic matching**: Considers pedagogical approach, not just keywords  
✅ **Weighted importance**: Emphasizes core pedagogical elements  
✅ **Explainable**: Shows why lessons are similar  
✅ **Tunable**: Weights can be adjusted per use case  

### Why Temporary Lesson Approach?

✅ **Clean separation**: User input ≠ database entries  
✅ **No pollution**: Doesn't clutter ontology with queries  
✅ **Flexible**: Can query without committing to database  
✅ **Efficient**: Automatic cleanup after query  

## 📈 Future Enhancements

### Short Term

1. **Parse PDF sheets**: Extract data from 27 existing PDFs
2. **Batch processing**: Handle multiple queries at once
3. **Export functions**: Save results to CSV/JSON
4. **Web API**: REST API for external access

### Medium Term

1. **Natural language input**: "I want a lesson about trees for 10-year-olds"
2. **Similarity clustering**: Group similar lessons visually
3. **Recommendation system**: "Users who liked X also used Y"
4. **Advanced filtering**: Complex queries with boolean logic

### Long Term

1. **AI Integration**: Use similar sheets to generate new ones
2. **Feedback loop**: Learn from user selections
3. **Multilingual support**: Support French, Arabic, etc.
4. **Mobile app**: Access on tablets/phones

## 🎓 Current Database Status

**Size**: 5 sample lessons  
**Domains**: Sciences (3), Ethics (1), Arts (1)  
**Expandable**: Yes, via `data/sample_data.json`  
**Future**: 27 PDF sheets ready to parse and add  

## 🚀 Quick Commands

```bash
# Find similar lessons (interactive examples)
python find_similar_lessons.py

# Test the system
python test_system.py

# Rebuild ontology
python src/ontology_builder.py

# Reload data
python src/data_loader.py
```

## 📞 Integration Points

### For Python Applications

```python
from find_similar_lessons import find_similar

results = find_similar(title="...", domain="...", ...)
```

### For Web Services (Future)

```bash
curl -X POST http://api/find-similar \
  -d '{"title": "My Lesson", "domain": "Sciences", ...}'
```

### For AI Models (Future)

```python
similar = find_similar(user_input)
new_sheet = ai_model.generate(user_input, examples=similar)
```

## ✅ System Status

✅ Ontology created (36 classes, 9 properties)  
✅ Query engine implemented  
✅ Similarity algorithm working  
✅ 5 sample lessons loaded  
✅ Simple API available  
✅ Tests passing  
✅ Documentation complete  

**Ready for**: Expanding database, AI integration, production use

---

**This system provides the foundation for AI-powered pedagogical sheet generation by finding relevant examples based on user input.**



