"""
Simple API for Finding Similar Pedagogical Sheets

INPUT: Lesson metadata (name, subject, age, etc.)
OUTPUT: Most similar existing pedagogical sheets

Usage:
    python find_similar_lessons.py
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from query_engine import search_similar_lessons
import json


def find_similar(
    title: str,
    description: str = "",
    domain: str = None,
    axes: list = None,
    tools: list = None,
    virtues: list = None,
    target_age_min: int = None,
    target_age_max: int = None,
    duration: float = None,
    top_k: int = 5
):
    """
    Find similar pedagogical sheets based on your lesson metadata
    
    Args:
        title: Your lesson title/name
        description: Brief description of your lesson
        domain: Academic domain (Sciences, Arts, Ethics, Languages)
        axes: Peace axes - choose from:
              - "peace_with_self"
              - "peace_with_others"  
              - "peace_with_environment"
        tools: Pedagogical tools - choose from:
               - "cevq"
               - "meditation"
               - "project_based_learning"
               - "artistic_expression"
               - "solution_oriented_learning"
        virtues: Virtues to develop - choose from:
                 - "gratitude"
                 - "empathy"
                 - "responsibility"
                 - "compassion"
                 - "patience"
                 - "benevolence"
        target_age_min: Minimum age (e.g., 6)
        target_age_max: Maximum age (e.g., 14)
        duration: Lesson duration in hours (e.g., 2.5)
        top_k: Number of similar lessons to return
    
    Returns:
        List of similar pedagogical sheets with similarity scores
    """
    
    results = search_similar_lessons(
        title=title,
        description=description,
        domain=domain,
        axes=axes,
        tools=tools,
        virtues=virtues,
        target_age_min=target_age_min,
        target_age_max=target_age_max,
        duration=duration,
        top_k=top_k
    )
    
    return results


def print_results(results):
    """Pretty print the results"""
    
    if not results:
        print("\nNo similar lessons found.")
        return
    
    print("\n" + "="*80)
    print(f"FOUND {len(results)} SIMILAR PEDAGOGICAL SHEETS")
    print("="*80)
    
    for i, result in enumerate(results, 1):
        print(f"\n[{i}] {result['title']}")
        print(f"    Similarity: {result['similarity_score']:.1%}")
        print(f"    Domain: {result['domain'] or 'N/A'}")
        print(f"    Age: {result['target_age_min']}-{result['target_age_max']} years")
        print(f"    Duration: {result['duration']} hours")
        
        if result['axes']:
            axes_clean = [a.replace('peace_pedagogy.', '').replace('_', ' ').title() for a in result['axes']]
            print(f"    Peace Axes: {', '.join(axes_clean)}")
        
        if result['tools']:
            tools_clean = [t.replace('peace_pedagogy.', '').replace('_', ' ').title() for t in result['tools']]
            print(f"    Tools: {', '.join(tools_clean)}")
        
        if result['virtues']:
            virtues_clean = [v.replace('peace_pedagogy.', '').replace('_', ' ').title() for v in result['virtues']]
            print(f"    Virtues: {', '.join(virtues_clean)}")
        
        # Show top contributing factors
        breakdown = result['similarity_breakdown']
        contributions = [
            ('Peace Axes', breakdown['axes']['contribution']),
            ('Tools', breakdown['tools']['contribution']),
            ('Virtues', breakdown['virtues']['contribution']),
            ('Strategies', breakdown['strategies']['contribution']),
            ('Age Match', breakdown['age']['contribution']),
            ('Duration Match', breakdown['duration']['contribution']),
        ]
        contributions.sort(key=lambda x: x[1], reverse=True)
        
        print(f"    Top matches: ", end="")
        top_3 = [f"{name} ({score:.2f})" for name, score in contributions[:3] if score > 0]
        print(", ".join(top_3))


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    
    print("\n" + "="*80)
    print("PEACE PEDAGOGY - FIND SIMILAR LESSONS")
    print("="*80)
    
    # ========================================================================
    # EXAMPLE 1: Environmental Science Lesson
    # ========================================================================
    
    print("\n" + "-"*80)
    print("EXAMPLE 1: Finding sheets for an Environmental Science lesson")
    print("-"*80)
    
    print("\nINPUT (Your New Lesson):")
    print("  Title: Protecting Local Wildlife")
    print("  Domain: Sciences")
    print("  Axes: Peace with Environment")
    print("  Tools: Project-Based Learning")
    print("  Virtues: Responsibility, Compassion")
    print("  Age: 8-12 years")
    print("  Duration: 2 hours")
    
    results = find_similar(
        title="Protecting Local Wildlife",
        description="Students learn about local animal species and conservation",
        domain="Sciences",
        axes=["peace_with_environment"],
        tools=["project_based_learning"],
        virtues=["responsibility", "compassion"],
        target_age_min=8,
        target_age_max=12,
        duration=2.0,
        top_k=3
    )
    
    print_results(results)
    
    # ========================================================================
    # EXAMPLE 2: Ethics/Emotional Learning
    # ========================================================================
    
    print("\n\n" + "-"*80)
    print("EXAMPLE 2: Finding sheets for an Ethics/Emotional Learning lesson")
    print("-"*80)
    
    print("\nINPUT (Your New Lesson):")
    print("  Title: Understanding Our Emotions")
    print("  Domain: Ethics")
    print("  Axes: Peace with Self, Peace with Others")
    print("  Tools: CEVQ, Meditation")
    print("  Virtues: Empathy, Patience")
    print("  Age: 7-10 years")
    print("  Duration: 1.5 hours")
    
    results = find_similar(
        title="Understanding Our Emotions",
        description="Helping children recognize and express emotions",
        domain="Ethics",
        axes=["peace_with_self", "peace_with_others"],
        tools=["cevq", "meditation"],
        virtues=["empathy", "patience"],
        target_age_min=7,
        target_age_max=10,
        duration=1.5,
        top_k=3
    )
    
    print_results(results)
    
    # ========================================================================
    # EXAMPLE 3: Arts Collaboration
    # ========================================================================
    
    print("\n\n" + "-"*80)
    print("EXAMPLE 3: Finding sheets for an Arts Collaboration lesson")
    print("-"*80)
    
    print("\nINPUT (Your New Lesson):")
    print("  Title: Creating Together")
    print("  Domain: Arts")
    print("  Axes: Peace with Others")
    print("  Tools: Artistic Expression, Project-Based Learning")
    print("  Virtues: Benevolence, Patience")
    print("  Age: 9-13 years")
    print("  Duration: 2.5 hours")
    
    results = find_similar(
        title="Creating Together",
        description="Collaborative art project for building team spirit",
        domain="Arts",
        axes=["peace_with_others"],
        tools=["artistic_expression", "project_based_learning"],
        virtues=["benevolence", "patience"],
        target_age_min=9,
        target_age_max=13,
        duration=2.5,
        top_k=3
    )
    
    print_results(results)
    
    print("\n" + "="*80)
    print("NEXT STEP: Use these similar sheets as examples for your AI model")
    print("="*80)
    print("\nTo use in your code:")
    print("  from find_similar_lessons import find_similar")
    print("  results = find_similar(title='...', domain='...', axes=[...], ...)")
    print("  # Feed results to your AI model to generate complete pedagogical sheet")
    print()



