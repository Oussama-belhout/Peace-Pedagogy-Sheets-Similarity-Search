"""
Query Engine for Peace Pedagogy Lessons
Takes raw metadata as input and finds similar existing pedagogical sheets
"""

from owlready2 import *
from typing import Dict, List, Tuple, Optional
import sys
import os

# Handle imports when running as script
if __name__ == "__main__":
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from similarity_engine import SimilarityEngine


class LessonQuery:
    """
    Represents a query for finding similar pedagogical sheets
    Takes raw metadata and creates a temporary lesson for comparison
    """
    
    def __init__(self, ontology):
        self.onto = ontology
        self.engine = SimilarityEngine(ontology)
        self._temp_namespace = None
    
    def query_similar_lessons(self, 
                             title: str,
                             description: str = "",
                             domain: str = None,
                             discipline: str = None,
                             axes: List[str] = None,
                             tools: List[str] = None,
                             virtues: List[str] = None,
                             strategies: List[str] = None,
                             target_age_min: int = None,
                             target_age_max: int = None,
                             duration: float = None,
                             group_size_min: int = None,
                             group_size_max: int = None,
                             top_k: int = 5,
                             min_similarity: float = 0.0) -> List[Dict]:
        """
        Query for similar pedagogical sheets based on raw metadata
        
        Args:
            title: Lesson title/name
            description: Lesson description
            domain: Academic domain (Sciences, Arts, Ethics, Languages)
            discipline: Specific discipline
            axes: List of peace axes (peace_with_self, peace_with_others, peace_with_environment)
            tools: List of pedagogical tools (cevq, meditation, project_based_learning, etc.)
            virtues: List of virtues to develop (gratitude, empathy, responsibility, etc.)
            strategies: List of teaching strategies (experiential_learning, etc.)
            target_age_min: Minimum target age
            target_age_max: Maximum target age
            duration: Lesson duration in hours
            group_size_min: Minimum group size
            group_size_max: Maximum group size
            top_k: Number of results to return
            min_similarity: Minimum similarity threshold
        
        Returns:
            List of dictionaries containing similar lessons and their metadata
        """
        
        # Create temporary lesson for comparison
        temp_lesson = self._create_temp_lesson(
            title=title,
            description=description,
            domain=domain,
            discipline=discipline,
            axes=axes,
            tools=tools,
            virtues=virtues,
            strategies=strategies,
            target_age_min=target_age_min,
            target_age_max=target_age_max,
            duration=duration,
            group_size_min=group_size_min,
            group_size_max=group_size_max
        )
        
        # Find similar lessons
        similar = self.engine.find_similar(temp_lesson, top_k=top_k, min_similarity=min_similarity)
        
        # Clean up temporary lesson
        self._cleanup_temp_lesson(temp_lesson)
        
        # Format results
        results = []
        for lesson, score, breakdown in similar:
            result = self._format_lesson_result(lesson, score, breakdown)
            results.append(result)
        
        return results
    
    def _create_temp_lesson(self, **kwargs) -> object:
        """Create a temporary lesson instance for querying"""
        
        with self.onto:
            # Create temporary lesson with unique ID
            temp_id = f"temp_query_lesson_{id(self)}"
            temp_lesson = self.onto.Lesson(temp_id)
            
            # Set data properties
            if kwargs.get('title'):
                temp_lesson.title = [kwargs['title']]
            if kwargs.get('description'):
                temp_lesson.description = [kwargs['description']]
            if kwargs.get('discipline'):
                temp_lesson.discipline = [kwargs['discipline']]
            if kwargs.get('duration'):
                temp_lesson.duration = [float(kwargs['duration'])]
            if kwargs.get('target_age_min'):
                temp_lesson.targetAgeMin = [int(kwargs['target_age_min'])]
            if kwargs.get('target_age_max'):
                temp_lesson.targetAgeMax = [int(kwargs['target_age_max'])]
            if kwargs.get('group_size_min'):
                temp_lesson.groupSizeMin = [int(kwargs['group_size_min'])]
            if kwargs.get('group_size_max'):
                temp_lesson.groupSizeMax = [int(kwargs['group_size_max'])]
            
            # Link to axes
            if kwargs.get('axes'):
                for axis_name in kwargs['axes']:
                    axis = self.onto.search_one(iri=f"*{axis_name}")
                    if axis:
                        temp_lesson.hasAxis.append(axis)
            
            # Link to tools
            if kwargs.get('tools'):
                for tool_name in kwargs['tools']:
                    tool = self.onto.search_one(iri=f"*{tool_name}")
                    if tool:
                        temp_lesson.usesTool.append(tool)
            
            # Link to virtues
            if kwargs.get('virtues'):
                for virtue_name in kwargs['virtues']:
                    virtue = self.onto.search_one(iri=f"*{virtue_name}")
                    if virtue:
                        temp_lesson.developsVirtue.append(virtue)
            
            # Link to strategies
            if kwargs.get('strategies'):
                for strategy_name in kwargs['strategies']:
                    strategy = self.onto.search_one(iri=f"*{strategy_name}")
                    if strategy:
                        temp_lesson.employsStrategy.append(strategy)
            
            # Link to domain
            if kwargs.get('domain'):
                domain = self.onto.search_one(iri=f"*{kwargs['domain'].lower()}")
                if domain:
                    temp_lesson.belongsToDomain = [domain]
            
            return temp_lesson
    
    def _cleanup_temp_lesson(self, temp_lesson):
        """Remove temporary lesson from ontology"""
        destroy_entity(temp_lesson)
    
    def _format_lesson_result(self, lesson, score: float, breakdown: Dict) -> Dict:
        """Format a lesson result into a structured dictionary"""
        
        return {
            'title': lesson.title[0] if lesson.title else "Untitled",
            'description': lesson.description[0] if lesson.description else "",
            'domain': lesson.belongsToDomain[0].name.replace('peace_pedagogy.', '') if lesson.belongsToDomain else None,
            'discipline': lesson.discipline[0] if lesson.discipline else None,
            'axes': [a.name.replace('peace_pedagogy.', '') for a in lesson.hasAxis] if lesson.hasAxis else [],
            'tools': [t.name.replace('peace_pedagogy.', '') for t in lesson.usesTool] if lesson.usesTool else [],
            'virtues': [v.name.replace('peace_pedagogy.', '') for v in lesson.developsVirtue] if lesson.developsVirtue else [],
            'strategies': [s.name.replace('peace_pedagogy.', '') for s in lesson.employsStrategy] if lesson.employsStrategy else [],
            'target_age_min': lesson.targetAgeMin[0] if lesson.targetAgeMin else None,
            'target_age_max': lesson.targetAgeMax[0] if lesson.targetAgeMax else None,
            'duration': lesson.duration[0] if lesson.duration else None,
            'group_size_min': lesson.groupSizeMin[0] if lesson.groupSizeMin else None,
            'group_size_max': lesson.groupSizeMax[0] if lesson.groupSizeMax else None,
            'similarity_score': score,
            'similarity_breakdown': {
                'axes': {
                    'score': breakdown['axes']['score'],
                    'contribution': breakdown['axes']['score'] * breakdown['axes']['weight'],
                    'shared': breakdown['axes']['shared']
                },
                'tools': {
                    'score': breakdown['tools']['score'],
                    'contribution': breakdown['tools']['score'] * breakdown['tools']['weight'],
                    'shared': breakdown['tools']['shared']
                },
                'virtues': {
                    'score': breakdown['virtues']['score'],
                    'contribution': breakdown['virtues']['score'] * breakdown['virtues']['weight'],
                    'shared': breakdown['virtues']['shared']
                },
                'strategies': {
                    'score': breakdown['strategies']['score'],
                    'contribution': breakdown['strategies']['score'] * breakdown['strategies']['weight'],
                    'shared': breakdown['strategies']['shared']
                },
                'age': {
                    'score': breakdown['age']['score'],
                    'contribution': breakdown['age']['score'] * breakdown['age']['weight']
                },
                'duration': {
                    'score': breakdown['duration']['score'],
                    'contribution': breakdown['duration']['score'] * breakdown['duration']['weight']
                },
                'domain': {
                    'score': breakdown['domain']['score'],
                    'contribution': breakdown['domain']['score'] * breakdown['domain']['weight']
                }
            }
        }


def search_similar_lessons(
    title: str,
    description: str = "",
    domain: str = None,
    discipline: str = None,
    axes: List[str] = None,
    tools: List[str] = None,
    virtues: List[str] = None,
    strategies: List[str] = None,
    target_age_min: int = None,
    target_age_max: int = None,
    duration: float = None,
    group_size_min: int = None,
    group_size_max: int = None,
    top_k: int = 5,
    ontology_path: str = "ontology/peace_pedagogy.owl"
) -> List[Dict]:
    """
    Convenience function to search for similar lessons
    
    Example:
        results = search_similar_lessons(
            title="My Environmental Lesson",
            description="Teaching kids about nature",
            domain="Sciences",
            axes=["peace_with_environment"],
            tools=["project_based_learning"],
            virtues=["responsibility", "gratitude"],
            target_age_min=8,
            target_age_max=12,
            duration=2.5,
            top_k=3
        )
    """
    
    # Load ontology
    onto = get_ontology(ontology_path).load()
    
    # Create query engine
    query_engine = LessonQuery(onto)
    
    # Search for similar lessons
    results = query_engine.query_similar_lessons(
        title=title,
        description=description,
        domain=domain,
        discipline=discipline,
        axes=axes,
        tools=tools,
        virtues=virtues,
        strategies=strategies,
        target_age_min=target_age_min,
        target_age_max=target_age_max,
        duration=duration,
        group_size_min=group_size_min,
        group_size_max=group_size_max,
        top_k=top_k
    )
    
    return results


if __name__ == "__main__":
    """
    Example usage: Query with raw metadata to find similar pedagogical sheets
    """
    
    print("="*80)
    print("PEACE PEDAGOGY - QUERY ENGINE DEMO")
    print("="*80)
    
    print("\n>> INPUT: New lesson metadata")
    print("-" * 80)
    
    # Example query - describing a NEW lesson we want to create
    query_metadata = {
        'title': "Exploring Our Local Ecosystem",
        'description': "Students will explore local nature and learn about biodiversity",
        'domain': "Sciences",
        'discipline': "ecology",
        'axes': ["peace_with_environment", "peace_with_others"],
        'tools': ["project_based_learning"],
        'virtues': ["responsibility", "gratitude"],
        'target_age_min': 9,
        'target_age_max': 13,
        'duration': 3.0,
        'group_size_min': 15,
        'group_size_max': 25
    }
    
    print(f"Title: {query_metadata['title']}")
    print(f"Domain: {query_metadata['domain']}")
    print(f"Axes: {', '.join(query_metadata['axes'])}")
    print(f"Tools: {', '.join(query_metadata['tools'])}")
    print(f"Virtues: {', '.join(query_metadata['virtues'])}")
    print(f"Age: {query_metadata['target_age_min']}-{query_metadata['target_age_max']}")
    print(f"Duration: {query_metadata['duration']} hours")
    
    print("\n>> OUTPUT: Most similar existing pedagogical sheets")
    print("-" * 80)
    
    # Search for similar lessons
    results = search_similar_lessons(**query_metadata, top_k=3)
    
    if not results:
        print("No similar lessons found.")
    else:
        for i, result in enumerate(results, 1):
            print(f"\n{i}. {result['title']}")
            print(f"   Similarity Score: {result['similarity_score']:.3f}")
            print(f"   Domain: {result['domain']}")
            print(f"   Age: {result['target_age_min']}-{result['target_age_max']}")
            print(f"   Duration: {result['duration']} hours")
            
            # Show why it's similar
            breakdown = result['similarity_breakdown']
            print(f"\n   Why similar:")
            print(f"   - Peace Axes: {breakdown['axes']['score']:.2f} (contribution: {breakdown['axes']['contribution']:.3f})")
            if breakdown['axes']['shared']:
                shared = [s.replace('peace_pedagogy.', '').replace('_', ' ') for s in breakdown['axes']['shared']]
                print(f"     Shared: {', '.join(shared)}")
            
            print(f"   - Tools: {breakdown['tools']['score']:.2f} (contribution: {breakdown['tools']['contribution']:.3f})")
            if breakdown['tools']['shared']:
                shared = [s.replace('peace_pedagogy.', '').replace('_', ' ') for s in breakdown['tools']['shared']]
                print(f"     Shared: {', '.join(shared)}")
            
            print(f"   - Virtues: {breakdown['virtues']['score']:.2f} (contribution: {breakdown['virtues']['contribution']:.3f})")
            if breakdown['virtues']['shared']:
                shared = [s.replace('peace_pedagogy.', '').replace('_', ' ') for s in breakdown['virtues']['shared']]
                print(f"     Shared: {', '.join(shared)}")
    
    print("\n" + "="*80)
    print("These similar sheets can now be used as examples for generating a new sheet!")
    print("="*80)

