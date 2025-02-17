from pydantic import (
    BaseModel,
    Field,
    ConfigDict,
)


class UserPaginatorQueryParams(BaseModel):
    """
    Pagination query params validation schema.
    By default, offset = 0 and items = 5.
    The maximum number of records is set to 1000.
    """

    offset: int = Field(ge=0, default=0)
    limit: int = Field(default=5, le=1000)

    model_config = ConfigDict(extra="forbid")
