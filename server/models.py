from typing import List

from pydantic import BaseModel


class TrelloBoard(BaseModel):
    """Model representing a Trello board."""

    id: str
    name: str
    desc: str | None = None
    closed: bool = False
    idOrganization: str | None = None
    url: str


class TrelloList(BaseModel):
    """Model representing a Trello list."""

    id: str
    name: str
    closed: bool = False
    idBoard: str
    pos: float


class TrelloLabel(BaseModel):
    """Model representing a Trello label."""
    
    id: str
    name: str
    color: str | None = None


class TrelloCard(BaseModel):
    """Model representing a Trello card."""

    id: str
    name: str
    desc: str | None = None
    closed: bool = False
    idList: str
    idBoard: str
    url: str
    pos: float
    labels: List[TrelloLabel] = []
    due: str | None = None
    comments: List['TrelloComment'] = []


class TrelloCommentData(BaseModel):
    """Model representing the data inside a Trello comment."""

    text: str


class TrelloMemberCreator(BaseModel):
    """Model representing the creator of a Trello action/comment."""

    id: str
    fullName: str
    username: str


class TrelloComment(BaseModel):
    """Model representing a Trello comment (action)."""

    id: str
    data: TrelloCommentData
    date: str
    memberCreator: TrelloMemberCreator
