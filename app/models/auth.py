from sqlmodel import SQLModel


class TokenPayload(SQLModel):
    sub: int | None = None
