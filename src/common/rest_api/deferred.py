class DeferredSerializerMixin:
    @property
    def _readable_fields(self):
        for field in self.fields.values():
            if field.write_only:
                continue
            if (
                self.parent
                and field.field_name in type(self).Meta.exclude_from_response_when_many
            ):
                continue

            yield field

    class Meta:
        exclude_from_response_when_many = []
