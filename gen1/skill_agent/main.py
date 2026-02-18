import sys
from pathlib import Path

# Add src to path so relative imports work if running as a script
sys.path.append(str(Path(__file__).parent / "src"))

from src.crew import SkillsCrew
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def main():
    """
    Main entry point for the Skills Agent.
    """
    print("\n--- Initializing Skills Crew ---\n")
    
    try:
        crew = SkillsCrew()
        
        # Sample task description
        task_desc = "Research the different types of memory architectures used in LLM agents and explain their pros and cons."
        
        print(f"Goal: {task_desc}\n")
        print("Starting execution (this may take a minute)...\n")
        
        result = crew.run(task_description=task_desc)
        
        print("\n--- Task Result ---\n")
        print(result)
        
    except Exception as e:
        print(f"\n❌ Error running Skills Crew: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
