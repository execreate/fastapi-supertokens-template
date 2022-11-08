from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from api.dependencies.database import get_db
from fastapi import APIRouter, Depends, Response, status
from schemas import blog_post as blog_post_schemas
from core.pagination import LimitOffsetPaginationParams
from db.crud.blog_post import BlogPostCrud


router = APIRouter(
    prefix="/blog",
    tags=["Blog posts"],
)


@router.post("", status_code=201, response_model=blog_post_schemas.BlogPostSchema)
async def create_a_blog_post(
    blog_post: blog_post_schemas.InBlogPostSchema, db: AsyncSession = Depends(get_db)
):
    crud = BlogPostCrud(db)
    result = await crud.create(blog_post)
    await db.commit()
    return result


@router.get("", response_model=blog_post_schemas.PaginatedBlogPostSchema)
async def list_blog_posts(
    pagination: LimitOffsetPaginationParams = Depends(),
    db: AsyncSession = Depends(get_db),
):
    crud = BlogPostCrud(db)
    return await crud.get_paginated_list(pagination.limit, pagination.offset)


@router.get(
    "/{post_id}",
    response_model=blog_post_schemas.BlogPostSchema,
    responses={
        404: {
            "description": "Object not found",
        },
    },
)
async def retrieve_a_blog_post(
    post_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    crud = BlogPostCrud(db)
    return await crud.get_by_id(post_id)


@router.patch(
    "/{post_id}",
    response_model=blog_post_schemas.BlogPostSchema,
    responses={
        404: {
            "description": "Object not found",
        },
    },
)
async def update_a_blog_post(
    post_id: UUID,
    blog_post: blog_post_schemas.UpdateBlogPostSchema,
    db: AsyncSession = Depends(get_db),
):
    crud = BlogPostCrud(db)
    result = await crud.update_by_id(post_id, blog_post)
    await db.commit()
    return result


@router.delete(
    "/{post_id}",
    status_code=204,
    responses={
        404: {
            "description": "Object not found",
        },
    },
)
async def delete_a_blog_post(
    post_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    crud = BlogPostCrud(db)
    await crud.delete_by_id(post_id)
    await db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
