import re

from fastapi import APIRouter, UploadFile, Depends, HTTPException, Request
from fastapi.responses import StreamingResponse

from services.image_service import ImageService


router = APIRouter(
    prefix='/image',
    tags=['image'],
)


@router.get('/{id}')
async def get_image(id: str,
                    image_service: ImageService = Depends()):

    try:
        bytes_iterator, file_extension = await image_service.get_image_by_id(id=id)
    except Exception as e:
        return HTTPException(status_code=500,
                             detail=str(e))

    return StreamingResponse(content=bytes_iterator,
                             status_code=200,
                             headers={'Content-Disposition': f'attachment; filename=picture.{file_extension}'})


@router.post('')
async def post_image(file: UploadFile = None,
                     image_service: ImageService = Depends()):

    if (file == None):
        return HTTPException(status_code=400,
                             detail=f'method requires file upload{str(e)}')

    content_type: str = file.content_type
    file_binary: bytes = await file.read()

    try:
        id = await image_service.upload_image(content_type, file_binary)
    except Exception as e:
        return HTTPException(status_code=500,
                             detail=str(e))

    return {'message': f'uploaded successfully: id {id}'}


@router.post('/{id}')
async def process_image(id: int,
                        request: Request = None,
                        image_service: ImageService = Depends()):

    if request == None:
            return HTTPException(status_code=400,
                                detail='method requires action parameter: {action\: resize H,W} or {action\: grayscale}.' + str(e))

    request_json = await request.json()

    action = ''
    try:
        action = request_json['action']
    except Exception as e:
        return HTTPException(status_code=400,
                             detail='method requires action parameter: {"action"\: "resize W,H"} or {"action"\: "grayscale"}.' + str(e))

    match = re.match(r'^(resize)(\s+\d+,\d+)|(grayscale\s*)$', action)

    if match == None:
        return HTTPException(status_code=400,
                             detail='method requires action parameter: {"action"\: "resize H,W"} or {"action"\: "grayscale"}')

    try:
        await image_service.process_image_by_id(id, action)
    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))

    return {'message': 'ok'}
