import pytest

from fuzeepass.passx import Uri


@pytest.fixture(
    params=[
        ("e:work/coding/github", True, False),
        ("e:personal/twitter", True, False),
        ("e:", True, False),
        ("g:work/coding/", False, True),
        ("g:personal/email/", False, True),
        ("g:::", False, True),
    ]
)
def setup_uri(request):
    yield request.param


def test_uri(setup_uri):
    uri, is_entry, is_group = setup_uri
    u = Uri(uri)
    assert u.is_entry() is is_entry
    assert u.is_group() is is_group


@pytest.fixture(
    params=[
        ("E:work/coding/github",),
        (":personal/twitter",),
        (":",),
        ("G:work/coding/",),
        ("x:personal/email/",),
    ]
)
def setup_uri_exception(request):
    yield request.param


def test_uri_exception(setup_uri_exception):
    (uri,) = setup_uri_exception
    with pytest.raises(TypeError):
        Uri(uri)
