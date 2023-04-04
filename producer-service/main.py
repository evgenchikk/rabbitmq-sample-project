import uvicorn
from fastapi import FastAPI

from routers import image_router


producer_service = FastAPI()
producer_service.include_router(image_router.router)

@producer_service.get('/')
async def root():
    return {'message': 'see available endpoints at /docs'}


if __name__ == '__main__':
    uvicorn.run('main:producer_service', host="0.0.0.0", port=3000, reload=True)
