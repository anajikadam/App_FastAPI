import uvicorn, os

# from app import main
from fastapi_project.app.config import ip, port, debug_flag, reload_flag
from fastapi_project.app.config import logger


# Set the environment variable APP_ENV to 'deployment'
# os.environ['APP_ENV'] = 'deployment'
os.environ['APP_ENV'] = 'local'

if __name__ == "__main__":
    logger.info("Starting FastAPI application...")  # Log when starting the application
    print("App Started...!!!!!")
    print(f"Starting server on {ip}:{port}")
    uvicorn.run("fastapi_project.app.main:app", 
                host = ip, 
                port = port,
                # debug = True, # unexpected keyword argument 'debug'
                # reload=True,    #reload_flag          # Enable reload for development
                limit_concurrency=3,      # Limit concurrent connections
                # workers=4                 # Set the number of worker processes
                )

# limit_concurrency = 3, #Small (e.g., 3 for testing) and for deployment Higher, based on server resources



