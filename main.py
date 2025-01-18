# main.py
from uuid import UUID
from fastapi import FastAPI, HTTPException
import uvicorn
from app.backend import Backend
from app.serializers.receipt_model import ReceiptModel



app = FastAPI()

instance = Backend()

@app.post("/receipts/process")
async def post_receipt(receipt: ReceiptModel):
    response = instance.add_receipt(receipt)
    if "error" in response:
        raise HTTPException(422, response["error"])
    return response

@app.get("/receipts/{receipt_id}/points")
async def get_points(receipt_id: UUID):
    response = instance.get_points(receipt_id)
    if not response:
        raise HTTPException(404, f'{receipt_id} not found.')
    return response

@app.get("/")
async def root():
    return {"hello": "world"}

if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)




