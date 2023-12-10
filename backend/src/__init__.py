from fastapi import APIRouter

from .user import router as user_router

_route_list: list = [user_router]

routes: APIRouter = APIRouter()

for route in _route_list:
    if hasattr(route, "router"):
        routes.include_router(route.router)
    else:
        raise AttributeError(f"Router not found in {route}")
