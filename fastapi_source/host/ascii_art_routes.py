import io
from fastapi.responses import StreamingResponse
from fastapi import APIRouter, UploadFile, File, Query
from fastapi_source.core.config import settings
from fastapi_source.application.ascii.ascii_service import get_mosaic_image

router = APIRouter(prefix=f'/{settings.ROUTER_NAME_Object_Detection}', 
                   tags=[settings.ROUTER_NAME_Object_Detection])

@router.put("/Mosaic", summary = "Make your image mosaic! 😁", 
            description = 'Upload your image file, and make it mosaic. 😃',
            response_class = StreamingResponse,
            responses = {200: {"content": {"image/png": {}}}})
async def detect(image_file: UploadFile = File(..., description="upload image file"),
                 block_size: int=Query(description="Sidelength of a mosaic block. Default value=10", default=10)):
    
    contents = await image_file.read()
    result_image = get_mosaic_image(contents, block_size)
    
    #save images to bytes
    img_byte_arr = io.BytesIO()
    result_image.save(img_byte_arr, format="PNG")
    img_byte_arr.seek(0) 
    
    return StreamingResponse(img_byte_arr, media_type = "image/png")