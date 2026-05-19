import sys
import os


sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agent.manager import AutoDocAgent

def main():
    print("=========================================")
    print("   AUTO-DOC AGENT CLI - RUNNING WORKFLOW ")
    print("=========================================\n")
    
    
    
    agent = AutoDocAgent(target_dir=target)
    agent.run_react_loop()
    
    print("\n=========================================")
    print("         WORKFLOW TERMINÉ AVEC SUCCÈS    ")
    print("=========================================")

if __name__ == "__main__":
    main()