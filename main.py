from fastapi import FastAPI, HTTPException
from models import POLineRequest
from fusion_client import create_po_line

app = FastAPI()

@app.post("/create-po-line")
def create_po_line_api(request: POLineRequest):
    payload = request.dict()

    result = create_po_line(payload)

    if result["status"] == "success":
        return {
            "message": "PO Line created successfully",
            "fusion_response": result["data"]
        }
    else:
        raise HTTPException(
            status_code=400,
            detail=result
        )