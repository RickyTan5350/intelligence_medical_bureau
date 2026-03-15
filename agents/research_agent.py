from google.adk.agents import Agent
from google.adk.models import Gemini
from tools.research_tools import (
    scrape_web_page, 
    extract_text_from_pdf, 
    list_available_resources, 
    index_research_finding
)

def create_research_agent(model_name="gemini-2.0-flash"):
    """Creates the strategic research swarm agent."""
    model = Gemini(model_name=model_name)
    
    # Define Tools for ADK
    tools = [
        scrape_web_page, 
        extract_text_from_pdf, 
        list_available_resources, 
        index_research_finding
    ]

    return Agent(
        name="research_swarm",
        description="Strategic Research Agent capable of scouting, analysis, and strategic synthesis.",
        instruction="""
        You are a Strategic Research Swarm. Your task is to perform an end-to-end investigation:
        
        PHASE 1: SCOUTING 
        - Use 'list_available_resources' to find relevant local PDFs.
        - Use 'extract_text_from_pdf' (for PDFs) or 'scrape_web_page' (for URLs) to gather raw evidence.
        
        PHASE 2: ANALYSIS
        - Synthesize all gathered raw data, identify key patterns, and extract facts.
        
        PHASE 3: STRATEGIC SYNTHESIS
        - Formulate a high-level strategic report based on your analysis.
        - MUST: Use 'index_research_finding' to save your final synthesis into the knowledge base.
        
        Always provide a clear, professional report as your final output.
        """,
        tools=tools,
        model=model
    )
