from typing import Generator, List

from blog.models import ArticleTag


def compose_cache_key(prefix: str, *parts: str | None):
    parts_without_none_values = [part for part in parts if part is not None]
    return ":".join([prefix, *parts_without_none_values])


def iter_all_possible_cache_keys_to_invalidate(
    *, slug: str | None = None, tags: List[ArticleTag] | None = None
) -> Generator[str, None, None]:
    yield "articles"
    if slug:
        yield compose_cache_key("article", slug)
    if tags:
        yield from (compose_cache_key("articles", tag.title) for tag in tags)
