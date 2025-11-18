from datetime import datetime

from fastapi import FastAPI, Request, Response

from client.lifespan.start_app import start_app
from api.api import router
from client.config.config import StartApp, Config
from log.log import logger

app = FastAPI(title=Config.title,
              description=Config.description,
              lifespan=start_app)
app.include_router(router=router)

@app.middleware('http')
async def log_routers(request: Request, call_next) -> Response:
    start_time = datetime.now()
    
    logger.info(f"request: {request.method}, url: {request.url}")
    response = await call_next(request)
    
    duration = (datetime.now() - start_time).total_seconds()
    logger.info(f"answer: {response.status_code} | time: {duration:.2f}s")
    
    return response


if __name__ == "__main__":
    start = StartApp()
    start.run()