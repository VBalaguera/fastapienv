from fastapi            import Depends, HTTPException, status
from fastapi.security   import HTTPBearer, HTTPAuthorizationCredentials
from firebase_admin     import auth

bearer = HTTPBearer()

async def get_current_user(
    creds: HTTPAuthorizationCredentials = Depends(bearer),
) -> dict:
    try:
        decoded = auth.verify_id_token(creds.credentials)
        return decoded
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )