# Step-by-Step Guide: Peace Pedagogy Similarity Search Project

## Project Overview

You'll build a system that:
1. Creates an ontology for Peace Pedagogy (ECP)
2. Loads lesson supports into the ontology
3. Performs semantic similarity searches
4. Returns the most relevant lessons based on pedagogical criteria


---


### Step 1.1 : check python is installed

### Step 1.2: Create Project Directory

```bash
# Create project folder
mkdir peace-pedagogy-similarity
cd peace-pedagogy-similarity

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Your prompt should now show (venv)
```

### Step 1.3: Install Python Libraries

```bash
# Install core libraries
pip install owlready2
pip install rdflib
pip install numpy
pip install pandas
pip install scikit-learn

# Install optional but useful libraries
pip install jupyter  # For interactive development
pip install matplotlib  # For visualization

# Save dependencies
pip freeze > requirements.txt
```

### Step 1.4: Check java is installed

### Step 1.5: Download Protégé (already in the directory "Protege")
---

## PHASE 2: Create Project Structure (10 minutes)

### Step 2.1: Create Directory Structure

```bash
# Inside peace-pedagogy-similarity/
mkdir data
mkdir ontology
mkdir src
mkdir tests
mkdir notebooks

# Create empty files
touch src/__init__.py
touch src/ontology_builder.py
touch src/similarity_engine.py
touch src/data_loader.py
touch README.md
```

**Final structure:**
```
peace-pedagogy-similarity/
├── venv/
├── data/
│   ├── lessons/          # JSON files for lessons
│   └── sample_data.json
├── ontology/
│   └── peace_pedagogy.owl
├── src/
│   ├── __init__.py
│   ├── ontology_builder.py
│   ├── similarity_engine.py
│   └── data_loader.py
├── tests/
├── notebooks/
├── requirements.txt
└── README.md
```

---

## PHASE 3: Build the Ontology (45 minutes)

### Step 3.1: Create `src/ontology_builder.py`

```python
"""
Peace Pedagogy Ontology Builder
Creates the formal ontology structure for ECP lessons
"""

from owlready2 import *

def create_peace_pedagogy_ontology():
    """
    Creates the Peace Pedagogy ontology with all classes, properties, and rules
    """
    
    # Create ontology
    onto = get_ontology("http://www.semanticweb.org/peace-pedagogy/ontology")
    
    with onto:
        # ==================== CLASSES ====================
        
        # Main Educational Components
        class EducationalComponent(Thing):
            """Base class for all educational elements"""
            pass
        
        class Lesson(EducationalComponent):
            """A specific lesson following Peace Pedagogy"""
            pass
        
        class Tool(EducationalComponent):
            """Pedagogical tools used in lessons"""
            pass
        
        class Strategy(EducationalComponent):
            """Teaching strategies and methodologies"""
            pass
        
        class Domain(EducationalComponent):
            """Academic domains (Sciences, Arts, etc.)"""
            pass
        
        # Peace Components
        class PeaceComponent(Thing):
            """Base class for peace-related concepts"""
            pass
        
        class PeaceAxis(PeaceComponent):
            """The three fundamental peace relationships"""
            pass
        
        class Virtue(PeaceComponent):
            """Virtues and values cultivated in lessons"""
            pass
        
        class LearningObjective(Thing):
            """Learning objectives"""
            pass
        
        # ==================== SUBCLASSES ====================
        
        # Peace Axes
        class PeaceWithSelf(PeaceAxis):
            pass
        
        class PeaceWithOthers(PeaceAxis):
            pass
        
        class PeaceWithEnvironment(PeaceAxis):
            pass
        
        # Tools
        class CEVQ(Tool):
            """Cercle d'Éveil aux Vertus et aux Qualités"""
            pass
        
        class Meditation(Tool):
            pass
        
        class ProjectBasedLearning(Tool):
            pass
        
        class ArtisticExpression(Tool):
            pass
        
        class SolutionOrientedLearning(Tool):
            pass
        
        # Strategies
        class ExperientialLearning(Strategy):
            pass
        
        class DialogicalApproach(Strategy):
            pass
        
        class StructuredQuestioning(Strategy):
            pass
        
        class AwakeningAlterity(Strategy):
            """Awakening of alterity - understanding others"""
            pass
        
        class CollaborativeConstruction(Strategy):
            pass
        
        # Domains
        class Sciences(Domain):
            pass
        
        class Arts(Domain):
            pass
        
        class Ethics(Domain):
            pass
        
        class Languages(Domain):
            pass
        
        # Virtues
        class Gratitude(Virtue):
            pass
        
        class Empathy(Virtue):
            pass
        
        class Responsibility(Virtue):
            pass
        
        class Compassion(Virtue):
            pass
        
        class Patience(Virtue):
            pass
        
        class Benevolence(Virtue):
            pass
        
        # Learning Objectives
        class CognitiveObjective(LearningObjective):
            pass
        
        class SocioEmotionalObjective(LearningObjective):
            pass
        
        class BehavioralObjective(LearningObjective):
            pass
        
        class EthicalObjective(LearningObjective):
            pass
        
        # ==================== OBJECT PROPERTIES ====================
        
        class hasAxis(ObjectProperty):
            """Links a lesson to its peace axes"""
            domain = [Lesson]
            range = [PeaceAxis]
        
        class usesTool(ObjectProperty):
            """Links a lesson to pedagogical tools"""
            domain = [Lesson]
            range = [Tool]
        
        class employsStrategy(ObjectProperty):
            """Links a lesson to teaching strategies"""
            domain = [Lesson]
            range = [Strategy]
        
        class belongsToDomain(ObjectProperty):
            """Links a lesson to an academic domain"""
            domain = [Lesson]
            range = [Domain]
        
        class developsVirtue(ObjectProperty):
            """Links a lesson to virtues it cultivates"""
            domain = [Lesson]
            range = [Virtue]
        
        class hasObjective(ObjectProperty):
            """Links a lesson to learning objectives"""
            domain = [Lesson]
            range = [LearningObjective]
        
        class supports(ObjectProperty):
            """Links a tool to peace axes it supports"""
            domain = [Tool]
            range = [PeaceAxis]
        
        class cultivates(ObjectProperty):
            """Links a strategy to virtues it cultivates"""
            domain = [Strategy]
            range = [Virtue]
        
        class prerequisiteOf(ObjectProperty):
            """Links lessons in a prerequisite chain"""
            domain = [Lesson]
            range = [Lesson]
        
        # ==================== DATA PROPERTIES ====================
        
        class title(DataProperty):
            """Lesson title"""
            domain = [Lesson]
            range = [str]
        
        class description(DataProperty):
            """Textual description"""
            domain = [Thing]
            range = [str]
        
        class duration(DataProperty):
            """Duration in hours"""
            domain = [Lesson]
            range = [float]
        
        class targetAgeMin(DataProperty):
            """Minimum target age"""
            domain = [Lesson]
            range = [int]
        
        class targetAgeMax(DataProperty):
            """Maximum target age"""
            domain = [Lesson]
            range = [int]
        
        class groupSizeMin(DataProperty):
            """Minimum group size"""
            domain = [Lesson]
            range = [int]
        
        class groupSizeMax(DataProperty):
            """Maximum group size"""
            domain = [Lesson]
            range = [int]
        
        class discipline(DataProperty):
            """Specific discipline within domain"""
            domain = [Lesson]
            range = [str]
        
        # ==================== INSTANCES (VOCABULARY) ====================
        
        # Create standard instances for axes
        peace_self = PeaceWithSelf("peace_with_self")
        peace_others = PeaceWithOthers("peace_with_others")
        peace_env = PeaceWithEnvironment("peace_with_environment")
        
        # Create standard tool instances
        cevq = CEVQ("cevq")
        cevq.description = ["Cercle d'Éveil aux Vertus et aux Qualités - Circle for awakening virtues and qualities"]
        
        meditation = Meditation("meditation")
        meditation.description = ["Mindfulness and inner calm practices"]
        
        project_learning = ProjectBasedLearning("project_based_learning")
        project_learning.description = ["Collaborative project-based approach"]
        
        # Create standard virtue instances
        gratitude = Gratitude("gratitude")
        empathy = Empathy("empathy")
        responsibility = Responsibility("responsibility")
        compassion = Compassion("compassion")
        
        # Define tool-axis relationships
        cevq.supports = [peace_others, peace_self]
        meditation.supports = [peace_self]
        project_learning.supports = [peace_others, peace_env]
        
    return onto


def save_ontology(onto, filepath="ontology/peace_pedagogy.owl"):
    """
    Save the ontology to a file
    """
    onto.save(file=filepath, format="rdfxml")
    print(f"Ontology saved to {filepath}")


if __name__ == "__main__":
    print("Creating Peace Pedagogy Ontology...")
    ontology = create_peace_pedagogy_ontology()
    
    print(f"Created {len(list(ontology.classes()))} classes")
    print(f"Created {len(list(ontology.object_properties()))} object properties")
    print(f"Created {len(list(ontology.data_properties()))} data properties")
    
    save_ontology(ontology)
    print("Done!")
```

### Step 3.2: Run the Ontology Builder

```bash
# Make sure you're in the project directory with venv activated
cd peace-pedagogy-similarity
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Run the builder
python src/ontology_builder.py
```

**Expected Output:**
```
Creating Peace Pedagogy Ontology...
Created 35 classes
Created 10 object properties
Created 9 data properties
Ontology saved to ontology/peace_pedagogy.owl
Done!
```

### Step 3.3: Verify with Protégé (Optional)

1. Open Protégé
2. File → Open → Select `ontology/peace_pedagogy.owl`
3. Explore the class hierarchy in the "Classes" tab
4. Check properties in the "Object Properties" tab
5. Run the reasoner: Reasoner → Pellet → Start Reasoner

---

## PHASE 4: Create Sample Data (20 minutes)

### Step 4.1: Create `data/sample_data.json`

```json
{
  "lessons": [
    {
      "id": "mandala_rice",
      "title": "Mandala d'une assiette de riz",
      "description": "Awakening to interdependence through visualization of a rice meal's origins",
      "domain": "Sciences",
      "discipline": "économie de la nature",
      "axes": ["peace_with_environment", "peace_with_others"],
      "tools": ["cevq", "project_based_learning"],
      "strategies": ["experiential_learning", "awakening_alterity"],
      "virtues": ["gratitude", "empathy", "responsibility"],
      "objectives": ["understand_interdependence", "develop_gratitude", "ecological_awareness"],
      "target_age_min": 6,
      "target_age_max": 14,
      "duration": 3.0,
      "group_size_min": 15,
      "group_size_max": 25
    },
    {
      "id": "community_garden",
      "title": "Community Garden Project",
      "description": "Creating and maintaining a shared garden to learn about ecosystems and collaboration",
      "domain": "Sciences",
      "discipline": "ecology",
      "axes": ["peace_with_environment", "peace_with_others"],
      "tools": ["project_based_learning", "cevq"],
      "strategies": ["experiential_learning", "collaborative_construction"],
      "virtues": ["responsibility", "patience", "cooperation"],
      "objectives": ["ecological_awareness", "collaborative_skills", "patience"],
      "target_age_min": 8,
      "target_age_max": 12,
      "duration": 2.5,
      "group_size_min": 10,
      "group_size_max": 20
    },
    {
      "id": "peace_circle",
      "title": "Circle of Listening",
      "description": "A CEVQ session focused on active listening and empathy",
      "domain": "Ethics",
      "discipline": "communication",
      "axes": ["peace_with_self", "peace_with_others"],
      "tools": ["cevq", "meditation"],
      "strategies": ["dialogical_approach", "structured_questioning"],
      "virtues": ["empathy", "patience", "benevolence"],
      "objectives": ["active_listening", "emotional_regulation", "empathy_development"],
      "target_age_min": 7,
      "target_age_max": 15,
      "duration": 1.5,
      "group_size_min": 12,
      "group_size_max": 25
    },
    {
      "id": "musical_harmony",
      "title": "Creating Harmony Together",
      "description": "Collaborative music creation to experience harmony and cooperation",
      "domain": "Arts",
      "discipline": "music",
      "axes": ["peace_with_self", "peace_with_others"],
      "tools": ["artistic_expression", "project_based_learning"],
      "strategies": ["experiential_learning", "collaborative_construction"],
      "virtues": ["patience", "benevolence", "empathy"],
      "objectives": ["emotional_expression", "collaborative_skills", "inner_harmony"],
      "target_age_min": 8,
      "target_age_max": 14,
      "duration": 2.0,
      "group_size_min": 15,
      "group_size_max": 30
    },
    {
      "id": "water_cycle",
      "title": "The Journey of Water",
      "description": "Understanding water cycle and our responsibility to water resources",
      "domain": "Sciences",
      "discipline": "environmental_science",
      "axes": ["peace_with_environment"],
      "tools": ["project_based_learning", "artistic_expression"],
      "strategies": ["experiential_learning", "structured_questioning"],
      "virtues": ["responsibility", "gratitude"],
      "objectives": ["ecological_awareness", "systems_thinking", "environmental_responsibility"],
      "target_age_min": 9,
      "target_age_max": 13,
      "duration": 2.5,
      "group_size_min": 15,
      "group_size_max": 25
    }
  ]
}
```

---

## PHASE 5: Build Data Loader (30 minutes)

### Step 5.1: Create `src/data_loader.py`

```python
"""
Data Loader for Peace Pedagogy Lessons
Loads lesson data and populates the ontology
"""

import json
from owlready2 import *


class LessonLoader:
    """
    Loads lessons from JSON into the ontology
    """
    
    def __init__(self, ontology):
        self.onto = ontology
    
    def normalize_name(self, name):
        """Convert string to valid ontology name"""
        return name.lower().replace(" ", "_").replace("'", "").replace("é", "e").replace("è", "e")
    
    def load_from_json(self, json_file):
        """
        Load lessons from JSON file into ontology
        """
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        lessons_created = []
        
        with self.onto:
            for lesson_data in data['lessons']:
                lesson = self.create_lesson(lesson_data)
                lessons_created.append(lesson)
        
        return lessons_created
    
    def create_lesson(self, lesson_data):
        """
        Create a lesson instance from data dictionary
        """
        # Get Lesson class
        Lesson = self.onto.Lesson
        
        # Create lesson instance
        lesson_id = self.normalize_name(lesson_data['id'])
        lesson = Lesson(lesson_id)
        
        # Set data properties
        lesson.title = [lesson_data['title']]
        lesson.description = [lesson_data.get('description', '')]
        lesson.discipline = [lesson_data.get('discipline', '')]
        lesson.duration = [lesson_data.get('duration', 0.0)]
        lesson.targetAgeMin = [lesson_data.get('target_age_min', 0)]
        lesson.targetAgeMax = [lesson_data.get('target_age_max', 0)]
        lesson.groupSizeMin = [lesson_data.get('group_size_min', 0)]
        lesson.groupSizeMax = [lesson_data.get('group_size_max', 0)]
        
        # Link to axes
        for axis_name in lesson_data.get('axes', []):
            axis = self.onto.search_one(iri=f"*{axis_name}")
            if axis:
                lesson.hasAxis.append(axis)
        
        # Link to tools
        for tool_name in lesson_data.get('tools', []):
            tool = self.onto.search_one(iri=f"*{tool_name}")
            if tool:
                lesson.usesTool.append(tool)
        
        # Link to strategies
        for strategy_name in lesson_data.get('strategies', []):
            # Try to find or create strategy
            strategy_class_name = ''.join(word.capitalize() for word in strategy_name.split('_'))
            strategy_class = getattr(self.onto, strategy_class_name, None)
            if strategy_class:
                strategy = strategy_class(strategy_name)
                lesson.employsStrategy.append(strategy)
        
        # Link to virtues
        for virtue_name in lesson_data.get('virtues', []):
            virtue = self.onto.search_one(iri=f"*{virtue_name}")
            if virtue:
                lesson.developsVirtue.append(virtue)
        
        # Link to domain
        domain_name = lesson_data.get('domain', '')
        domain = self.onto.search_one(iri=f"*{domain_name.lower()}")
        if domain:
            lesson.belongsToDomain = [domain]
        
        return lesson


def load_lessons(ontology_path, data_path):
    """
    Load ontology and populate with lesson data
    """
    # Load ontology
    onto = get_ontology(ontology_path).load()
    
    # Create loader
    loader = LessonLoader(onto)
    
    # Load lessons
    lessons = loader.load_from_json(data_path)
    
    print(f"Loaded {len(lessons)} lessons into ontology")
    
    # Save updated ontology
    onto.save()
    
    return onto, lessons


if __name__ == "__main__":
    ontology_path = "ontology/peace_pedagogy.owl"
    data_path = "data/sample_data.json"
    
    onto, lessons = load_lessons(ontology_path, data_path)
    
    print("\nCreated lessons:")
    for lesson in lessons:
        print(f"  - {lesson.title[0]}")
```

### Step 5.2: Run the Data Loader

```bash
python src/data_loader.py
```

**Expected Output:**
```
Loaded 5 lessons into ontology

Created lessons:
  - Mandala d'une assiette de riz
  - Community Garden Project
  - Circle of Listening
  - Creating Harmony Together
  - The Journey of Water
```

---

## PHASE 6: Build Similarity Engine (45 minutes)

### Step 6.1: Create `src/similarity_engine.py`

```python
"""
Semantic Similarity Engine for Peace Pedagogy Lessons
Computes multi-dimensional similarity between lessons
"""

from owlready2 import *
import numpy as np
from typing import List, Tuple, Dict


class SimilarityEngine:
    """
    Computes semantic similarity between Peace Pedagogy lessons
    """
    
    def __init__(self, ontology):
        self.onto = ontology
        
        # Weights for different dimensions
        self.weights = {
            'axes': 0.25,
            'tools': 0.20,
            'virtues': 0.20,
            'strategies': 0.15,
            'age': 0.10,
            'duration': 0.05,
            'domain': 0.05
        }
    
    def jaccard_similarity(self, set1, set2):
        """
        Compute Jaccard similarity between two sets
        J(A,B) = |A ∩ B| / |A ∪ B|
        """
        if not set1 or not set2:
            return 0.0
        
        intersection = len(set1 & set2)
        union = len(set1 | set2)
        
        if union == 0:
            return 0.0
        
        return intersection / union
    
    def age_similarity(self, lesson1, lesson2):
        """
        Compute age range compatibility
        """
        age1_min = lesson1.targetAgeMin[0] if lesson1.targetAgeMin else 0
        age1_max = lesson1.targetAgeMax[0] if lesson1.targetAgeMax else 0
        age2_min = lesson2.targetAgeMin[0] if lesson2.targetAgeMin else 0
        age2_max = lesson2.targetAgeMax[0] if lesson2.targetAgeMax else 0
        
        if age1_min == 0 or age2_min == 0:
            return 0.0
        
        # Calculate overlap
        overlap_start = max(age1_min, age2_min)
        overlap_end = min(age1_max, age2_max)
        
        if overlap_start > overlap_end:
            return 0.0  # No overlap
        
        overlap = overlap_end - overlap_start + 1
        range1 = age1_max - age1_min + 1
        range2 = age2_max - age2_min + 1
        
        return overlap / max(range1, range2)
    
    def duration_similarity(self, lesson1, lesson2):
        """
        Compute duration compatibility
        """
        dur1 = lesson1.duration[0] if lesson1.duration else 0
        dur2 = lesson2.duration[0] if lesson2.duration else 0
        
        if dur1 == 0 or dur2 == 0:
            return 0.0
        
        # Ratio of shorter to longer
        return min(dur1, dur2) / max(dur1, dur2)
    
    def domain_similarity(self, lesson1, lesson2):
        """
        Check if lessons are in same domain
        """
        domain1 = set(lesson1.belongsToDomain) if lesson1.belongsToDomain else set()
        domain2 = set(lesson2.belongsToDomain) if lesson2.belongsToDomain else set()
        
        if not domain1 or not domain2:
            return 0.0
        
        return 1.0 if domain1 & domain2 else 0.0
    
    def compute_similarity(self, lesson1, lesson2) -> float:
        """
        Compute overall semantic similarity between two lessons
        Returns a score between 0 and 1
        """
        score = 0.0
        
        # 1. Peace Axes similarity (0.25)
        axes1 = set(lesson1.hasAxis) if lesson1.hasAxis else set()
        axes2 = set(lesson2.hasAxis) if lesson2.hasAxis else set()
        axes_sim = self.jaccard_similarity(axes1, axes2)
        score += self.weights['axes'] * axes_sim
        
        # 2. Tools similarity (0.20)
        tools1 = set(lesson1.usesTool) if lesson1.usesTool else set()
        tools2 = set(lesson2.usesTool) if lesson2.usesTool else set()
        tools_sim = self.jaccard_similarity(tools1, tools2)
        score += self.weights['tools'] * tools_sim
        
        # 3. Virtues similarity (0.20)
        virtues1 = set(lesson1.developsVirtue) if lesson1.developsVirtue else set()
        virtues2 = set(lesson2.developsVirtue) if lesson2.developsVirtue else set()
        virtues_sim = self.jaccard_similarity(virtues1, virtues2)
        score += self.weights['virtues'] * virtues_sim
        
        # 4. Strategies similarity (0.15)
        strategies1 = set(lesson1.employsStrategy) if lesson1.employsStrategy else set()
        strategies2 = set(lesson2.employsStrategy) if lesson2.employsStrategy else set()
        strategies_sim = self.jaccard_similarity(strategies1, strategies2)
        score += self.weights['strategies'] * strategies_sim
        
        # 5. Age compatibility (0.10)
        age_sim = self.age_similarity(lesson1, lesson2)
        score += self.weights['age'] * age_sim
        
        # 6. Duration compatibility (0.05)
        dur_sim = self.duration_similarity(lesson1, lesson2)
        score += self.weights['duration'] * dur_sim
        
        # 7. Domain similarity (0.05)
        domain_sim = self.domain_similarity(lesson1, lesson2)
        score += self.weights['domain'] * domain_sim
        
        return score
    
    def find_similar(self, target_lesson, top_k=5, min_similarity=0.0) -> List[Tuple[object, float, Dict]]:
        """
        Find the k most similar lessons to the target lesson
        Returns list of (lesson, similarity_score, breakdown)
        """
        all_lessons = list(self.onto.Lesson.instances())
        similarities = []
        
        for lesson in all_lessons:
            if lesson == target_lesson:
                continue  # Skip the target lesson itself
            
            sim_score = self.compute_similarity(target_lesson, lesson)
            
            if sim_score >= min_similarity:
                # Compute breakdown for explainability
                breakdown = self.get_similarity_breakdown(target_lesson, lesson)
                similarities.append((lesson, sim_score, breakdown))
        
        # Sort by similarity score (descending)
        similarities.sort(key=lambda x: x[1], reverse=True)
        
        return similarities[:top_k]
    
    def get_similarity_breakdown(self, lesson1, lesson2) -> Dict:
        """
        Get detailed breakdown of similarity components
        """
        axes1 = set(lesson1.hasAxis) if lesson1.hasAxis else set()
        axes2 = set(lesson2.hasAxis) if lesson2.hasAxis else set()
        
        tools1 = set(lesson1.usesTool) if lesson1.usesTool else set()
        tools2 = set(lesson2.usesTool) if lesson2.usesTool else set()
        
        virtues1 = set(lesson1.developsVirtue) if lesson1.developsVirtue else set()
        virtues2 = set(lesson2.developsVirtue) if lesson2.developsVirtue else set()
        
        strategies1 = set(lesson1.employsStrategy) if lesson1.employsStrategy else set()
        strategies2 = set(lesson2.employsStrategy) if lesson2.employsStrategy else set()
        
        return {
            'axes': {
                'score': self.jaccard_similarity(axes1, axes2),
                'shared': [str(x) for x in (axes1 & axes2)],
                'weight': self.weights['axes']
            },
            'tools': {
                'score': self.jaccard_similarity(tools1, tools2),
                'shared': [str(x) for x in (tools1 & tools2)],
                'weight': self.weights['tools']
            },
            'virtues': {
                'score': self.jaccard_similarity(virtues1, virtues2),
                'shared': [str(x) for x in (virtues1 & virtues2)],
                'weight': self.weights['virtues']
            },
            'strategies': {
                'score': self.jaccard_similarity(strategies1, strategies2),
                'shared': [str(x) for x in (strategies1 & strategies2)],
                'weight': self.weights['strategies']
            },
            'age': {
                'score': self.age_similarity(lesson1, lesson2),
                'weight': self.weights['age']
            },
            'duration': {
                'score': self.duration_similarity(lesson1, lesson2),
                'weight': self.weights['duration']
            },
            'domain': {
                'score': self.domain_similarity(lesson1, lesson2),
                'weight': self.weights['domain']
            }
        }
    
    def search_by_criteria(self, axes=