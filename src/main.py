import uuid
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from src.database import init_db
from src.image_processor.routers import image_router
from src.common.constants import ServerConfiguration
from src.common.logging import request_id_var



app = FastAPI(
    title="Open Innovation AI",
    version="1.0.0",
    swagger_ui_parameters={"displayRequestDuration": True}
)


# Initialize the database when the app starts
init_db()

app.include_router(image_router.router)

# Health Check API
@app.get("/v1/health", tags=["Health"])
async def health_check():
    """
    Health check API to verify if the server is running properly.
    """
    return JSONResponse(status_code=200, content={
        "status": "healthy"
    })

# FastAPI middleware to set the request ID
@app.middleware("http")
async def add_request_id_to_logs(request: Request, call_next):
    # Generate a unique request ID
    request_id = str(uuid.uuid4())
    # Set the request ID in the context variable
    request_id_var.set(request_id)

    # Process the request
    response = await call_next(request)

    return response

# Run the FastAPI application using `uvicorn` server
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app",
                host=ServerConfiguration.SERVER_HOST,
                port=ServerConfiguration.SERVER_PORT,
                reload=True,
                log_level=ServerConfiguration.LOG_LEVEL.lower()
                )

