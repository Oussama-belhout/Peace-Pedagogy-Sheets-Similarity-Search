"""
Simple test script to verify the Peace Pedagogy Similarity Search System
"""

from owlready2 import get_ontology
from src.similarity_engine import SimilarityEngine
import sys

def test_ontology():
    """Test that ontology loads correctly"""
    print("Test 1: Loading Ontology...")
    try:
        onto = get_ontology("ontology/peace_pedagogy.owl").load()
        print("  [PASS] Ontology loaded")
        
        # Check classes
        classes = list(onto.classes())
        print(f"  [INFO] Found {len(classes)} classes")
        
        # Check properties
        obj_props = list(onto.object_properties())
        data_props = list(onto.data_properties())
        print(f"  [INFO] Found {len(obj_props)} object properties")
        print(f"  [INFO] Found {len(data_props)} data properties")
        
        return onto
    except Exception as e:
        print(f"  [FAIL] {e}")
        return None

def test_lessons(onto):
    """Test that lessons are loaded"""
    print("\nTest 2: Checking Lessons...")
    try:
        lessons = list(onto.Lesson.instances())
        print(f"  [PASS] Found {len(lessons)} lessons")
        
        for lesson in lessons:
            title = lesson.title[0] if lesson.title else "No title"
            print(f"    - {title}")
        
        return lessons
    except Exception as e:
        print(f"  [FAIL] {e}")
        return []

def test_similarity(onto, lessons):
    """Test similarity search"""
    print("\nTest 3: Testing Similarity Engine...")
    try:
        engine = SimilarityEngine(onto)
        print("  [PASS] Engine initialized")
        
        if len(lessons) < 2:
            print("  [SKIP] Not enough lessons to test similarity")
            return True
        
        target = lessons[0]
        similar = engine.find_similar(target, top_k=2)
        
        print(f"  [PASS] Found {len(similar)} similar lessons to '{target.title[0]}'")
        
        for lesson, score, _ in similar:
            print(f"    - {lesson.title[0]}: {score:.3f}")
        
        return True
    except Exception as e:
        print(f"  [FAIL] {e}")
        import traceback
        traceback.print_exc()
        return False

def test_criteria_search(onto):
    """Test search by criteria"""
    print("\nTest 4: Testing Criteria Search...")
    try:
        engine = SimilarityEngine(onto)
        
        # Search for lessons with peace_with_environment
        matching = engine.search_by_criteria(axes=["peace_with_environment"])
        
        print(f"  [PASS] Found {len(matching)} lessons with 'peace_with_environment'")
        
        for lesson in matching:
            print(f"    - {lesson.title[0]}")
        
        return True
    except Exception as e:
        print(f"  [FAIL] {e}")
        return False

def main():
    """Run all tests"""
    print("="*60)
    print("Peace Pedagogy Similarity Search System - Test Suite")
    print("="*60)
    
    # Test 1: Load ontology
    onto = test_ontology()
    if onto is None:
        print("\n[ERROR] Cannot proceed without ontology")
        sys.exit(1)
    
    # Test 2: Check lessons
    lessons = test_lessons(onto)
    if len(lessons) == 0:
        print("\n[WARNING] No lessons found. Run 'python src/data_loader.py' to load data.")
    
    # Test 3: Test similarity
    test_similarity(onto, lessons)
    
    # Test 4: Test criteria search
    test_criteria_search(onto)
    
    print("\n" + "="*60)
    print("All tests completed!")
    print("="*60)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n[ERROR] Test suite failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)



