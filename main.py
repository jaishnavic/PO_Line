from fastapi import FastAPI, HTTPException, Request
from models import POLineRequest
from fusion_client import create_po_line
import json

app = FastAPI()

@app.post("/create-po-line")
async def create_po_line_api(request: Request):
    try:
        # 🔍 STEP 1: Get RAW request (before validation)
        raw_body = await request.json()

        print("\n===== RAW REQUEST FROM AGENT =====")
        print(json.dumps(raw_body, indent=4))
        print("==================================\n")

        # 🔍 STEP 2: Try validation manually
        try:
            validated_request = POLineRequest(**raw_body)
            payload = validated_request.dict()
        except Exception as validation_error:
            print("\n===== VALIDATION ERROR =====")
            print(str(validation_error))
            print("============================\n")

            raise HTTPException(
                status_code=422,
                detail=str(validation_error)
            )

        # 🔍 STEP 3: Call Fusion API
        result = create_po_line(payload)

        print("\n===== FUSION RESPONSE =====")
        print(json.dumps(result, indent=4))
        print("===========================\n")

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

    except Exception as e:
        print("\n===== ERROR =====")
        print(str(e))
        print("=================\n")

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )