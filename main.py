from fastapi import FastAPI
from fastapi.responses import JSONResponse
from datetime import datetime

from api.routes import jira
from core.exceptions import BadRequest, NotFound, InternalServerError

app = FastAPI(title="IA QA AGENT")


# Exception handlers (replaces your decorator)
@app.exception_handler(BadRequest)
async def bad_request_handler(request, exc):
    return JSONResponse(status_code=400, content={"error": str(exc)})


@app.exception_handler(NotFound)
async def not_found_handler(request, exc):
    return JSONResponse(status_code=404, content={"error": str(exc)})


@app.exception_handler(InternalServerError)
async def internal_server_error_handler(request, exc):
    return JSONResponse(status_code=500, content={"error": "Internal server error"})


app.include_router(jira.router)


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "message": "IA QA AGENT is running smoothly",
        "time": datetime.now().isoformat(),
    }
