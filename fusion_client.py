import requests
from config import FUSION_BASE_URL, FUSION_USERNAME, FUSION_PASSWORD

def create_po_line(payload: dict):
    try:
        # Extract POHeaderID
        po_header_id = payload.pop("POHeaderID")

        # Construct URL
        url = f"{FUSION_BASE_URL}/fscmRestApi/resources/11.13.18.05/draftPurchaseOrders/{po_header_id}/child/lines"

        # Build headers
        headers = {
            "Content-Type": "application/vnd.oracle.adf.resourceitem+json",
            "REST-Framework-Version": "2",
            "Upsert-Mode": "true"
        }

        # Ensure correct types
        body = {
            "LineNumber": int(payload["LineNumber"]),
            "LineType": payload["LineType"],
            "Category": payload["Category"],
            "Description": payload["Description"],
            "Quantity": float(payload["Quantity"]),
            "Price": float(payload["Price"]),
            "UOM": payload["UOM"]
        }

        # Debug logs
        print("URL:", url)
        print("BODY:", body)

        # API call
        response = requests.post(
            url,
            json=body,
            headers=headers,
            auth=(FUSION_USERNAME, FUSION_PASSWORD)
        )

        # Handle response
        if response.status_code in [200, 201]:
            return {
                "status": "success",
                "data": response.json()
            }
        else:
            return {
                "status": "error",
                "status_code": response.status_code,
                "message": response.text
            }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }