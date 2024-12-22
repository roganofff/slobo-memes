from starlette.requests import Request
from starlette.responses import Response

from bot.src.api import router


@router.get("/healthcheck")
async def healthcheck(request: Request) -> Response:
    return Response("Healthy", status_code=200)
