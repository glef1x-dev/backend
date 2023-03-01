from typing import Optional
from urllib.parse import urljoin

from django.conf import settings
from django.contrib.sites.models import Site
from django.utils.encoding import iri_to_uri


def build_absolute_uri(location: str, domain: Optional[str] = None) -> str:
    """Create absolute uri from location.

    If provided location is absolute uri by itself, it returns unchanged value,
    otherwise if provided location is relative, absolute uri is built and returned.
    """
    host = domain or Site.objects.get_current().domain
    protocol = "https" if settings.ENABLE_SSL else "http"  # type: ignore[misc] # circular import # noqa: E501
    current_uri = f"{protocol}://{host}"
    location = urljoin(current_uri, location)
    return iri_to_uri(location)
