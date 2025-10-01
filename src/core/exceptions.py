from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from authx.exceptions import MissingTokenError, RevokedTokenError, InvalidToken

app = FastAPI()


@app.exception_handler((MissingTokenError, RevokedTokenError, InvalidToken))
async def authx_exception_handler(request: Request, exc: Exception):
    if isinstance(exc, MissingTokenError):
        return JSONResponse(
            status_code=401,
            content={"detail": "Authentication token is missing"}
        )
    elif isinstance(exc, RevokedTokenError):
        return JSONResponse(
            status_code=401,
            content={"detail": "Authentication token has expired"}
        )
    elif isinstance(exc, InvalidToken):
        return JSONResponse(
            status_code=403,
            content={"detail": "Invalid authentication token"}
        )
    else:
        return JSONResponse(
            status_code=401,
            content={"detail": "Authentication failed"}
        )
