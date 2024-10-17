import uvicorn, re, webbrowser, threading, time
from fastapi import FastAPI
from fastapi_source.host.ascii_art_routes import router as ascii_router
from starlette.routing import Route
from fastapi_source.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME_EN_US,
    description=settings.PROJECT_NAME_EN_US,
    version=settings.VERSION,
    openapi_tags=[
        {
            "name": settings.ROUTER_NAME_Object_Detection,
            "description": settings.ROUTER_Description_Object_Detection
        }
    ])

#router register
app.include_router(ascii_router)

#make api path "case-insensitive"
for route in app.router.routes:
    if isinstance(route, Route):
        route.path_regex = re.compile(route.path_regex.pattern, re.IGNORECASE)

#run api !
if __name__ == "__main__":
    def open_browser():
        #wait for two seconds
        time.sleep(2)
        webbrowser.open("http://127.0.0.1:8000/docs")
    print("Waiting for browser...")
    #open browser
    threading.Thread(target=open_browser).start()
    uvicorn.run("fast-api-main:app", host="0.0.0.0", port=8000, reload=True)
    
    
# Example usage:
# python3 fast-api-main.py