# __run fast api application __
import uvicorn

from src.app.initialize.server_creator import create_server
from src.utils.config import components

server = create_server(repositories=components.repositories_com)

if __name__ == "__main__":
    uvicorn.run("server_app_run:server",
                host='0.0.0.0',
                port=8080,
                lifespan="on",
                log_level="debug",
                reload=True
                )
