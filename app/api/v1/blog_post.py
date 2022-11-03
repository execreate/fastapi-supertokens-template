from uuid import UUID
from fastapi import APIRouter, Depends
from schemas import blog_post as blog_post_schemas
from core.pagination import LimitOffsetPaginationParams


router = APIRouter(
    prefix="/blog",
    tags=["Blog posts"],
)


@router.post("", response_model=blog_post_schemas.BlogPostSchema)
async def create_a_blog_post(blog_post: blog_post_schemas.InBlogPostSchema):
    return None


@router.get("", response_model=blog_post_schemas.PaginatedBlogPostSchema)
async def list_blog_posts(
    pagination=Depends(LimitOffsetPaginationParams),
):
    return None


@router.get("/{post_id}", response_model=blog_post_schemas.BlogPostSchema)
async def retrieve_a_blog_post(post_id: UUID):
    return None


@router.delete("/{post_id}", response_model=blog_post_schemas.BlogPostSchema)
async def delete_a_blog_post(post_id: UUID):
    return None
