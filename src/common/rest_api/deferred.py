class DeferredSerializerMixin:
    @property
    def _readable_fields(self):
        for field in self.fields.values():
            if field.write_only:
                continue
            if (
                self.parent
                and field.field_name
                in type(self).Meta.deferred_fields_for_list_serializer
            ):
                continue

            yield field

    class Meta:
        deferred_fields_for_list_serializer = []
