import pytest

pytestmark = pytest.mark.django_db


def test(as_anon):
    healthcheck_report = as_anon.get("/api/v1/healthchecks/?format=json")
    for component, is_working in healthcheck_report.json().items():
        assert is_working == "working", f"{component} doesn't work"
