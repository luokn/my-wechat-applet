from ..deps import *

router = APIRouter()


@router.get("/me", response_model=schemas.IdentityUser)
async def query_me(me: models.User = Depends(authenticate)):
    return me


@router.put("/me")
async def update(
    *,
    form: schemas.UserUpdate,
    db: Session = Depends(get_db),
    user_crud: crud.UserCRUD = Depends(get_user_crud),
    current_user: models.User = Depends(authenticate),
):
    if form.username:
        user_crud.update(current_user.id, **form.dict(), username_words=" ".join(jieba.lcut_for_search(form.username)))
        db.execute(f"update public.user set username_tsvec = to_tsvector(username_words) where id = {current_user.id}")
        db.commit()
    else:
        user_crud.update(current_user.id, **form.dict())
    return {"msg": "ok"}


@router.get("/me/teams", response_model=Dict[str, List[schemas.Team]])
async def query_my_teams(me: models.User = Depends(authenticate)):
    return {"owned": me.owned_teams, "joined": me.joined_teams, "applied": me.applied_teams}


@router.post("/me/collections")
async def append_collection(
    competition_id: int,
    me: models.User = Depends(authenticate),
    db: Session = Depends(get_db),
    competition_crud: crud.CompetitionCRUD = Depends(get_competition_crud),
):
    competition = competition_crud.query(competition_id)
    if competition is None:
        raise HTTPException(status_code=400, detail="Competition not found")
    if competition in me.collections:
        raise HTTPException(status_code=400, detail="Already in collections")
    me.collections.append(competition)
    db.commit()
    return {"msg": "ok"}


@router.delete("/me/collections")
async def delete_collection(
    competition_id: int,
    me: models.User = Depends(authenticate),
    db: Session = Depends(get_db),
    competition_crud: crud.CompetitionCRUD = Depends(get_competition_crud),
):
    competition = competition_crud.query(competition_id)
    if competition is None:
        raise HTTPException(status_code=400, detail="Competition not found")
    if competition not in me.collections:
        raise HTTPException(status_code=400, detail="Not in collections")
    me.collections.remove(competition)
    db.commit()
    return {"msg": "ok"}


@router.get("/", response_model=List[schemas.IdentityUser])
async def query_multi(
    *,
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    user_crud: crud.UserCRUD = Depends(get_user_crud),
    current_user: models.User = Depends(authenticate),
):
    if search is not None and len(search) > 0:
        kwords = " | ".join(jieba.lcut(search))
        users = db.query(models.User).where(text(f"username_tsvec @@ to_tsquery('{kwords}') ")).all()
    else:
        users = db.query(models.User).all()
    return users


@router.get("/{user_id}", response_model=schemas.IdentityUser)
async def query_one(
    *,
    user: models.User = Depends(get_user),
    current_user: models.User = Depends(authenticate),
):
    return user


@router.put("/{user_id}")
async def update(
    *,
    form: schemas.UserUpdate,
    db: Session = Depends(get_db),
    user: models.User = Depends(get_user),
    user_crud: crud.UserCRUD = Depends(get_user_crud),
    current_superadmin: models.User = Depends(get_current_superadmin),
):
    if form.username:
        user_crud.update(user.id, **form.dict(), username_words=" ".join(jieba.lcut_for_search(form.username)))
        db.execute(f"update public.user set username_tsvec = to_tsvector(username_words) where id = {user.id}")
        db.commit()
    else:
        user_crud.update(user.id, **form.dict())
    return {"msg": "ok"}


@router.get("/{user_id}/teams", response_model=Dict[str, List[schemas.Team]])
async def query_teams(
    *,
    user: models.User = Depends(get_user),
    current_admin: models.User = Depends(get_current_admin),
):
    return {"owned": user.owned_teams, "joined": user.joined_teams, "applied": user.applied_teams}
