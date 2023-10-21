import io
import os
from PIL import Image
from rembg import remove
from shazamio import Shazam
from fastapi import FastAPI, UploadFile, File, HTTPException


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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
