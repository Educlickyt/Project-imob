from fastapi import APIRouter, Depends, HTTPException, status
from app.modules.users.schemas import UserCreate, UserResponse
from app.modules.users.service import UserService
from app.modules.auth.dependencies import get_current_user
from app.modules.users.models import User

from sqlalchemy.orm import Session
from app.core.dependencies import get_db

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserResponse, status_code=201)
def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Cria um novo usuário vinculado ao tenant do usuário autenticado.
    Requer autenticação.
    """
    user_service = UserService(db)
    return user_service.create_user(user_data, current_user.tenant_id)