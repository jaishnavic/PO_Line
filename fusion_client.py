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
    "Item": payload["Item"],
    "Category": payload["Category"],
    "Description": payload["Description"],
    "Quantity": float(payload["Quantity"]),
    "Price": float(payload["Price"]),
    "UOM": payload["UOM"],

    "schedules": [
        {
            "ScheduleNumber": int(schedule["ScheduleNumber"]),
            "Quantity": float(schedule["Quantity"]),
            "ShipToLocation": schedule["ShipToLocation"],
            "ShipToOrganizationCode": schedule["ShipToOrganizationCode"],
            "ReceiptCloseTolerancePercent": float(schedule["ReceiptCloseTolerancePercent"]),
            "InvoiceMatchOptionCode": schedule["InvoiceMatchOptionCode"],
            "EarlyReceiptToleranceDays": int(schedule["EarlyReceiptToleranceDays"]),
            "InvoiceCloseTolerancePercent": float(schedule["InvoiceCloseTolerancePercent"]),
            "LateReceiptToleranceDays": int(schedule["LateReceiptToleranceDays"]),
            "AccrueAtReceiptFlag": bool(schedule["AccrueAtReceiptFlag"]),
            "InspectionRequiredFlag": bool(schedule["InspectionRequiredFlag"]),
            "ReceiptRequiredFlag": bool(schedule["ReceiptRequiredFlag"]),
            "RequestedDeliveryDate": schedule["RequestedDeliveryDate"],
            "RequestedShipDate": schedule["RequestedShipDate"],
            "ReceiptRoutingId": int(schedule["ReceiptRoutingId"]),
            "DestinationTypeCode": schedule["DestinationTypeCode"],
            "Carrier": schedule["Carrier"],

            "distributions": [
                {
                    "DistributionNumber": int(distribution["DistributionNumber"]),
                    "DeliverToLocation": distribution["DeliverToLocation"],
                    "POChargeAccountId": int(distribution["POChargeAccountId"]),
                    "Quantity": float(distribution["Quantity"])
                }
                for distribution in schedule.get("distributions", [])
            ]
        }
        for schedule in payload.get("schedules", [])
    ]
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