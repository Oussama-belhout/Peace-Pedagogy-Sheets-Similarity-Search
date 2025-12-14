"""
Peace Pedagogy Similarity Search - Interactive Demo
Run this to see the system in action!
"""

from owlready2 import get_ontology
from src.similarity_engine import SimilarityEngine
import sys

def print_header(text):
    """Print a nice header"""
    print("\n" + "=" * 80)
    print(text.center(80))
    print("=" * 80)

def print_lesson_details(lesson):
    """Print detailed information about a lesson"""
    print(f"\n[LESSON] {lesson.title[0]}")
    print(f"   Description: {lesson.description[0] if lesson.description else 'N/A'}")
    print(f"   Domain: {lesson.belongsToDomain[0].name if lesson.belongsToDomain else 'N/A'}")
    print(f"   Discipline: {lesson.discipline[0] if lesson.discipline else 'N/A'}")
    
    if lesson.hasAxis:
        axes_names = [a.name.replace('peace_pedagogy.', '').replace('_', ' ').title() for a in lesson.hasAxis]
        print(f"   Peace Axes: {', '.join(axes_names)}")
    
    if lesson.usesTool:
        tools_names = [t.name.replace('peace_pedagogy.', '').replace('_', ' ').title() for t in lesson.usesTool]
        print(f"   Tools: {', '.join(tools_names)}")
    
    if lesson.developsVirtue:
        virtues_names = [v.name.replace('peace_pedagogy.', '').replace('_', ' ').title() for v in lesson.developsVirtue]
        print(f"   Virtues: {', '.join(virtues_names)}")
    
    print(f"   Age Range: {lesson.targetAgeMin[0] if lesson.targetAgeMin else 'N/A'} - {lesson.targetAgeMax[0] if lesson.targetAgeMax else 'N/A'} years")
    print(f"   Duration: {lesson.duration[0] if lesson.duration else 'N/A'} hours")
    print(f"   Group Size: {lesson.groupSizeMin[0] if lesson.groupSizeMin else 'N/A'} - {lesson.groupSizeMax[0] if lesson.groupSizeMax else 'N/A'} students")

def print_similarity_result(rank, lesson, score, breakdown):
    """Print similarity search results"""
    print(f"\n{rank}. {lesson.title[0]}")
    print(f"   Overall Similarity: {score:.3f}")
    print(f"   +- Peace Axes: {breakdown['axes']['score']:.2f} x {breakdown['axes']['weight']:.2f} = {breakdown['axes']['score'] * breakdown['axes']['weight']:.3f}")
    if breakdown['axes']['shared']:
        shared = [s.replace('peace_pedagogy.', '').replace('_', ' ') for s in breakdown['axes']['shared']]
        print(f"   |  Shared: {', '.join(shared)}")
    print(f"   +- Tools: {breakdown['tools']['score']:.2f} x {breakdown['tools']['weight']:.2f} = {breakdown['tools']['score'] * breakdown['tools']['weight']:.3f}")
    if breakdown['tools']['shared']:
        shared = [s.replace('peace_pedagogy.', '').replace('_', ' ') for s in breakdown['tools']['shared']]
        print(f"   |  Shared: {', '.join(shared)}")
    print(f"   +- Virtues: {breakdown['virtues']['score']:.2f} x {breakdown['virtues']['weight']:.2f} = {breakdown['virtues']['score'] * breakdown['virtues']['weight']:.3f}")
    if breakdown['virtues']['shared']:
        shared = [s.replace('peace_pedagogy.', '').replace('_', ' ') for s in breakdown['virtues']['shared']]
        print(f"   |  Shared: {', '.join(shared)}")
    print(f"   +- Strategies: {breakdown['strategies']['score']:.2f} x {breakdown['strategies']['weight']:.2f} = {breakdown['strategies']['score'] * breakdown['strategies']['weight']:.3f}")
    print(f"   +- Age Range: {breakdown['age']['score']:.2f} x {breakdown['age']['weight']:.2f} = {breakdown['age']['score'] * breakdown['age']['weight']:.3f}")
    print(f"   +- Duration: {breakdown['duration']['score']:.2f} x {breakdown['duration']['weight']:.2f} = {breakdown['duration']['score'] * breakdown['duration']['weight']:.3f}")
    print(f"   +- Domain: {breakdown['domain']['score']:.2f} x {breakdown['domain']['weight']:.2f} = {breakdown['domain']['score'] * breakdown['domain']['weight']:.3f}")

def demo_all_lessons(onto):
    """Show all lessons in the ontology"""
    print_header("ALL LESSONS IN THE ONTOLOGY")
    
    lessons = list(onto.Lesson.instances())
    print(f"\nTotal lessons loaded: {len(lessons)}")
    
    for i, lesson in enumerate(lessons, 1):
        print(f"\n{i}. {lesson.title[0]}")
        print(f"   {lesson.description[0] if lesson.description else 'No description'}")

def demo_similarity_search(onto, engine):
    """Demonstrate similarity search"""
    print_header("SIMILARITY SEARCH DEMO")
    
    lessons = list(onto.Lesson.instances())
    
    # Show the target lesson
    target_lesson = lessons[0]
    print("\n>> TARGET LESSON:")
    print_lesson_details(target_lesson)
    
    # Find similar lessons
    print("\n\n>> FINDING MOST SIMILAR LESSONS...")
    similar = engine.find_similar(target_lesson, top_k=3, min_similarity=0.0)
    
    if not similar:
        print("No similar lessons found.")
        return
    
    print("\n>> TOP 3 MOST SIMILAR LESSONS:")
    for i, (lesson, score, breakdown) in enumerate(similar, 1):
        print_similarity_result(i, lesson, score, breakdown)

def demo_criteria_search(onto, engine):
    """Demonstrate search by criteria"""
    print_header("SEARCH BY CRITERIA DEMO")
    
    print("\n>> Searching for lessons that:")
    print("   - Focus on Peace with Environment")
    print("   - Suitable for ages 8-12")
    
    matching = engine.search_by_criteria(
        axes=["peace_with_environment"],
        age_min=8,
        age_max=12
    )
    
    print(f"\n>> Found {len(matching)} matching lessons:")
    for lesson in matching:
        print(f"\n   * {lesson.title[0]}")
        print(f"     Ages: {lesson.targetAgeMin[0]}-{lesson.targetAgeMax[0]}")
        if lesson.hasAxis:
            axes = [a.name.replace('peace_pedagogy.', '').replace('_', ' ') for a in lesson.hasAxis]
            print(f"     Axes: {', '.join(axes)}")

def demo_custom_weights(onto, engine):
    """Demonstrate custom weight configuration"""
    print_header("CUSTOM WEIGHTS DEMO")
    
    lessons = list(onto.Lesson.instances())
    target_lesson = lessons[0]
    
    # Original weights
    print("\n[ORIGINAL WEIGHTS]:")
    for dim, weight in engine.weights.items():
        print(f"   {dim.capitalize()}: {weight:.2f}")
    
    similar_original = engine.find_similar(target_lesson, top_k=1, min_similarity=0.0)
    
    if similar_original:
        lesson, score, _ = similar_original[0]
        print(f"\n   Top match: {lesson.title[0]} (score: {score:.3f})")
    
    # Emphasize virtues
    print("\n\n[EMPHASIZING VIRTUES (0.40)]:")
    engine.weights = {
        'axes': 0.20,
        'tools': 0.15,
        'virtues': 0.40,  # Increased!
        'strategies': 0.10,
        'age': 0.08,
        'duration': 0.04,
        'domain': 0.03
    }
    
    for dim, weight in engine.weights.items():
        print(f"   {dim.capitalize()}: {weight:.2f}")
    
    similar_virtues = engine.find_similar(target_lesson, top_k=1, min_similarity=0.0)
    
    if similar_virtues:
        lesson, score, _ = similar_virtues[0]
        print(f"\n   Top match: {lesson.title[0]} (score: {score:.3f})")
    
    # Reset weights
    engine.weights = {
        'axes': 0.25,
        'tools': 0.20,
        'virtues': 0.20,
        'strategies': 0.15,
        'age': 0.10,
        'duration': 0.05,
        'domain': 0.05
    }

def main():
    """Run the interactive demo"""
    print("\n")
    print("+" + "=" * 78 + "+")
    print("|" + " " * 78 + "|")
    print("|" + "PEACE PEDAGOGY SIMILARITY SEARCH SYSTEM".center(78) + "|")
    print("|" + "Interactive Demo".center(78) + "|")
    print("|" + " " * 78 + "|")
    print("+" + "=" * 78 + "+")
    
    # Load ontology
    print("\n>> Loading ontology...")
    try:
        onto = get_ontology("ontology/peace_pedagogy.owl").load()
        print("[OK] Ontology loaded successfully!")
    except Exception as e:
        print(f"[ERROR] Error loading ontology: {e}")
        print("\n[TIP] Please run 'python src/ontology_builder.py' first to create the ontology.")
        sys.exit(1)
    
    # Create similarity engine
    print(">> Initializing similarity engine...")
    engine = SimilarityEngine(onto)
    print("[OK] Engine ready!")
    
    # Check if lessons exist
    lessons = list(onto.Lesson.instances())
    if len(lessons) == 0:
        print("\n[ERROR] No lessons found in the ontology.")
        print("[TIP] Please run 'python src/data_loader.py' to load sample data.")
        sys.exit(1)
    
    # Run demos
    demo_all_lessons(onto)
    input("\n\n[Press Enter to continue to Similarity Search Demo...]")
    
    demo_similarity_search(onto, engine)
    input("\n\n[Press Enter to continue to Criteria Search Demo...]")
    
    demo_criteria_search(onto, engine)
    input("\n\n[Press Enter to continue to Custom Weights Demo...]")
    
    demo_custom_weights(onto, engine)
    
    # Final message
    print_header("DEMO COMPLETE")
    print("\n>> Thank you for exploring the Peace Pedagogy Similarity Search System!")
    print("\n>> For more information, see README.md")
    print(">> To customize, edit src/similarity_engine.py")
    print(">> To add lessons, edit data/sample_data.json\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n>> Demo interrupted. Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n[ERROR] An error occurred: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

