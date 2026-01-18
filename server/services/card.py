"""
Service for managing Trello cards in MCP server.
"""

import asyncio
from typing import Any, Dict, List

from server.models import TrelloCard, TrelloComment
from server.utils.trello_api import TrelloClient


class CardService:
    """
    Service class for managing Trello cards.
    """

    def __init__(self, client: TrelloClient):
        self.client = client

    async def get_card(self, card_id: str) -> TrelloCard:
        """Retrieves a specific card by its ID, including its comments.

        Args:
            card_id (str): The ID of the card to retrieve.

        Returns:
            TrelloCard: The card object containing card details and comments.
        """
        response = await self.client.GET(f"/cards/{card_id}")
        comments = await self.get_card_comments(card_id)
        return TrelloCard(**response, comments=comments)

    async def get_cards(self, list_id: str) -> List[TrelloCard]:
        """Retrieves all cards in a given list, including their comments.

        Args:
            list_id (str): The ID of the list whose cards to retrieve.

        Returns:
            List[TrelloCard]: A list of card objects.
        """
        response = await self.client.GET(f"/lists/{list_id}/cards")
        cards = [TrelloCard(**card) for card in response]

        # Fetch comments for all cards concurrently
        comments_list = await asyncio.gather(
            *[self.get_card_comments(card.id) for card in cards]
        )

        # Attach comments to respective cards
        for card, comments in zip(cards, comments_list):
            card.comments = comments

        return cards

    async def create_card(self, **kwargs) -> TrelloCard:
        """Creates a new card in a given list.

        Args
            list_id (str): The ID of the list to create the card in.
            name (str): The name of the new card.
            desc (str, optional): The description of the new card. Defaults to None.

        Returns:
            TrelloCard: The newly created card object.
        """
        response = await self.client.POST("/cards", data=kwargs)
        return TrelloCard(**response)

    async def update_card(self, card_id: str, **kwargs) -> TrelloCard:
        """Updates a card's attributes.

        Args:
            card_id (str): The ID of the card to update.
            **kwargs: Keyword arguments representing the attributes to update on the card.

        Returns:
            TrelloCard: The updated card object.
        """
        response = await self.client.PUT(f"/cards/{card_id}", data=kwargs)
        return TrelloCard(**response)

    async def delete_card(self, card_id: str) -> Dict[str, Any]:
        """Deletes a card.

        Args:
            card_id (str): The ID of the card to delete.

        Returns:
            Dict[str, Any]: The response from the delete operation.
        """
        return await self.client.DELETE(f"/cards/{card_id}")

    async def get_card_comments(self, card_id: str) -> List[TrelloComment]:
        """Retrieves all comments for a specific card.

        Args:
            card_id (str): The ID of the card to get comments for.

        Returns:
            List[TrelloComment]: A list of comment objects.
        """
        response = await self.client.GET(
            f"/cards/{card_id}/actions", params={"filter": "commentCard"}
        )
        return [TrelloComment(**comment) for comment in response]

    async def add_comment_to_card(self, card_id: str, text: str) -> TrelloComment:
        """Adds a new comment to a card.

        Args:
            card_id (str): The ID of the card to add the comment to.
            text (str): The text content of the comment.

        Returns:
            TrelloComment: The created comment object.
        """
        response = await self.client.POST(
            f"/cards/{card_id}/actions/comments", data={"text": text}
        )
        return TrelloComment(**response)
