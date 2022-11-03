from uuid import UUID
from fastapi import APIRouter, Depends
from schemas import blog_post as blog_post_schemas
from core.pagination import LimitOffsetPaginationParams


router = APIRouter(
    prefix="/blog",
    tags=["Blog posts"],
)


@router.post("", response_model=blog_post_schemas.OutBlogPostSchema)
async def create_a_blog_post(blog_post: blog_post_schemas.InBlogPostSchema):
    return None


@router.get("", response_model=blog_post_schemas.PaginatedBlogPostSchema)
async def list_blog_posts(
    blog_post: blog_post_schemas.InBlogPostSchema,
    pagination=Depends(LimitOffsetPaginationParams),
):
    return None


@router.get("/{post_id}", response_model=blog_post_schemas.OutBlogPostSchema)
async def retrieve_a_blog_post(
    blog_post: blog_post_schemas.InBlogPostSchema, post_id: UUID
):
    return None
