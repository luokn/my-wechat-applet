from ..deps import *

router = APIRouter()


@router.get("/{comment_id}", response_model=schemas.Comment)
async def query(
    *,
    comment: models.Comment = Depends(get_comment),
    current_user: models.User = Depends(authenticate),
):
    return comment


@router.delete("/{comment_id}")
async def delete(
    *,
    comment: models.Comment = Depends(get_comment),
    comment_crud: crud.CommentCRUD = Depends(get_comment_crud),
    current_user: models.User = Depends(authenticate),
):
    if current_user.is_admin or current_user.is_superadmin or comment.user_id == current_user.id:
        comment_crud.delete(comment.id)
        return {"msg": "ok"}
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not allowed to delete this comment.")


@router.get("/{comment_id}/replies", response_model=List[schemas.Reply])
async def query_replies(
    *,
    comment: models.Comment = Depends(get_comment),
    current_user: models.User = Depends(authenticate),
):
    return comment.replies


@router.post("/{comment_id}/replies")
async def create_reply(
    *,
    form: schemas.ReplyCreate,
    comment: models.Comment = Depends(get_comment),
    reply_crud: crud.ReplyCRUD = Depends(get_reply_crud),
    current_user: models.User = Depends(authenticate),
):
    reply_crud.create(**form.dict(), user_id=current_user.id, comment_id=comment.id)
    return {"msg": "ok"}
