from rest_framework import serializers


class FromContext(object):
    def __init__(self, value_fn):
        self.value_fn = value_fn

    def set_context(self, serializer_field):
        self.value = self.value_fn(serializer_field.context)

    def __call__(self):
        return self.value


class FromInitialData(object):
    def __init__(self, value_fn):
        self.value_fn = value_fn

    def set_context(self, serializer_field):
        self.value = self.value_fn(serializer_field.parent.initial_data)

    def __call__(self):
        return self.value


class MyPrimaryKeyRelatedField(serializers.Field):

    def get_value(self, dictionary):
        # always use the default value.
        # User input is never provided or accepted.
        return serializers.empty

    def to_representation(self, value):
        return value.pk


class UpdateOnlyDefault(serializers.CreateOnlyDefault):
    """
    This class may be used to provide default values that are only used
    for update operations, but that do not return any value for create
    operations.
    """

    def set_context(self, serializer_field):
        self.is_update = serializer_field.parent.instance is not None
        if callable(self.default) and hasattr(self.default, 'set_context') and self.is_update:
            self.default.set_context(serializer_field)

    def __call__(self):
        if not self.is_update:
            raise serializers.SkipField()
        if callable(self.default):
            return self.default()
        return self.default


class CommonFields(serializers.Serializer):
    # tenant = serializers.HiddenField(default=FromContext(
    #     lambda context: context.get('request').user.profile.tenant))
    created_by = MyPrimaryKeyRelatedField(required=False,
                                          default=serializers.CreateOnlyDefault(
                                              serializers.CurrentUserDefault()))
    modified_by = MyPrimaryKeyRelatedField(required=False,
                                           default=UpdateOnlyDefault(
                                               serializers.CurrentUserDefault()))
    common_fields = ('created_by',
                     'created_on', 'modified_by', 'modified_on'
                     #  , 'tenant'
                     )
    read_only_fields = ('created_by',
                        'created_on', 'modified_by', 'modified_on')
