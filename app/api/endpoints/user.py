from app.core.user import fastapi_users
from app.schemas.user import UserRead, UserUpdate

router = fastapi_users.get_users_router(UserRead, UserUpdate)
router.routes = [
    route for route in router.routes if route.name != "users:delete_user"
]
