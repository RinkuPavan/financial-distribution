from fastapi import FastAPI, HTTPException, Response, Request
from typing import List
from pydantic import ValidationError
from datetime import datetime
import calendar
import xml.etree.ElementTree as ET
from services.distribution import generate_transaction_schedule
from schemas import DistributionRequest, DistributionResponse
from tally_schemas import TallyDistributionResponse, TallyTransactionEntry
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Financial Distribution Engine")

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
    Endpoint for Tally Prime TDL Collection with RemoteURL + RemoteRequest.

    Tally sends:
        <ENVELOPE>
          <REQUEST>
            <total_amount>100000</total_amount>
            <months>12</months>
            <financial_year_start>April</financial_year_start>
          </REQUEST>
        </ENVELOPE>

    CRITICAL — Response must be EXACTLY this structure:
        <RESPONSE>
          <STATUS>1</STATUS>
          <ITEM><MONTH>April 2025</MONTH><DATE>01-04-2025</DATE><AMOUNT>8333.33</AMOUNT></ITEM>
          <ITEM>...</ITEM>
        </RESPONSE>

    Rules:
      - Root tag must be RESPONSE
      - ITEM must be DIRECT children of RESPONSE (NOT nested under DATA or any wrapper)
      - NO XML declaration line (no <?xml version...?>)
      - NO pretty printing / indentation (Tally parser is strict)
      - media_type must be text/xml
    """
    try:
        body = await request.body()
        body_str = body.decode("utf-8", errors="ignore").strip()
        print(f"[Tally XML] Received body:\n{body_str}")

        if not body_str:
            raise ValueError("Empty request body received from Tally")

        root = ET.fromstring(body_str)

        def find_text(tag):
            el = root.find(f".//{tag}")
            return el.text.strip() if el is not None and el.text else None

        total_amount_str     = find_text("total_amount")
        months_str           = find_text("months")
        financial_year_start = find_text("financial_year_start")

        print(f"[Tally XML] Parsed: amount={total_amount_str}, months={months_str}, fy={financial_year_start}")

        if not total_amount_str or not months_str or not financial_year_start:
            raise ValueError(f"Missing required fields in XML. Got: {body_str}")

        total_amount = float(total_amount_str)
        months       = int(months_str)

        result = generate_transaction_schedule(
            total_amount=total_amount,
            months=months,
            financial_year_start=financial_year_start
        )

        # ── Build response XML ───────────────────────────────
        # CRITICAL: ITEM must be direct children of RESPONSE.
        # TDL Collection uses XMLObjectPath: ITEM : 1 : RESPONSE
        # DO NOT wrap items in <DATA> or any other tag.
        resp_root = ET.Element("RESPONSE")
        ET.SubElement(resp_root, "STATUS").text = "1"

        for month_block in result["monthly_distribution"]:
            for entry in month_block["entries"]:
                item = ET.SubElement(resp_root, "ITEM")
                ET.SubElement(item, "MONTH").text  = str(month_block["month"])
                ET.SubElement(item, "DATE").text   = str(entry["date"])
                ET.SubElement(item, "AMOUNT").text = str(round(entry["amount"], 2))

        # NO pretty printing. NO xml declaration. Plain flat string.
        xml_str = ET.tostring(resp_root, encoding="unicode", xml_declaration=False)
        print(f"[Tally XML] Sending response:\n{xml_str}")

        return Response(content=xml_str, media_type="text/xml")

    except Exception as e:
        print(f"[Tally XML] Error: {str(e)}")
        err_xml = f"<RESPONSE><STATUS>0</STATUS><MESSAGE>{str(e)}</MESSAGE></RESPONSE>"
        return Response(content=err_xml, media_type="text/xml", status_code=200)


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
