from ..deps import *

router = APIRouter()


@router.post("/")
async def create(
    *,
    form: schemas.ExcellentCreate,
    excellent_crud: crud.ExcellentCRUD = Depends(get_excellent_crud),
    current_admin: models.User = Depends(get_current_admin),
):
    excellent = excellent_crud.create(**form.dict())
    return {"msg": "ok"}


@router.get("/", response_model=List[schemas.Excellent])
async def query_multi(
    *,
    excellent_crud: crud.ExcellentCRUD = Depends(get_excellent_crud),
    current_admin: models.User = Depends(get_current_admin),
):
    excellents = excellent_crud.query_multi()
    return excellents


@router.get("/{excellent_id}", response_model=schemas.Excellent)
async def query_one(
    *,
    excellent: models.Excellent = Depends(get_excellent),
    current_user: models.User = Depends(authenticate),
):
    return excellent


@router.delete("/{excellent_id}")
async def delete(
    *,
    excellent: models.Excellent = Depends(get_excellent),
    excellent_crud: crud.ExcellentCRUD = Depends(get_excellent_crud),
    current_captain_or_admin: models.User = Depends(get_current_captain_or_admin),
):
    excellent_crud.delete(excellent.id)
    return {"msg": "ok"}


@router.put("/{excellent_id}")
async def update(
    *,
    form: schemas.ExcellentUpdate,
    excellent: models.Excellent = Depends(get_excellent),
    excellent_crud: crud.ExcellentCRUD = Depends(get_excellent_crud),
    current_admin: models.User = Depends(get_current_admin),
):
    excellent_crud.update(excellent.id, **form.dict(exclude_none=True))
    return {"msg": "ok"}
