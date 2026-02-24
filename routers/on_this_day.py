from fastapi import Response, APIRouter
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
        return Response(
            content=f"Error: {response.text}",
            status_code=response.status_code,
            media_type="text/plain"
        )

    return Response(
        content=response.content,
        media_type="application/json",
        headers={
            "Cache-Control": "public, max-age=86400",
            "X-Attribution": "Historical data provided by ZenQuotes.io"
        }
    )