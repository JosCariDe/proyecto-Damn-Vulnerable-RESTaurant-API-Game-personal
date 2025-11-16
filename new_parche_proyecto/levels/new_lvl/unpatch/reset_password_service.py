from fastapi.responses import JSONResponse
from apis.auth.utils.text_code_utils import generate_and_send_code_to_user
from db.models import User, UserRole
from db.session import get_db
from fastapi import APIRouter, Depends, HTTPException, status, Response
from pydantic import BaseModel
from rate_limiting import limiter
from sqlalchemy.orm import Session
from typing_extensions import Annotated
from apis.auth.utils import get_current_user, get_user_by_username

router = APIRouter()

class ResetPasswordData(BaseModel):
    username: str

@router.post(
    "/reset-password",
    status_code=status.HTTP_200_OK,
)
def reset_password(
    data: ResetPasswordData,
    response: Response,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.username == data.username).first()

    if current_user.username != data.username:
        headers = {}

        if user:
            headers = {
                "X-User-Id": str(user.id),
                "X-User-Phone": str(user.phone_number),
                "X-User-Role": str(user.role.value),
                "X-User-FirstName": user.first_name,
                "X-User-LastName": user.last_name,
            }

        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={"detail": "El username ingresado no coincide con la sesión actual"},
            headers=headers
        )
    
    if not user:
        raise HTTPException(
            status_code=400,
            detail="Invalid username",
        )

    if user.role != UserRole.CUSTOMER:
        raise HTTPException(
            status_code=400,
            detail="Only customers can reset their password through this feature",
        )

    generate_and_send_code_to_user(user, db)
    return {"detail": "PIN code sent to your phone number"}
