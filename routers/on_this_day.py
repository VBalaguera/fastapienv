from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
import httpx

router = APIRouter(
    prefix="/on_this_day",
    tags=["On This Day"]
)


@router.get("/events/{month}/{day}")
async def get_on_this_day_events(month: str, day: str):
    url = f"https://today.zenquotes.io/api/{month}/{day}"
    headers = {
        "User-Agent": "SatelliteAPI/1.0 (https://swissblade.vercel.app)",
        "Accept": "application/json"
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, follow_redirects=True, timeout=10.0)

    if response.status_code != 200:
        return JSONResponse(
            status_code=response.status_code,
            content={"error": "Could not fetch data from ZenQuotes"}
        )

    full_data = response.json()

    clean_data = full_data.get("data", {})

    return JSONResponse(
        content=clean_data,
        headers={
            "Cache-Control": "public, max-age=86400",
            "X-Attribution": "Historical data provided by ZenQuotes.io"
        }
    )