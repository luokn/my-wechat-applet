from typing import Dict, Generator, List, Optional

import jieba
import requests
from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import text
from sqlalchemy.orm import Session

from .. import crud, models, schemas
from ..core import decode_token, encode_token, settings
from ..db import SessionLocal

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl=f"/api/login/access-token")


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_comment_crud(db: Session = Depends(get_db)) -> crud.CommentCRUD:
    return crud.CommentCRUD(db)


def get_competition_crud(db: Session = Depends(get_db)) -> crud.CompetitionCRUD:
    return crud.CompetitionCRUD(db)


def get_reply_crud(db: Session = Depends(get_db)) -> crud.ReplyCRUD:
    return crud.ReplyCRUD(db)


def get_team_crud(db: Session = Depends(get_db)) -> crud.TeamCRUD:
    return crud.TeamCRUD(db)


def get_user_crud(db: Session = Depends(get_db)) -> crud.UserCRUD:
    return crud.UserCRUD(db)


def get_excellent_crud(db: Session = Depends(get_db)) -> crud.ExcellentCRUD:
    return crud.ExcellentCRUD(db)


def get_user(
    *,
    user_id: int = Path(...),
    user_crud: crud.UserCRUD = Depends(get_user_crud),
) -> models.User:
    user = user_crud.query(user_id)
    if user is not None:
        return user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not exist.")


def get_competition(
    *,
    competition_id: int = Path(...),
    competition_crud: crud.CompetitionCRUD = Depends(get_competition_crud),
) -> models.Competition:
    competition = competition_crud.query(competition_id)
    if competition is not None:
        return competition
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Competition not found.")


def get_team(
    *,
    team_id: int = Path(...),
    team_crud: crud.TeamCRUD = Depends(get_team_crud),
) -> models.Team:
    team = team_crud.query(team_id)
    if team is not None:
        return team
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team not found.")


def get_comment(
    *,
    comment_id: int = Path(...),
    comment_crud: crud.CommentCRUD = Depends(get_comment_crud),
) -> models.Comment:
    team = comment_crud.query(comment_id)
    if team is not None:
        return team
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found.")


def get_excellent(
    *,
    excellent_id: int = Path(...),
    excellent_crud: crud.ExcellentCRUD = Depends(get_excellent_crud),
) -> models.Excellent:
    excellent = excellent_crud.query(excellent_id)
    if excellent is not None:
        return excellent
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Excellent not found.")


def authenticate(
    *,
    token: str = Depends(reusable_oauth2),
    user_crud: crud.UserCRUD = Depends(get_user_crud),
) -> models.User:
    claims = decode_token(token)
    if claims is not None:
        current_user = user_crud.query(int(claims["sub"]))
        if current_user is not None:
            return current_user
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication failed.")


def get_current_admin(
    *,
    current_user: models.User = Depends(authenticate),
) -> models.User:
    if current_user.is_admin or current_user.is_superadmin:
        return current_user
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied.")


def get_current_superadmin(
    *,
    current_user: models.User = Depends(authenticate),
) -> models.User:
    if current_user.is_superadmin:
        return current_user
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied.")


def get_current_captain_or_admin(
    *,
    team: models.Team = Depends(get_team),
    current_user: models.User = Depends(authenticate),
) -> models.User:
    if current_user.id == team.captain_id or current_user.is_admin or current_user.is_superadmin:
        return current_user
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied.")
