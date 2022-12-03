from djangorestframework_camel_case.util import camelize
from rest_framework.renderers import JSONRenderer


class AppJSONRenderer(JSONRenderer):
    charset = "utf-8"  # force DRF to add charset header to the content-type
    json_underscoreize = {
        "no_underscore_before_number": True
    }  # https://github.com/vbabiy/djangorestframework-camel-case#underscoreize-options

    def render(self, data, *args, **kwargs):
        return super().render(
            camelize(data, **self.json_underscoreize), *args, **kwargs
        )
