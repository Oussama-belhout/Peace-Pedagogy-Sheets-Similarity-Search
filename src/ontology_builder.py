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



