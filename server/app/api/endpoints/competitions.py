from fastapi import Query
from ..deps import *

router = APIRouter()


@router.post("/")
async def create(
    *,
    form: schemas.CompetitionCreate,
    db: Session = Depends(get_db),
    competition_crud: crud.CompetitionCRUD = Depends(get_competition_crud),
    current_admin: models.User = Depends(get_current_admin),
):
    competition = competition_crud.create(**form.dict(), title_words=" ".join(jieba.lcut_for_search(form.title)))
    db.execute(f"update public.competition set title_tsvec = to_tsvector(title_words) where id = {competition.id}")
    db.commit()
    return {"msg": "ok"}


@router.get("/", response_model=List[schemas.Competition])
async def query_multi(
    *,
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(authenticate),
):
    if search is not None and len(search) > 0:
        kwords = " | ".join(jieba.lcut_for_search(search))
        competitions = db.query(models.Competition).where(text(f"title_tsvec @@ to_tsquery('{kwords}') ")).all()
    else:
        competitions = db.query(models.Competition).all()
    return competitions


@router.get("/{competition_id}", response_model=schemas.Competition)
async def query_one(
    *,
    competition: models.Competition = Depends(get_competition),
    current_user: models.User = Depends(authenticate),
):
    return competition


@router.delete("/{competition_id}")
async def delete(
    *,
    competition: models.Competition = Depends(get_competition),
    competition_crud: crud.CompetitionCRUD = Depends(get_competition_crud),
    current_admin: models.User = Depends(get_current_admin),
):
    competition_crud.delete(competition.id)
    return {"msg": "ok"}


import jieba


@router.put("/{competition_id}")
async def update(
    *,
    form: schemas.CompetitionUpdate,
    db: Session = Depends(get_db),
    competition: models.Competition = Depends(get_competition),
    competition_crud: crud.CompetitionCRUD = Depends(get_competition_crud),
    current_admin: models.User = Depends(get_current_admin),
):
    update = form.dict(exclude_none=True)
    if len(update) != 0:
        if form.title:
            competition_crud.update(competition.id, **update, title_words=" ".join(jieba.lcut_for_search(form.title)))
            db.execute(
                f"update public.competition set title_tsvec = to_tsvector(title_words) where id = {competition.id}"
            )
            db.commit()
        else:
            competition_crud.update(competition.id, **update)
    return {"msg": "ok"}


@router.get("/{competition_id}/teams", response_model=List[schemas.Team])
async def query_teams(
    *,
    skip: int = 0,
    limit: int = 100,
    competition: models.Competition = Depends(get_competition),
    current_user: models.User = Depends(authenticate),
):
    return competition.teams.offset(skip).limit(limit).all()


@router.post("/{competition_id}/teams")
async def create_team(
    *,
    form: schemas.TeamCreate,
    db: Session = Depends(get_db),
    competition: models.Competition = Depends(get_competition),
    team_crud: crud.TeamCRUD = Depends(get_team_crud),
    current_user: models.User = Depends(authenticate),
):
    team = team_crud.create(
        **form.dict(),
        captain_id=current_user.id,
        competition_id=competition.id,
        name_words=" ".join(jieba.lcut_for_search(form.name)),
    )
    db.execute(f"update public.team set name_tsvec = to_tsvector(name_words) where id = {team.id}")
    db.commit()
    return {"msg": "ok"}


@router.post("/{competition_id}/comments")
async def create_comment(
    *,
    form: schemas.CommentCreate,
    competition: models.Competition = Depends(get_competition),
    comment_crud: crud.CommentCRUD = Depends(get_comment_crud),
    current_user: models.User = Depends(authenticate),
):
    comment_crud.create(**form.dict(), user_id=current_user.id, competition_id=competition.id)
    return {"msg": "ok"}


@router.get("/{competition_id}/comments", response_model=List[schemas.Comment])
async def query_comments(
    *,
    skip: int = 0,
    limit: int = 100,
    competition: models.Competition = Depends(get_competition),
    current_user: models.User = Depends(authenticate),
):
    return competition.comments.offset(skip).limit(limit).all()
