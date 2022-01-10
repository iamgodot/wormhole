import json
from datetime import datetime, timedelta, timezone
from hashlib import md5

import base62
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.db.utils import IntegrityError
from django.http import HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import ShortLink


def get_alias(raw: str):
    return base62.encodebytes(md5((raw).encode()).digest())[:6]


@csrf_exempt
def create_short_link(request):
    """Given an URL, return a shortened link.

    Args:
      url: URL to be shortened.

    Returns:
      short_link: Shortened result of URL.
      expires_at: Timestamp before which the link is valid.
    """

    payload = json.loads(request.body)
    url = payload.get("url")
    try:
        URLValidator(["http", "https"])(url)
    except ValidationError:
        return JsonResponse({"error": "Valid URL required."}, status=422)

    expires_at = datetime.now(tz=timezone.utc) + timedelta(hours=1)
    try:
        short_link, _ = ShortLink.objects.update_or_create(
            url=url, alias=get_alias(url), defaults={"expires_at": expires_at}
        )
    except IntegrityError:
        # Add timestamp as randoms to avoid collision
        short_link = ShortLink.objects.create(
            url=url, alias=get_alias(f"{url}{datetime.utcnow()}"), expires_at=expires_at
        )

    return JsonResponse(
        {
            "short_link": short_link.build_url(),
            "expires_at": expires_at.isoformat(),
        },
        status=201,
    )


def redirect_short_link(request):
    """Redirect to the original url.

    Args:
      shor_link: This should be the requested url.

    Returns:
      Response with 302: If short link is valid.
      Error with 400: If short link is expired.
      Error with 404: If link is not found.
    """
    alias = request.path.strip("/")
    if short_link := ShortLink.objects.filter(alias=alias).first():
        time_delta = short_link.expires_at - datetime.now(tz=timezone.utc)
        if time_delta.total_seconds() < 0:
            return JsonResponse({"error": "Link has expired."}, status=400)
        return HttpResponseRedirect(short_link.url)

    return JsonResponse({"error": "Link not found."}, status=404)
