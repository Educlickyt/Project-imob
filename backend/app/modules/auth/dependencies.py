# from fastapi import Depends, HTTPException, status
# from fastapi.security import OAuth2PasswordBearer
# import jwt
# from app.core.config import settings
# from app.modules.auth.schemas import TokenPayload

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# def get_current_user(token: str = Depends(oauth2_scheme)):
#     try:
#         payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
#         token_data = TokenPayload(**payload)
#     except (jwt.PyJWTError, ValueError):
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="Não foi possível validar as credenciais",
#         )
    
#     # Aqui você buscaria o usuário no banco se necessário
#     # user = db.query(User).filter(User.id == token_data.sub).first()
#     return token_data.sub # Retorna o ID do usuário para a rota