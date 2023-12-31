from typing import Optional


from sqlalchemy.orm import Session
from sqlalchemy import select

from docubot.database.models import Tag
from docubot.schemas.tag import TagBase


async def get_tags(skip: int, limit: int, db: Session) -> list[Tag]:
    """
    The get_tags function returns a list of tags.

    :param skip: int: Skip a number of records
    :param limit: int: Limit the number of tags returned
    :param db: Session: Pass the database session to the function
    :return: A list of tag objects
    """
    tags = db.scalars(
        select(Tag)
        .offset(skip)
        .limit(limit)
    )

    return tags.all()  # noqa


async def get_tags_by_list_values(values: list[str], db: Session) -> list[Tag]:
    """
    The get_tags_by_list_values function takes a list of strings and a Session object as arguments.
    It returns a list of Tag objects that match the names in the values argument.

    :param values: list[str]: Pass in a list of strings to the function
    :param db: Session: Pass in the database session
    :return: A list of tag objects
    """
    tags = db.scalars(
        select(Tag)
        .filter(Tag.name.in_(values))
    )
    return tags.all()  # noqa


async def get_tag_by_id(tag_id: int, db: Session) -> Optional[Tag]:
    """
    The get_tag_by_id function returns a Tag object from the database.

    :param tag_id: int: Specify the id of the tag to be retrieved
    :param db: Session: Pass the database session to the function
    :return: A tag object or none
    """
    return db.scalar(
        select(Tag)
        .filter(Tag.id == tag_id)
    )


async def get_or_create_tags(values: list[str], db: Session) -> list[Tag]:
    """
    The get_or_create_tags function takes a list of strings and  database session.
    It returns a list of Tag objects.
    If the tag already exists in the database, it is returned as-is. If not, it is created and then returned.

    :param values: list[str]: Pass in a list of strings
    :param db: Session: Pass the database session to the function
    :return: A list of tag objects
    """
    tags = await get_tags_by_list_values(values, db)
    new_tags = []

    for value in values:
        for tag in tags:
            if value == tag.name:
                break
        else:
            new_tags.append(Tag(name=value.strip()))  
             
    if new_tags:
        db.add_all(new_tags)

        db.commit()
        for new_tag in new_tags:
            db.refresh(new_tag)

    tags.extend(new_tags)

    return tags


async def update_tag(tag_id: int, body: TagBase, db: Session) -> Optional[Tag]:
    """
    The update_tag function updates a tag in the database.

    :param tag_id: int: Specify the id of the tag to be deleted
    :param body: TagBase: Pass in the new name of the tag
    :param db: Session: Pass a database session to the function
    :return: The updated tag if found, otherwise none
    """
    tag = await get_tag_by_id(tag_id, db)

    if tag:
        tag.name = body.name
        db.commit()
        db.refresh(tag)

    return tag


async def remove_tag(tag_id: int, db: Session) -> Optional[Tag]:
    """
    The remove_tag function removes a tag from the database.

    :param tag_id: int: Specify the id of the tag to remove
    :param db: Session: Pass in the database session
    :return: The tag that was removed, or none if the tag wasn't found
    """
    tag = await get_tag_by_id(tag_id, db)

    if tag:
        db.delete(tag)
        db.commit()

    return tag


def get_list_tags(tags) -> list[str]:
    set_tags = set()
    if isinstance(tags, list):
        for tag in tags:
            set_tags.update({_tag.strip() for _tag in tag.split(',') if tag.strip()})
    elif isinstance(tags, str):
        set_tags = {tag.strip() for tag in tags.split(',')}
    
    return list(set_tags)
