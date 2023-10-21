import io
import os
import uvicorn
import logging
from PIL import Image
from rembg import remove
from shazamio import Shazam
from fastapi.responses import Response, JSONResponse
from fastapi import FastAPI, UploadFile, File, HTTPException

# Configure logging
logging.basicConfig(level=logging.INFO)


app = FastAPI()


@app.get('/')
async def root():
    return 'Running...'


@app.post('/shazam')
async def shazam(file: UploadFile = File(...)):
    logging.info("Shazam endpoint hit")
    try:
        sz = Shazam()
        content = await file.read()
        output = await sz.recognize_song(content)
        logging.info("Song recognized")
        return JSONResponse(content=output['track'])
    except Exception as e:
        logging.error(f"An error occurred: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="An error occurred.")


@app.post('/removebg')
async def removebg(image: UploadFile = File(...)):
    logging.info("RemoveBG endpoint hit")
    try:
        input = Image.open(image.file)
        output = remove(input)
        logging.info("Background removed")
        output_buffer = io.BytesIO()
        output.save(output_buffer, format='PNG')
        output_buffer.seek(0)
        return Response(content=output_buffer.getvalue(), media_type="image/png")
    except Exception as e:
        logging.error(f"An error occurred: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="An error occurred.")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
