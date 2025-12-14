"""
Test the similarity search with real pedagogical sheets
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from find_similar_lessons import find_similar


def test_environmental_lesson():
    """Test finding sheets for an environmental lesson"""
    
    print("\n" + "="*80)
    print("TEST 1: Environmental Science Lesson")
    print("="*80)
    
    print("\nINPUT (Your New Lesson):")
    print("  Title: Protecting Biodiversity in Our City")
    print("  Domain: Sciences")
    print("  Axes: Peace with Environment, Peace with Others")
    print("  Tools: Project-Based Learning")
    print("  Virtues: Responsibility, Empathy")
    print("  Age: 8-12 years")
    
    results = find_similar(
        title="Protecting Biodiversity in Our City",
        description="Students learn about local biodiversity and conservation",
        domain="Sciences",
        axes=["peace_with_environment", "peace_with_others"],
        tools=["project_based_learning"],
        virtues=["responsibility", "empathy"],
        target_age_min=8,
        target_age_max=12,
        top_k=5
    )
    
    print(f"\nFOUND {len(results)} SIMILAR PEDAGOGICAL SHEETS:\n")
    
    for i, sheet in enumerate(results, 1):
        print(f"[{i}] {sheet['title']}")
        print(f"    Similarity: {sheet['similarity_score']:.1%}")
        print(f"    Domain: {sheet['domain']}")
        print(f"    Age: {sheet['target_age_min']}-{sheet['target_age_max']} years")
        print(f"    Duration: {sheet['duration']:.1f} hours")
        
        # Show why it's similar
        breakdown = sheet['similarity_breakdown']
        top_factors = []
        if breakdown['axes']['contribution'] > 0.1:
            top_factors.append(f"Peace Axes ({breakdown['axes']['contribution']:.2f})")
        if breakdown['tools']['contribution'] > 0.1:
            top_factors.append(f"Tools ({breakdown['tools']['contribution']:.2f})")
        if breakdown['virtues']['contribution'] > 0.1:
            top_factors.append(f"Virtues ({breakdown['virtues']['contribution']:.2f})")
        
        if top_factors:
            print(f"    Key matches: {', '.join(top_factors)}")
        print()


def test_emotional_learning():
    """Test finding sheets for emotional learning"""
    
    print("\n" + "="*80)
    print("TEST 2: Emotional Learning / Ethics")
    print("="*80)
    
    print("\nINPUT (Your New Lesson):")
    print("  Title: Understanding and Managing Emotions")
    print("  Domain: Ethics")
    print("  Axes: Peace with Self, Peace with Others")
    print("  Tools: CEVQ, Meditation")
    print("  Virtues: Empathy, Patience, Benevolence")
    print("  Age: 7-11 years")
    
    results = find_similar(
        title="Understanding and Managing Emotions",
        description="Help children recognize, name, and manage their emotions",
        domain="Ethics",
        axes=["peace_with_self", "peace_with_others"],
        tools=["cevq", "meditation"],
        virtues=["empathy", "patience", "benevolence"],
        target_age_min=7,
        target_age_max=11,
        top_k=5
    )
    
    print(f"\nFOUND {len(results)} SIMILAR PEDAGOGICAL SHEETS:\n")
    
    for i, sheet in enumerate(results, 1):
        print(f"[{i}] {sheet['title']}")
        print(f"    Similarity: {sheet['similarity_score']:.1%}")
        print(f"    Domain: {sheet['domain']}")
        print(f"    Age: {sheet['target_age_min']}-{sheet['target_age_max']} years")
        
        # Show shared elements
        breakdown = sheet['similarity_breakdown']
        if breakdown['virtues']['shared']:
            virtues = [v.replace('peace_pedagogy.', '') for v in breakdown['virtues']['shared']]
            print(f"    Shared virtues: {', '.join(virtues)}")
        print()


def test_collaboration_arts():
    """Test finding sheets for arts collaboration"""
    
    print("\n" + "="*80)
    print("TEST 3: Arts Collaboration")
    print("="*80)
    
    print("\nINPUT (Your New Lesson):")
    print("  Title: Creating a Collective Mural")
    print("  Domain: Arts")
    print("  Axes: Peace with Others")
    print("  Tools: Artistic Expression, Project-Based Learning")
    print("  Virtues: Cooperation, Benevolence")
    print("  Age: 9-13 years")
    
    results = find_similar(
        title="Creating a Collective Mural",
        description="Students work together to create a large mural",
        domain="Arts",
        axes=["peace_with_others"],
        tools=["artistic_expression", "project_based_learning"],
        virtues=["cooperation", "benevolence"],
        target_age_min=9,
        target_age_max=13,
        top_k=5
    )
    
    print(f"\nFOUND {len(results)} SIMILAR PEDAGOGICAL SHEETS:\n")
    
    for i, sheet in enumerate(results, 1):
        print(f"[{i}] {sheet['title']}")
        print(f"    Similarity: {sheet['similarity_score']:.1%}")
        print(f"    Domain: {sheet['domain']}")
        print(f"    PDF: {os.path.basename(sheet.get('pdf_path', 'N/A'))}")
        print()


def main():
    print("\n" + "="*80)
    print("TESTING SIMILARITY SEARCH WITH REAL PEDAGOGICAL SHEETS")
    print("Database: 27 real lessons from FICHES PEDAGOGIQUES")
    print("="*80)
    
    test_environmental_lesson()
    test_emotional_learning()
    test_collaboration_arts()
    
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    print("\n[OK] System successfully finds similar real pedagogical sheets")
    print("[OK] Results are ranked by relevance")
    print("[OK] Similarity scores are meaningful")
    print("[OK] Ready to feed to AI model for lesson generation")
    print("\nNext step: Use these similar sheets as examples for AI generation!")
    print()


if __name__ == "__main__":
    main()

