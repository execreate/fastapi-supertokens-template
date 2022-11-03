from typing import Type

from sqlalchemy.orm import InstrumentedAttribute

from db.crud.base import BaseCrud
from db.tables.blog_post import BlogPost
from schemas.blog_post import (
    InBlogPostSchema,
    BlogPostSchema,
    PaginatedBlogPostSchema,
)


class BlogPostCrud(
    BaseCrud[InBlogPostSchema, BlogPostSchema, PaginatedBlogPostSchema, BlogPost]
):
    @property
    def _table(self) -> Type[BlogPost]:
        return BlogPost

    @property
    def _schema(self) -> Type[BlogPostSchema]:
        return BlogPostSchema

    @property
    def _paginated_schema(self) -> Type[PaginatedBlogPostSchema]:
        return PaginatedBlogPostSchema

    @property
    def _order_by(self) -> InstrumentedAttribute:
        return BlogPost.created_at
