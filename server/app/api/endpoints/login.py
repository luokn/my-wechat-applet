from ..deps import *

router = APIRouter()


@router.post("/access-token", response_model=schemas.Token)
async def login(
    *,
    form: schemas.Login = Depends(schemas.Login.form),
    user_crud: crud.UserCRUD = Depends(get_user_crud),
):
    if form.grant_type == "password":
        if form.username == "test" and form.password == settings.TEST_PASSWORD:
            return {"token_type": "Bearer", "access_token": encode_token({"sub": "1"})}
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Password wrong.")
    if form.grant_type == "code":
        if form.code is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid params.")
        params = {
            "appid": settings.APP_ID,
            "secret": settings.APP_SECRET,
            "js_code": form.code,
            "grant_type": "authorization_code",
        }
        obj = requests.get("https://api.weixin.qq.com/sns/jscode2session", params=params).json()
        if "openid" not in obj:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Wechat api error.")
        user = user_crud.query_by_openid(obj["openid"])
        if user is None:
            if form.username is None or form.avatar is None:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid params.")
            user = user_crud.create(
                **form.dict(include={"username", "avatar"}), openid=obj["openid"], is_admin=False, is_superadmin=False
            )
        else:
            update = form.dict(include={"username", "avatar"}, exclude_none=True)
            if len(update) != 0:
                user_crud.update(user.id, **update)
        return {"token_type": "Bearer", "access_token": encode_token({"sub": str(user.id)})}
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unsupported grant type.")
