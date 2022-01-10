from datetime import datetime, timezone
from functools import partial

import pytest
from django.test import Client
from wormhole.core.models import ShortLink

REPO_URL = "https://github.com/iamgodot/wormhole"
REPO_ALIAS = "4S4U4o"


@pytest.fixture
def client():
    return Client()


@pytest.fixture
def create_short_link(client, url: str = ""):
    return partial(
        client.post,
        "/api/v1/short_links",
        data={"url": url or REPO_URL},
        content_type="application/json",
    )


@pytest.mark.django_db
def test_shortening(create_short_link):
    resp = create_short_link()
    assert resp.status_code == 201
    resp_json = resp.json()
    short_link, expires_at = resp_json["short_link"], resp_json["expires_at"]
    assert short_link == f"wormhole.com/{REPO_ALIAS}"
    assert isinstance(expires_at, str)

    # Update expiration for the same url
    resp_json = create_short_link().json()
    assert resp_json["short_link"] == short_link
    expires_at_new = resp_json["expires_at"]
    assert isinstance(expires_at_new, str)
    assert expires_at_new != expires_at


@pytest.mark.django_db
def test_collision(create_short_link, mocker):
    ShortLink.objects.create(
        url="https://preset-url-for-collision",
        alias=REPO_ALIAS,
        expires_at=datetime.now(tz=timezone.utc),
    )
    spy = mocker.spy(ShortLink.objects, "create")
    spy.assert_not_called()
    resp = create_short_link()
    assert resp.status_code == 201
    spy.assert_called_once()


@pytest.fixture
def access_short_link(client, alias: str = ""):
    return partial(client.get, f"/{alias or REPO_ALIAS}")


@pytest.mark.django_db
def test_redirection(create_short_link, access_short_link):
    create_short_link()
    resp = access_short_link()
    assert resp.status_code == 302


@pytest.mark.django_db
def test_expired_redirection(access_short_link):
    ShortLink.objects.create(
        url=REPO_URL,
        alias=REPO_ALIAS,
        expires_at=datetime.now(tz=timezone.utc),
    )
    resp = access_short_link()
    assert resp.status_code == 400


@pytest.mark.django_db
def test_failed_redirection(access_short_link):
    resp = access_short_link()
    assert resp.status_code == 404
