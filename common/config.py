from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


def create_app():
    app = FastAPI()

    origins = [
        "http://localhost",
        "http://localhost:8011",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["*"],
    )

    return app


app = create_app()
