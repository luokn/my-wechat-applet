from ..deps import *

router = APIRouter()


@router.get("/", response_model=List[schemas.Team])
async def query_multi(
    *,
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    team_crud: crud.TeamCRUD = Depends(get_team_crud),
    current_admin: models.User = Depends(get_current_admin),
):
    if search is not None and len(search) > 0:
        kwords = " | ".join(jieba.lcut_for_search(search))
        teams = db.query(models.Team).where(text(f"name_tsvec @@ to_tsquery('{kwords}') ")).all()
    else:
        teams = db.query(models.Team).all()
    return teams


@router.get("/{team_id}", response_model=schemas.Team)
async def query_one(
    *,
    team: models.Team = Depends(get_team),
    current_user: models.User = Depends(authenticate),
):
    return team


@router.delete("/{team_id}")
async def delete(
    *,
    team: models.Team = Depends(get_team),
    team_crud: crud.TeamCRUD = Depends(get_team_crud),
    current_captain_or_admin: models.User = Depends(get_current_captain_or_admin),
):
    team_crud.delete(team.id)
    return {"msg": "ok"}


@router.put("/{team_id}")
async def update(
    *,
    form: schemas.TeamUpdate,
    db: Session = Depends(get_db),
    team: models.Team = Depends(get_team),
    team_crud: crud.TeamCRUD = Depends(get_team_crud),
    current_captain_or_admin: models.User = Depends(get_current_captain_or_admin),
):
    update = form.dict(exclude_none=True)
    if len(update) != 0:
        team_crud.update(
            team.id,
            **update,
            name_words=" ".join(jieba.lcut_for_search(form.name)),
        )
        db.execute(f"update public.team set name_tsvec = to_tsvector(name_words) where id = {team.id}")
        db.commit()
    return {"msg": "ok"}


@router.get("/{team_id}/members", response_model=List[schemas.User])
async def query_members(
    *,
    team: models.Team = Depends(get_team),
    current_user: models.User = Depends(authenticate),
):
    return team.members


@router.get("/{team_id}/applicants", response_model=List[schemas.User])
async def query_applicants(
    *,
    team: models.Team = Depends(get_team),
    current_user: models.User = Depends(authenticate),
):
    return team.applicants


@router.post("/{team_id}/members")
async def append_member(
    *,
    user_id: int,
    db: Session = Depends(get_db),
    team: models.Team = Depends(get_team),
    user_crud: crud.UserCRUD = Depends(get_user_crud),
    current_captain_or_admin: models.User = Depends(get_current_captain_or_admin),
):
    user = user_crud.query(user_id)
    if (
        user is not None
        and user_id != team.captain_id
        and len(team.members) < 10
        and all([user_id != u.id for u in team.members])
    ):
        team.members.append(user)
        db.commit()
        return {"msg": "ok"}
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Not allowed.")


@router.post("/{team_id}/applicants")
async def append_applicant(
    *,
    team: models.Team = Depends(get_team),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(authenticate),
):
    if (
        current_user.id != team.captain_id
        and all([current_user.id != u.id for u in team.members])
        and all([current_user.id != u.id for u in team.applicants])
    ):
        team.applicants.append(current_user)
        db.commit()
        return {"msg": "ok"}
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Not allowed.")


@router.delete("/{team_id}/members")
async def remove_member(
    *,
    user_id: int,
    db: Session = Depends(get_db),
    team: models.Team = Depends(get_team),
    user_crud: crud.UserCRUD = Depends(get_user_crud),
    current_captain_or_admin: models.User = Depends(get_current_captain_or_admin),
):
    user = user_crud.query(user_id)
    if user is not None and any([user_id == u.id for u in team.members]):
        team.members.remove(user)
        db.commit()
    return {"msg": "ok"}


@router.delete("/{team_id}/applicants")
async def remove_applicant(
    *,
    user_id: int,
    approve: bool = False,
    db: Session = Depends(get_db),
    team: models.Team = Depends(get_team),
    user_crud: crud.UserCRUD = Depends(get_user_crud),
    current_captain_or_admin: models.User = Depends(get_current_captain_or_admin),
):
    user = user_crud.query(user_id)
    if user is not None and any([user_id == u.id for u in team.applicants]):
        team.applicants.remove(user)
        if approve:
            team.members.append(user)
        db.commit()
    return {"msg": "ok"}
