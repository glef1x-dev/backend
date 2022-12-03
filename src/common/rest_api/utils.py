from typing import no_type_check

from rest_framework import serializers


@no_type_check
def create_serializer_class(name, fields):
    return type(name, (serializers.Serializer,), fields)


@no_type_check
def inline_serializer(*, fields, data=None, **kwargs):
    serializer_class = create_serializer_class(name="", fields=fields)

    if data is not None:
        return serializer_class(data=data, **kwargs)

    return serializer_class(**kwargs)
