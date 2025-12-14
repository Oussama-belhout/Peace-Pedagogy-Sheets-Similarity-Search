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
    onto.save(file=ontology_path, format="rdfxml")
    
    return onto, lessons


if __name__ == "__main__":
    import sys
    
    ontology_path = "ontology/peace_pedagogy.owl"
    
    # Check for command line argument
    if len(sys.argv) > 2 and sys.argv[1] == '--data-file':
        data_path = sys.argv[2]
    else:
        # Default to pedagogical sheets if available, else sample data
        import os
        if os.path.exists("data/pedagogical_sheets.json"):
            data_path = "data/pedagogical_sheets.json"
        else:
            data_path = "data/sample_data.json"
    
    print(f"Loading data from: {data_path}")
    onto, lessons = load_lessons(ontology_path, data_path)
    
    print("\nCreated lessons:")
    for lesson in lessons:
        print(f"  - {lesson.title[0]}")

