import pytest
from easy_publish import posts


@pytest.fixture(scope="module")
def fakenotes_files():
    return [
        "./tests/fakenotes/note.md",
        "./tests/fakenotes/other.md",
        "./tests/fakenotes/other-note-two.md",
    ]


@pytest.fixture(scope="module")
def fakenotes_file():
    return "./tests/fakenotes/note.md"


@pytest.fixture(scope="module")
def parsed_posts(fakenotes_files):
    parsed_posts = posts.generate_parsed_post_list(fakenotes_files, "%m-%d-%y")
    return parsed_posts


@pytest.fixture(scope="module")
def PostsCollection(parsed_posts):
    posts_collection = posts.PostsCollection(parsed_posts)
    return posts_collection


@pytest.fixture(scope="module")
def MetadataCollection(parsed_posts):
    metadata_collection = posts.MetadataCollection(parsed_posts, "ascending")
    return metadata_collection


def test_generate_posts():
    # incomplete
    p = posts.generate_posts("./tests/fakenotes")
    assert p.__class__.__name__ == "Posts"


def test_Posts(PostsCollection, MetadataCollection):
    p = posts.Posts(PostsCollection.posts, MetadataCollection.metadata)
    assert p.posts.__class__.__name__ == "dict"
    assert p.metadata.__class__.__name__ == "list"
    assert len(p.posts) == 3
    assert p.posts['note'].title == "This is the fakenote"

    assert len(p.metadata) == 3
    assert p.metadata[0].title == "This is the fakenote"


def test_Metadata(fakenotes_file):
    p = posts.PostParser(fakenotes_file, "date")
    assert p.route == "note"
    assert p.file == "./tests/fakenotes/note.md"
    assert p.title == "This is the fakenote"
    assert p.date == "5-23-94"
    assert p.author == "Sam Dixon"
    assert p.tags == ["first post", "item", "blogpost"]


def test_PostParser(fakenotes_file):
    # incomplete
    p = posts.PostParser(fakenotes_file, "date")
    assert p.route == "note"
    assert p.file == "./tests/fakenotes/note.md"
    assert p.title == "This is the fakenote"
    assert p.date == "5-23-94"
    assert p.author == "Sam Dixon"
    assert p.tags == ["first post", "item", "blogpost"]
    assert p.content
