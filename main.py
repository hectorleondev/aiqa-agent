from fastapi import FastAPI
from fastapi.responses import JSONResponse


from api.routes import jira, health, messages
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


app.include_router(health.router)
app.include_router(jira.router)
app.include_router(messages.router)