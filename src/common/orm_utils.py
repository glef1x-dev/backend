from operator import itemgetter
from typing import Any, Dict, Iterable, Iterator, List, Type, TypeAlias, TypeVar

from django.db import models
from django.db.models import ForeignKey
from django.db.models.fields.files import ImageFieldFile
from django.forms.models import model_to_dict

from blog.tests.utils.files import file_to_base64

_T = TypeVar("_T")
ListOfDicts: TypeAlias = List[Dict[str, Any]]


def create_m2m_related_objects(
    second_related_model_dicts: ListOfDicts,
    *,
    first_related_model_instance: models.Model,
    second_related_model_cls: Type[models.Model],
    through_model_cls: Type[models.Model]
) -> List[models.Model]:
    """The most efficient way to create m2m related objects using only 3 queries:

    * one query to fetch the relevant first_related_model_instance;
    * one query to fetch the relevant second_related_model_cls instances related to first_related_model_instance;
    * one query to create all connections between the first_related_model_instance and second_related_model_cls


    :param second_related_model_dicts: list of dicts that contains valid data of second_related_model_cls
    :param first_related_model_instance:
    :param second_related_model_cls:
    :param through_model_cls:
    :return:
    """
    created_related_objects = list(
        _only_first_element_from_tuples(
            second_related_model_cls.objects.get_or_create(**related_object_dict)
            for related_object_dict in second_related_model_dicts
        )
    )

    foreign_key_from_through_model_to_first_related_model_name = (
        _get_foreign_key_field_name_from_related_model(
            first_related_model_instance.__class__, through_model_cls
        ).name
    )
    foreign_key_from_through_model_to_seconds_related_model_name = (
        _get_foreign_key_field_name_from_related_model(
            second_related_model_cls, through_model_cls
        ).name
    )

    return through_model_cls.objects.bulk_create(
        [
            through_model_cls(
                **{
                    foreign_key_from_through_model_to_first_related_model_name: first_related_model_instance,
                    foreign_key_from_through_model_to_seconds_related_model_name: related_object,
                }
            )
            for related_object in created_related_objects
        ]
    )


def _get_foreign_key_field_name_from_related_model(
    first_related_model_cls: Type[models.Model],
    second_related_model_cls: Type[models.Model],
) -> ForeignKey | None:
    foreign_keys_of_seconds_related_model = tuple(
        filter(
            lambda field: isinstance(field, ForeignKey),
            second_related_model_cls._meta.fields,
        )
    )

    foreign_key_to_first_related_model = tuple(
        filter(
            lambda foreign_key_field: foreign_key_field.related_model
            == first_related_model_cls,
            foreign_keys_of_seconds_related_model,
        )
    )
    if foreign_key_to_first_related_model:
        return foreign_key_to_first_related_model[0]

    return None


def _only_first_element_from_tuples(collection: Iterable[_T]) -> Iterator[_T]:
    return map(itemgetter(0), collection)


def model_to_dict_nested(model: models.Model):
    model_as_dict = model_to_dict(model)

    for key, value in model_as_dict.items():
        if isinstance(value, ImageFieldFile):
            model_as_dict[key] = file_to_base64(value)
        elif isinstance(value, list):
            model_as_dict[key] = [
                model_to_dict(obj) for obj in value if isinstance(obj, models.Model)
            ]

    return model_as_dict
