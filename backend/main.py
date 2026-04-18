from fastapi import FastAPI, HTTPException, Response, Request
from typing import List
from pydantic import ValidationError
from datetime import datetime
import calendar
import xml.etree.ElementTree as ET
from xml.dom import minidom
from services.distribution import generate_transaction_schedule
from schemas import DistributionRequest, DistributionResponse
from tally_schemas import TallyDistributionResponse, TallyTransactionEntry
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Financial Distribution Engine")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Endpoints ────────────────────────────────────────────────

@app.post("/generate-plan", response_model=DistributionResponse)
async def generate_plan(request: DistributionRequest):
    try:
        return generate_transaction_schedule(
            total_amount=request.total_amount,
            months=request.months,
            financial_year_start=request.financial_year_start
        )
    except Exception as e:
        print(f"Error in generate_plan: {str(e)}")
        raise HTTPException(status_code=500, detail={
            "error": "Internal server error",
            "details": str(e) if __debug__ else "An unexpected error occurred"
        })


@app.post("/generate-plan-tally-xml")
async def generate_plan_tally_xml(request: Request):
    """
    Endpoint for Tally Prime TDL HTTP Post action.
    Tally sends XML wrapped in <ENVELOPE><REQUEST>...</REQUEST></ENVELOPE>
    Returns XML with <STATUS>1</STATUS> for success, <STATUS>0</STATUS> for failure.
    """
    try:
        # Read raw XML body from Tally
        body = await request.body()
        body_str = body.decode("utf-8", errors="ignore")
        print(f"[Tally XML] Received body: {body_str}")

        # Parse XML sent by Tally
        root = ET.fromstring(body_str)

        # Search for fields at any depth (Tally wraps in ENVELOPE)
        def find_text(tag):
            el = root.find(f".//{tag}")
            return el.text.strip() if el is not None and el.text else None

        total_amount_str     = find_text("total_amount")
        months_str           = find_text("months")
        financial_year_start = find_text("financial_year_start")

        print(f"[Tally XML] Parsed: amount={total_amount_str}, months={months_str}, fy={financial_year_start}")

        if not total_amount_str or not months_str or not financial_year_start:
            raise ValueError(f"Missing required fields. Received XML: {body_str}")

        total_amount = float(total_amount_str)
        months       = int(months_str)

        # Call existing distribution service
        result = generate_transaction_schedule(
            total_amount=total_amount,
            months=months,
            financial_year_start=financial_year_start
        )

        # Build Tally-compatible XML response
        # STATUS=1 → Tally shows Success Report
        # STATUS=0 → Tally shows Error Report
        resp_root = ET.Element("RESPONSE")
        ET.SubElement(resp_root, "STATUS").text  = "1"
        ET.SubElement(resp_root, "MESSAGE").text = "Distribution plan generated successfully"

        data_el = ET.SubElement(resp_root, "DATA")
        for month_block in result["monthly_distribution"]:
            for entry in month_block["entries"]:
                item = ET.SubElement(data_el, "ITEM")
                ET.SubElement(item, "MONTH").text  = month_block["month"]
                ET.SubElement(item, "DATE").text   = entry["date"]
                ET.SubElement(item, "AMOUNT").text = str(entry["amount"])

        rough  = ET.tostring(resp_root, encoding="unicode")
        pretty = minidom.parseString(rough).toprettyxml(indent="  ")

        print(f"[Tally XML] Responding with STATUS=1, items generated successfully")
        return Response(content=pretty, media_type="application/xml")

    except Exception as e:
        print(f"[Tally XML] Error: {str(e)}")
        err_xml = f"<RESPONSE><STATUS>0</STATUS><MESSAGE>{str(e)}</MESSAGE></RESPONSE>"
        return Response(content=err_xml, media_type="application/xml", status_code=200)


@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "Financial Distribution Engine is running"}


# ── Exception handlers ───────────────────────────────────────

@app.exception_handler(ValidationError)
async def validation_exception_handler(request, exc):
    from fastapi.responses import JSONResponse
    return JSONResponse(
        status_code=422,
        content={"error": "Invalid input", "details": str(exc)}
    )

@app.exception_handler(Exception)
async def generic_exception_handler(request, exc):
    from fastapi.responses import JSONResponse
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error", "details": "An unexpected error occurred"}
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=48765)