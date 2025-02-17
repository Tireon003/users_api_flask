from flask import Blueprint, make_response, Response, jsonify
from flask_pydantic import validate

from app.src.core import db
from app.src.exceptions import (
    UserNotFoundException,
    UserAlreadyExistsException,
)
from app.src.repositories import UserRepository
from app.src.schemas.entities import (
    UserFromDB,
    UserUpdate,
    UserCreate,
)
from app.src.schemas.query import UserPaginatorQueryParams

router = Blueprint(
    name="users_router",
    import_name=__name__,
    url_prefix="/api/users",
)


@router.get("/")
@validate()  # type: ignore[misc]
def get_all_users(query: UserPaginatorQueryParams) -> Response:
    """
    Endpoint for getting all users. Pagination is optional.
    :return: list of users
    """
    repo = UserRepository(db)
    users_list = repo.get_all(query)
    users_dto_list = [UserFromDB.model_validate(usr) for usr in users_list]
    return make_response(
        jsonify([usr.to_dict() for usr in users_dto_list]),
        200,
    )


@router.get("/<int:id>/")
def get_user(id: int) -> Response:
    """
    Endpoint for getting user by id.
    :param id: user id
    :return: user
    """
    repo = UserRepository(db)
    try:
        user = repo.get_one(id)
    except UserNotFoundException as exc:
        err_body = {"error": str(exc)}
        return make_response(
            jsonify(err_body),
            404,
        )
    user_dto = UserFromDB.model_validate(user)
    return make_response(
        jsonify(user_dto.to_dict()),
        200,
    )


@router.post("/")
@validate()  # type: ignore[misc]
def create_user(body: UserCreate) -> Response:
    repo = UserRepository(db)
    try:
        created_user = repo.create(body)
        user_dto = UserFromDB.model_validate(created_user)
        return make_response(
            jsonify(user_dto.to_dict()),
            201,
        )
    except UserAlreadyExistsException as exc:
        err_body = {"error": str(exc)}
        return make_response(
            jsonify(err_body),
            404,
        )


@router.patch("/<int:id>/")
@validate()  # type: ignore[misc]
def update_user(id: int, body: UserUpdate) -> Response:
    repo = UserRepository(db)
    try:
        updated_user = repo.update(id=id, data=body)
        user_dto = UserFromDB.model_validate(updated_user)
        return make_response(
            jsonify(user_dto.to_dict()),
            200,
        )
    except UserNotFoundException as exc:
        err_body = {"error": str(exc)}
        return make_response(
            jsonify(err_body),
            404,
        )


@router.delete("/<int:id>/")
def delete_user(id: int) -> Response:
    repo = UserRepository(db)
    try:
        repo.delete(id)
        return make_response(
            jsonify({"message": f"User with id {id} deleted"}),
            200,
        )
    except UserNotFoundException as exc:
        err_body = {"error": str(exc)}
        return make_response(
            jsonify(err_body),
            404,
        )
