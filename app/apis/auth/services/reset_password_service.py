from apis.auth.utils.text_code_utils import generate_and_send_code_to_user
from db.models import User, UserRole
from db.session import get_db
from fastapi import APIRouter, Depends, HTTPException, status
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
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    if current_user.username != data.username:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="El username ingresado no coincide con la sesión actual"
        )
    
    user = db.query(User).filter(User.username == data.username).first()
    
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