from fastapi import FastAPI

def create_app() -> FastAPI:
    return FastAPI(title="Waypoint Partner Source API", version="1.0.0")

app = create_app()

