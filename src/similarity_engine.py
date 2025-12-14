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
    
    def search_by_criteria(self, axes=None, tools=None, virtues=None, 
                          strategies=None, domain=None, 
                          age_min=None, age_max=None,
                          min_similarity=0.0) -> List[object]:
        """
        Search for lessons matching specific criteria
        """
        matching_lessons = []
        all_lessons = list(self.onto.Lesson.instances())
        
        for lesson in all_lessons:
            match = True
            
            # Check axes
            if axes:
                lesson_axes = set([str(a) for a in lesson.hasAxis]) if lesson.hasAxis else set()
                if not any(axis in lesson_axes for axis in axes):
                    match = False
            
            # Check tools
            if tools:
                lesson_tools = set([str(t) for t in lesson.usesTool]) if lesson.usesTool else set()
                if not any(tool in lesson_tools for tool in tools):
                    match = False
            
            # Check virtues
            if virtues:
                lesson_virtues = set([str(v) for v in lesson.developsVirtue]) if lesson.developsVirtue else set()
                if not any(virtue in lesson_virtues for virtue in virtues):
                    match = False
            
            # Check age range
            if age_min is not None and age_max is not None:
                lesson_age_min = lesson.targetAgeMin[0] if lesson.targetAgeMin else 0
                lesson_age_max = lesson.targetAgeMax[0] if lesson.targetAgeMax else 0
                
                # Check if there's overlap
                if lesson_age_max < age_min or lesson_age_min > age_max:
                    match = False
            
            if match:
                matching_lessons.append(lesson)
        
        return matching_lessons


def main():
    """
    Example usage of the similarity engine
    """
    # Load ontology
    onto = get_ontology("ontology/peace_pedagogy.owl").load()
    
    # Create engine
    engine = SimilarityEngine(onto)
    
    # Get all lessons
    lessons = list(onto.Lesson.instances())
    
    if not lessons:
        print("No lessons found in ontology. Please run data_loader.py first.")
        return
    
    print(f"\nFound {len(lessons)} lessons in ontology\n")
    
    # Find similar lessons for the first lesson
    target_lesson = lessons[0]
    print(f"Finding lessons similar to: {target_lesson.title[0]}")
    print("=" * 80)
    
    similar = engine.find_similar(target_lesson, top_k=3)
    
    for i, (lesson, score, breakdown) in enumerate(similar, 1):
        print(f"\n{i}. {lesson.title[0]}")
        print(f"   Overall Similarity: {score:.3f}")
        print(f"   - Peace Axes: {breakdown['axes']['score']:.2f} (shared: {breakdown['axes']['shared']})")
        print(f"   - Tools: {breakdown['tools']['score']:.2f} (shared: {breakdown['tools']['shared']})")
        print(f"   - Virtues: {breakdown['virtues']['score']:.2f} (shared: {breakdown['virtues']['shared']})")
        print(f"   - Strategies: {breakdown['strategies']['score']:.2f}")


if __name__ == "__main__":
    main()



