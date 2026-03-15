import os
import sys
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

# Add root folder to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.main import IntelligenceBureau

app = FastAPI(title="Intelligence Bureau Web API")

# Serve static files
static_dir = os.path.join(os.path.dirname(__file__), "static")
if not os.path.exists(static_dir):
    os.makedirs(static_dir)

app.mount("/static", StaticFiles(directory=static_dir), name="static")

bureau = IntelligenceBureau()

class ResearchRequest(BaseModel):
    query: str

@app.get("/", response_class=HTMLResponse)
async def read_root():
    with open(os.path.join(static_dir, "index.html"), "r", encoding="utf-8") as f:
        return f.read()

@app.post("/api/research")
def do_research(req: ResearchRequest):
    try:
        report = bureau.run_swarm_pipeline(req.query)
        return {"status": "success", "report": report}
    except Exception as e:
        return {"status": "error", "message": str(e)}
