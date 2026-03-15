import os
import sys
from dotenv import load_dotenv

# Ensure the root directory is on the path so we can import agents and tools
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from google.adk.runners import Runner
from google.adk.sessions.in_memory_session_service import InMemorySessionService
from google.genai import types

from agents.research_agent import create_research_agent

# Load environment variables
load_dotenv()

# Project Configuration
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "gemininexus6")
LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")

# Force google-genai to use Vertex AI backend (for gcloud/ADC auth)
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "True"
os.environ["GOOGLE_CLOUD_PROJECT"] = PROJECT_ID
os.environ["GOOGLE_CLOUD_LOCATION"] = LOCATION

# Set up local resource path
RESOURCES_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "resources")
if not os.path.exists(RESOURCES_DIR):
    os.makedirs(RESOURCES_DIR)

# Load API key if available
api_key = os.getenv("GOOGLE_API_KEY")
if api_key and api_key != "your_gemini_api_key_here":
    import google.generativeai as old_genai # for compatibility if needed
    old_genai.configure(api_key=api_key)
else:
    print(f"[*] Intelligence Bureau: Using GCloud Project '{PROJECT_ID}' for authentication.")

class IntelligenceBureau:
    def __init__(self):
        self.research_swarm = create_research_agent()
        self.session_service = InMemorySessionService()
        self.runner = Runner(
            app_name=PROJECT_ID,
            agent=self.research_swarm,
            session_service=self.session_service,
            auto_create_session=True
        )

    def run_swarm_pipeline(self, research_topic: str):
        print(f"\n[!] INTELLIGENCE BUREAU: DISPATCHING SWARM FOR: '{research_topic}'")
        
        user_id = "default_user"
        from datetime import datetime
        session_id = f"research_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        final_report = ""
        for event in self.runner.run(
            user_id=user_id,
            session_id=session_id,
            new_message=types.Content(parts=[types.Part(text=f"Full Research Objective: {research_topic}")])
        ):
            if event.content and event.content.parts:
                for part in event.content.parts:
                    if part.text:
                        final_report += part.text

        return final_report

def main():
    print("--- INTELLIGENCE BUREAU: MULTI-AGENT SWARM (v3.0 - ADK) ---")
    print(f"[*] Project ID: {PROJECT_ID}")
        
    bureau = IntelligenceBureau()
    
    while True:
        print("\n" + "="*60)
        query = input("Enter Research Objective (or 'exit'): ")
        if query.lower() in ['exit', 'quit']:
            break
            
        try:
            report = bureau.run_swarm_pipeline(query)
            print("\n" + "*"*30 + " FINAL BUREAU STRATEGIC REPORT " + "*"*30)
            print(report)
            print("*" * 90)
        except Exception as e:
            print(f"SWARM ERROR: {e}")

if __name__ == "__main__":
    main()
