"""
LIVE DEMONSTRATION: Peace Pedagogy Similarity Search
Shows real-world usage with 27 pedagogical sheets
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from find_similar_lessons import find_similar
import json


def demo_scenario_1():

    print("\n" + "="*80)
    print("SCENARIO 1: Water Conservation Lesson")
    print("="*80)
    
    print("\nTeacher Input:")
    print("  'I want to create a lesson about water conservation for ages 9-12'")
    print("  'Focus on environmental responsibility and collaboration'")
    print("  'Use project-based learning'")
    
    print("\nSearching database of 27 pedagogical sheets...")
    
    results = find_similar(
        title="Water Conservation and Responsibility",
        description="Teaching children about water conservation",
        domain="Sciences",
        axes=["peace_with_environment", "peace_with_others"],
        tools=["project_based_learning"],
        virtues=["responsibility", "cooperation"],
        target_age_min=9,
        target_age_max=12,
        top_k=3
    )
    
    print(f"\nFOUND {len(results)} MOST RELEVANT EXISTING SHEETS:\n")
    
    for i, sheet in enumerate(results, 1):
        print(f"{i}. {sheet['title']}")
        print(f"   Similarity: {sheet['similarity_score']:.1%}")
        print(f"   Ages: {sheet['target_age_min']}-{sheet['target_age_max']}")
        print(f"   Duration: {sheet['duration']:.1f}h")
        
        # Show the actual PDF file
        pdf_path = sheet.get('pdf_path', 'N/A')
        if pdf_path != 'N/A':
            pdf_name = os.path.basename(pdf_path)
            print(f"   PDF: {pdf_name}")
        
        # Show shared elements
        breakdown = sheet['similarity_breakdown']
        shared_items = []
        if breakdown['axes']['shared']:
            shared_items.append(f"Axes: {len(breakdown['axes']['shared'])}")
        if breakdown['tools']['shared']:
            shared_items.append(f"Tools: {len(breakdown['tools']['shared'])}")
        if breakdown['virtues']['shared']:
            shared_items.append(f"Virtues: {len(breakdown['virtues']['shared'])}")
        
        if shared_items:
            print(f"   Shared: {', '.join(shared_items)}")
        print()
    
    print("Next Step: Review these sheets and use as inspiration for your new lesson!")
    return results


def demo_scenario_2():
    """
    SCENARIO 2: School counselor needs emotional learning materials
    """
    print("\n" + "="*80)
    print("SCENARIO 2: Emotional Learning Materials")
    print("="*80)
    
    print("\nCounselor Input:")
    print("  'Need materials for helping 7-10 year olds understand emotions'")
    print("  'Focus on empathy and self-awareness'")
    print("  'Prefer CEVQ approach'")
    
    print("\nSearching database...")
    
    results = find_similar(
        title="Understanding and Expressing Emotions",
        domain="Ethics",
        axes=["peace_with_self", "peace_with_others"],
        tools=["cevq", "meditation"],
        virtues=["empathy", "patience"],
        target_age_min=7,
        target_age_max=10,
        top_k=3
    )
    
    print(f"\nFOUND {len(results)} RELEVANT SHEETS:\n")
    
    for i, sheet in enumerate(results, 1):
        print(f"{i}. {sheet['title']} - {sheet['similarity_score']:.1%} match")
        
        # Show specific details counselor cares about
        if sheet.get('virtues'):
            virtues = [v.replace('peace_pedagogy.', '') for v in sheet['virtues']]
            print(f"   Develops: {', '.join(virtues[:3])}")
        
        if sheet.get('tools'):
            tools = [t.replace('peace_pedagogy.', '') for t in sheet['tools']]
            print(f"   Methods: {', '.join(tools[:2])}")
        
        print(f"   Age fit: {sheet['target_age_min']}-{sheet['target_age_max']} years")
        print()
    
    return results


def demo_scenario_3():
    """
    SCENARIO 3: Art teacher wants collaboration project
    """
    print("\n" + "="*80)
    print("SCENARIO 3: Collaborative Arts Project")
    print("="*80)
    
    print("\nArt Teacher Input:")
    print("  'Want students to work together on creative project'")
    print("  'Ages 10-14, focus on teamwork and expression'")
    print("  'Any artistic medium'")
    
    print("\nSearching database...")
    
    results = find_similar(
        title="Collaborative Creative Expression",
        domain="Arts",
        axes=["peace_with_others"],
        tools=["artistic_expression", "project_based_learning"],
        virtues=["cooperation", "patience", "benevolence"],
        target_age_min=10,
        target_age_max=14,
        top_k=3
    )
    
    print(f"\nFOUND {len(results)} RELEVANT SHEETS:\n")
    
    for i, sheet in enumerate(results, 1):
        print(f"{i}. {sheet['title']}")
        print(f"   Match: {sheet['similarity_score']:.1%}")
        print(f"   Discipline: {sheet.get('discipline', 'N/A')}")
        print(f"   Group size: {sheet['group_size_min']}-{sheet['group_size_max']}")
        print()
    
    return results


def demo_api_usage():
    """
    SCENARIO 4: Show how to use programmatically
    """
    print("\n" + "="*80)
    print("SCENARIO 4: Programmatic Usage (For Developers)")
    print("="*80)
    
    print("\nCode Example:")
    print("-" * 80)
    print("""
from find_similar_lessons import find_similar

# Query for similar sheets
results = find_similar(
    title="My New Lesson",
    domain="Sciences",
    axes=["peace_with_environment"],
    tools=["project_based_learning"],
    virtues=["responsibility"],
    target_age_min=8,
    target_age_max=12,
    top_k=5
)

# Process results
for sheet in results:
    print(f"Title: {sheet['title']}")
    print(f"Similarity: {sheet['similarity_score']:.1%}")
    print(f"PDF: {sheet['pdf_path']}")
    
    # Get full similarity breakdown
    breakdown = sheet['similarity_breakdown']
    print(f"Peace Axes match: {breakdown['axes']['score']:.1%}")
    print(f"Tools match: {breakdown['tools']['score']:.1%}")
    
    # Use for AI model training
    # ai_model.generate(user_input, examples=[sheet])
""")
    print("-" * 80)
    
    print("\nRunning actual query...")
    
    results = find_similar(
        title="Example Environmental Lesson",
        domain="Sciences",
        axes=["peace_with_environment"],
        top_k=2
    )
    
    print(f"\nGot {len(results)} results")
    print("\nResult structure (JSON format):")
    if results:
        # Show first result structure
        result_sample = {
            'title': results[0]['title'],
            'similarity_score': results[0]['similarity_score'],
            'domain': results[0]['domain'],
            'axes': results[0]['axes'][:2] if results[0]['axes'] else [],
            'pdf_path': os.path.basename(results[0].get('pdf_path', 'N/A')),
            'similarity_breakdown': {
                'axes': results[0]['similarity_breakdown']['axes'],
                'tools': results[0]['similarity_breakdown']['tools'],
            }
        }
        print(json.dumps(result_sample, indent=2, ensure_ascii=False))


def main():
    """
    Run complete live demonstration
    """
    print("\n")
    print("#" * 80)
    print("#" + " " * 78 + "#")
    print("#" + "PEACE PEDAGOGY SIMILARITY SEARCH - LIVE DEMONSTRATION".center(78) + "#")
    print("#" + "27 Real Pedagogical Sheets from FICHES PEDAGOGIQUES".center(78) + "#")
    print("#" + " " * 78 + "#")
    print("#" * 80)
    
    print("\nThis demonstration shows real-world usage scenarios")
    print("with the 27 pedagogical sheets from your PDF collection.")
    
    # Run scenarios
    demo_scenario_1()
    input("\n[Press Enter to continue to Scenario 2...]")
    
    demo_scenario_2()
    input("\n[Press Enter to continue to Scenario 3...]")
    
    demo_scenario_3()
    input("\n[Press Enter to see API usage example...]")
    
    demo_api_usage()
    
    # Final summary
    print("\n" + "="*80)
    print("DEMONSTRATION COMPLETE")
    print("="*80)
    
    print("\nKey Takeaways:")
    print("  [1] Input: Teacher describes their new lesson idea")
    print("  [2] Process: System searches 27 real pedagogical sheets")
    print("  [3] Output: Returns most similar existing sheets")
    print("  [4] Next: Use similar sheets as examples for AI generation")
    
    print("\nDatabase Statistics:")
    print("  - Total sheets: 27")
    print("  - Sciences: 11 sheets")
    print("  - Ethics: 11 sheets")
    print("  - Arts: 3 sheets")
    print("  - Languages: 2 sheets")
    
    print("\nReady for AI Integration:")
    print("  -> Feed similar sheets to AI model")
    print("  -> Generate complete new pedagogical sheet")
    print("  -> Based on proven templates from real teachers")
    
    print("\n" + "="*80)
    print("Thank you for using Peace Pedagogy Similarity Search!")
    print("="*80)
    print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[Demo interrupted]")
    except Exception as e:
        print(f"\n[Error: {e}]")
        import traceback
        traceback.print_exc()

