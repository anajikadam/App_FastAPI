import asyncio

import time
import json
from typing import List, Optional
import shutil

import concurrent.futures
from fastapi import FastAPI, HTTPException
from fastapi import Form, Query, File, UploadFile, Response, status, Body
from fastapi import Request
from fastapi.templating import Jinja2Templates
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.responses import RedirectResponse
from fastapi.responses import HTMLResponse
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
# from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware

import pandas as pd
import aiofiles

from .routers import task1
from .config import logger

app = FastAPI()

# Include routers
app.include_router(task1.router)

app.mount("/static", StaticFiles(directory="fastapi_project/app/static"), name="static")
# app.mount("/Output", StaticFiles(directory="Output"), name="Output")
templates = Jinja2Templates(directory="fastapi_project/app/templates")

@app.get("/doc")
def read_root_docs():
    return {"message": "Welcome to the FastAPI app!"}

@app.get("/")
@app.get("/root")
@app.get("/api/")
def read_root(request: Request, ):
    sent = "--------/api/ In url redirect to index.html --------\n"
    print(sent)
    logger.info("Root endpoint called")  # Log info when root endpoint is accessed
    return templates.TemplateResponse("index.html", {"request": request,})

'''
Runs in main thread
No awaitable operation, cannot be paused
Sequential Order, wait for complete prev. operation..
'''

@app.get ('/1')
async def endpoint1():  # process sequentially
    print("1-->Hello")
    time.sleep(5) # Blocking 1/0 Operaition, cannot be awaited
    # Function execution cannot be paused
    print("1-->Bye")

'''
Runs in main thread
Has awaitable operation, can be paused
not wait for prev. operation it processed for next operation..
'''
@app.get ('/2')
async def endpoint2():  # process concurrently..
    print("2-->Hello")
    await asyncio.sleep(5)  # Non-Blocking I/0 Operation, awaited,
    # Function execution paused
    print("2-->Bye")

# Define a user-defined asynchronous function
async def user_defined_function():
    print("User-defined function started")
    await asyncio.sleep(5)  # Simulate a non-blocking I/O operation
    print("User-defined function completed")

@app.get('/22')
async def endpoint2():  # Process concurrently
    print("22 --> Hello")
    await user_defined_function()  # Await the user-defined function
    print("22 --> Bye")
'''
Runs in separate threads per used, process parallely
'''

@app.get ('/3')
def endpoint3():       # process Parallely
    print("3-->Hello")
    print("3-->Bye")


@app.get ('/3')
async def endpoint3():       # # Use async/await in this endpoint process Parallely
    print("3-->Hello")
    # Use a thread pool for blocking operations
    loop = asyncio.get_event_loop()  # Get the current event loop
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Submit the blocking function to the executor
        await loop.run_in_executor(executor, time.sleep, 5)  # Run in a separate thread

    # with concurrent.futures.ThreadPoolExecutor() as executor:
    #     future = executor.submit(time.sleep(5)) # Run in a separate thread
    #     future.result() # Wait for the result (non-blocking to main event loop)
    print("3-->Bye")

@app.get("/load-csv")
async def load_csv():
    try:
        # Path to your large CSV file
        CSV_FILE_PATH = "path/to/your/large_file.csv"
        async with aiofiles.open(CSV_FILE_PATH, mode='r') as file:
            # Read the content asynchronously
            content = await file.read()
        
        # Load the content into a DataFrame
        from io import StringIO
        df = pd.read_csv(StringIO(content))

        # Here you can process the DataFrame as needed
        print(df.head())  # Replace with your processing logic

        return {"message": "CSV loaded successfully!"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
# Uvicorn > Main Thread
# Coroutines runs in Event Loop in Main Thread

'''
BEST PRACTICES
1. use async def for endpoint with non-blocking I/0 operations
2. Don't use async def for endpoint with blocking I/0 operations
3. Use normal function for endpoints with blocking I/0 operations, 
DB client lib when seprate thread used for precessed..
'''