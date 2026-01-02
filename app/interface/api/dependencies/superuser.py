from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from app.config import settings

security_basic = HTTPBasic()

def verify_superuser_credentials(credentials: HTTPBasicCredentials = Depends(security_basic)):
    if (credentials.username != settings.superuser_username or 
        credentials.password != settings.superuser_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid superuser credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials