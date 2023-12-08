import uvicorn

from common.config import app
from common.router import register_router

register_router(app)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8011)
