"""
This module contains tools for managing Trello cards.
"""

import logging
from typing import List

from mcp.server.fastmcp import Context

from server.models import TrelloCard, TrelloComment
from server.services.card import CardService
...
async def delete_card(ctx: Context, card_id: str) -> dict:
    """Deletes a card.

    Args:
        card_id (str): The ID of the card to delete.

    Returns:
        dict: The response from the delete operation.
    """
    try:
        logger.info(f"Deleting card: {card_id}")
        result = await service.delete_card(card_id)
        logger.info(f"Successfully deleted card: {card_id}")
        return result
    except Exception as e:
        error_msg = f"Failed to delete card: {str(e)}"
        logger.error(error_msg)
        await ctx.error(error_msg)
        raise


async def get_card_comments(ctx: Context, card_id: str) -> List[TrelloComment]:
    """Retrieves all comments for a specific card.

    Args:
        card_id (str): The ID of the card to get comments for.

    Returns:
        List[TrelloComment]: A list of comment objects.
    """
    try:
        logger.info(f"Getting comments for card: {card_id}")
        result = await service.get_card_comments(card_id)
        logger.info(f"Successfully retrieved {len(result)} comments for card: {card_id}")
        return result
    except Exception as e:
        error_msg = f"Failed to get comments: {str(e)}"
        logger.error(error_msg)
        await ctx.error(error_msg)
        raise


async def add_comment_to_card(ctx: Context, card_id: str, text: str) -> TrelloComment:
    """Adds a new comment to a card.

    Args:
        card_id (str): The ID of the card to add the comment to.
        text (str): The text content of the comment.

    Returns:
        TrelloComment: The created comment object.
    """
    try:
        logger.info(f"Adding comment to card: {card_id}")
        result = await service.add_comment_to_card(card_id, text)
        logger.info(f"Successfully added comment to card: {card_id}")
        return result
    except Exception as e:
        error_msg = f"Failed to add comment: {str(e)}"
        logger.error(error_msg)
        await ctx.error(error_msg)
        raise
