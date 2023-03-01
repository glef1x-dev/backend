import pytest
from typing import List, Optional

from blog.models import ArticleTag
from blog.utils.cache import compose_cache_key
from blog.utils.cache import iter_all_possible_cache_keys_to_invalidate


@pytest.mark.parametrize(
    "prefix,parts,expected_result",
    [
        ["articles", ["some title"], "articles:some title"],
        ["h", ["e", "l", "l", "o"], "h:e:l:l:0"],
        ["h", None, "h"],
    ],
)
def test_compose_cache_key(
    prefix: str, parts: Optional[List[str]], expected_result: str
):
    parts = parts or []
    return compose_cache_key(prefix, *parts) == expected_result


@pytest.mark.parametrize(
    "expected_result,slug,tags",
    [
        [["articles"], None, None],
        [["articles", "articles:test"], None, "test"],
        [["articles", "articles:test"], None, [ArticleTag(title="test")]],
        [
            ["articles", "articles:test1", "articles:test2"],
            None,
            [ArticleTag(title="test1"), ArticleTag(title="test2")],
        ],
    ],
)
def test_get_all_possible_cache_keys_to_invalidate(
    expected_result: List[str],
    slug: Optional[str],
    tags: List[ArticleTag] | None,
):
    assert (
        list(iter_all_possible_cache_keys_to_invalidate(slug=slug, tags=tags))
        == expected_result
    )
