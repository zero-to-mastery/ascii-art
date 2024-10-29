import uvicorn
import re
import webbrowser
import threading
import time
from fastapi import FastAPI
from fastapi_source.host.ascii_art_routes import router as ascii_router
from starlette.routing import Route
from fastapi_source.core.config import settings

# Initialize FastAPI app with project metadata
app = FastAPI(
    title=settings.PROJECT_NAME_EN_US,
    description=settings.PROJECT_DESCRIPTION_EN_US,
    version=settings.VERSION,
    openapi_tags=[
        {
            "name": settings.ROUTER_NAME_Object_Detection,
            "description": settings.ROUTER_DESCRIPTION_Object_Detection
        }
    ]
)

# Register the ASCII art router
app.include_router(ascii_router)

# Convert all API routes to be case-insensitive
for route in app.router.routes:
    if isinstance(route, Route):
        route.path_regex = re.compile(route.path_regex.pattern, re.IGNORECASE)

# Function to open the browser to the API documentation
def open_browser():
    """Open the API documentation in the default browser after a delay."""
    time.sleep(2)  # wait for server to start
    webbrowser.open("http://127.0.0.1:8000/docs")

# Start the API with live reloading and auto browser open
if __name__ == "__main__":
    print("Starting server and waiting to open the browser...")
    threading.Thread(target=open_browser).start()
    uvicorn.run("fast-api-main:app", host="0.0.0.0", port=8000, reload=True)

# Example usage:
# python3 fast-api-main.py
