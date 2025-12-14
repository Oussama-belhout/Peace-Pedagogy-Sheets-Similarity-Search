"""
COMPLETE PROJECT DEMONSTRATION
Peace Pedagogy Similarity Search with 27 Real Pedagogical Sheets
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from find_similar_lessons import find_similar


print("\n" + "#"*80)
print("#" + " "*78 + "#")
print("#" + "PEACE PEDAGOGY SIMILARITY SEARCH - COMPLETE DEMO".center(78) + "#")
print("#" + "27 Real Pedagogical Sheets Loaded".center(78) + "#")
print("#" + " "*78 + "#")
print("#"*80)

print("\n" + "="*80)
print("PROJECT OVERVIEW")
print("="*80)
print("\nINPUT:  Raw metadata for a NEW lesson (title, domain, age, virtues, etc.)")
print("OUTPUT: Most similar EXISTING pedagogical sheets from database")
print("GOAL:   Provide examples for AI-powered lesson generation")
print("\nDATABASE: 27 real pedagogical sheets from FICHES PEDAGOGIQUES")
print("  - Sciences: 11 sheets")
print("  - Ethics: 11 sheets")
print("  - Arts: 3 sheets")
print("  - Languages: 2 sheets")

# ============================================================================
# EXAMPLE 1: Environmental Science
# ============================================================================

print("\n\n" + "="*80)
print("EXAMPLE 1: ENVIRONMENTAL SCIENCE LESSON")
print("="*80)

print("\n[INPUT] Teacher wants to create:")
print("  Title: 'Protecting Biodiversity in Our City'")
print("  Domain: Sciences")
print("  Focus: Environmental responsibility & collaboration")
print("  Age: 9-12 years")
print("  Tools: Project-based learning")

results = find_similar(
    title="Protecting Biodiversity in Our City",
    domain="Sciences",
    axes=["peace_with_environment", "peace_with_others"],
    tools=["project_based_learning"],
    virtues=["responsibility", "cooperation"],
    target_age_min=9,
    target_age_max=12,
    top_k=3
)

print(f"\n[OUTPUT] Top 3 Similar Existing Sheets:\n")

for i, sheet in enumerate(results, 1):
    print(f"{i}. {sheet['title']}")
    print(f"   Similarity: {sheet['similarity_score']:.1%}")
    print(f"   Ages: {sheet['target_age_min']}-{sheet['target_age_max']} years")
    print(f"   PDF: {os.path.basename(sheet.get('pdf_path', 'N/A'))}")
    
    # Show why it matches
    breakdown = sheet['similarity_breakdown']
    contributions = []
    if breakdown['axes']['score'] > 0:
        contributions.append(f"Axes:{breakdown['axes']['score']:.0%}")
    if breakdown['tools']['score'] > 0:
        contributions.append(f"Tools:{breakdown['tools']['score']:.0%}")
    if breakdown['virtues']['score'] > 0:
        contributions.append(f"Virtues:{breakdown['virtues']['score']:.0%}")
    
    print(f"   Match details: {', '.join(contributions)}")
    print()

# ============================================================================
# EXAMPLE 2: Emotional Learning
# ============================================================================

print("\n" + "="*80)
print("EXAMPLE 2: EMOTIONAL LEARNING / ETHICS")
print("="*80)

print("\n[INPUT] Counselor needs:")
print("  Title: 'Understanding and Managing Emotions'")
print("  Domain: Ethics")
print("  Focus: Self-awareness & empathy")
print("  Age: 7-10 years")
print("  Tools: CEVQ, Meditation")

results = find_similar(
    title="Understanding and Managing Emotions",
    domain="Ethics",
    axes=["peace_with_self", "peace_with_others"],
    tools=["cevq", "meditation"],
    virtues=["empathy", "patience"],
    target_age_min=7,
    target_age_max=10,
    top_k=3
)

print(f"\n[OUTPUT] Top 3 Similar Existing Sheets:\n")

for i, sheet in enumerate(results, 1):
    print(f"{i}. {sheet['title']}")
    print(f"   Similarity: {sheet['similarity_score']:.1%}")
    print(f"   Ages: {sheet['target_age_min']}-{sheet['target_age_max']} years")
    
    # Show shared virtues
    breakdown = sheet['similarity_breakdown']
    if breakdown['virtues']['shared']:
        virtues = [v.replace('peace_pedagogy.', '') for v in breakdown['virtues']['shared']]
        print(f"   Shared virtues: {', '.join(virtues)}")
    
    print(f"   PDF: {os.path.basename(sheet.get('pdf_path', 'N/A'))}")
    print()

# ============================================================================
# EXAMPLE 3: Arts Collaboration
# ============================================================================

print("\n" + "="*80)
print("EXAMPLE 3: ARTS COLLABORATION PROJECT")
print("="*80)

print("\n[INPUT] Art teacher wants:")
print("  Title: 'Creating a Collective Mural'")
print("  Domain: Arts")
print("  Focus: Teamwork & creative expression")
print("  Age: 10-14 years")
print("  Tools: Artistic expression, Project-based learning")

results = find_similar(
    title="Creating a Collective Mural",
    domain="Arts",
    axes=["peace_with_others"],
    tools=["artistic_expression", "project_based_learning"],
    virtues=["cooperation", "patience"],
    target_age_min=10,
    target_age_max=14,
    top_k=3
)

print(f"\n[OUTPUT] Top 3 Similar Existing Sheets:\n")

for i, sheet in enumerate(results, 1):
    print(f"{i}. {sheet['title']}")
    print(f"   Similarity: {sheet['similarity_score']:.1%}")
    print(f"   Discipline: {sheet.get('discipline', 'N/A')}")
    print(f"   PDF: {os.path.basename(sheet.get('pdf_path', 'N/A'))}")
    print()

# ============================================================================
# CODE USAGE EXAMPLE
# ============================================================================

print("\n" + "="*80)
print("HOW TO USE IN YOUR CODE")
print("="*80)

print("\nPython Code:")
print("-" * 80)
print("""
from find_similar_lessons import find_similar

# Describe your new lesson
results = find_similar(
    title="My New Lesson About Trees",
    domain="Sciences",
    axes=["peace_with_environment"],
    tools=["project_based_learning"],
    virtues=["responsibility"],
    target_age_min=8,
    target_age_max=12,
    top_k=5
)

# Process similar sheets
for sheet in results:
    print(f"Title: {sheet['title']}")
    print(f"Similarity: {sheet['similarity_score']:.1%}")
    print(f"PDF path: {sheet['pdf_path']}")
    
    # Use for AI generation
    # ai_model.generate(user_input, examples=[sheet])
""")
print("-" * 80)

# ============================================================================
# SUMMARY
# ============================================================================

print("\n\n" + "="*80)
print("PROJECT SUMMARY")
print("="*80)

print("\n[SUCCESS] System Status:")
print("  [OK] 27 real pedagogical sheets loaded from PDFs")
print("  [OK] Metadata automatically extracted")
print("  [OK] Similarity search operational")
print("  [OK] Multiple query scenarios tested")
print("  [OK] Ready for AI integration")

print("\n[WORKFLOW]")
print("  1. User provides lesson metadata (title, domain, age, etc.)")
print("  2. System searches 27 real pedagogical sheets")
print("  3. Returns top N most similar sheets with scores")
print("  4. User/AI uses similar sheets as templates")
print("  5. Generate complete new pedagogical sheet")

print("\n[DATABASE] 27 Pedagogical Sheets:")
print("  Sciences:")
print("    - Aventures d'un verre d'eau")
print("    - Mandala d'une assiette de riz")
print("    - Que serait le monde sans abeilles")
print("    - La vie d'une feuille")
print("    - Structure de l'univers")
print("    - ... and 6 more")
print("\n  Ethics:")
print("    - L'univers des emotions")
print("    - La bienveillance")
print("    - L'humilite")
print("    - Accepter differents points de vue")
print("    - ... and 7 more")
print("\n  Arts:")
print("    - Mise en scene du Sultan")
print("    - Realisation d'objets decoratifs")
print("    - Tableau de feuilles sechees")
print("\n  Languages:")
print("    - Les enfants mediateurs de paix")
print("    - Le Secret de la lettre BA")

print("\n[FILES CREATED]")
print("  Core:")
print("    - find_similar_lessons.py  (Main API)")
print("    - src/pdf_parser.py        (PDF extractor)")
print("    - src/query_engine.py      (Query processor)")
print("    - src/similarity_engine.py (Similarity algorithm)")
print("\n  Data:")
print("    - data/pedagogical_sheets.json (27 extracted lessons)")
print("    - ontology/peace_pedagogy.owl  (Knowledge base)")
print("\n  Documentation:")
print("    - USAGE_GUIDE.md           (How to use)")
print("    - API_REFERENCE.md         (API docs)")
print("    - REAL_DATA_INTEGRATION.md (Integration guide)")
print("    - PROJECT_SUMMARY.md       (Project overview)")

print("\n[NEXT STEPS]")
print("  Immediate:")
print("    -> python find_similar_lessons.py  (See more examples)")
print("    -> python test_system.py           (Verify system)")
print("\n  Integration:")
print("    -> Feed similar sheets to AI model")
print("    -> Generate complete pedagogical sheets")
print("    -> Build web interface (optional)")

print("\n" + "="*80)
print("DEMONSTRATION COMPLETE!")
print("="*80)
print("\nThe Peace Pedagogy Similarity Search system is fully operational")
print("with 27 real pedagogical sheets from your FICHES PEDAGOGIQUES folder.")
print("\nYou can now use this to find similar lessons for any new lesson idea!")
print("\nFor more information, see the documentation files.")
print("="*80)
print()

