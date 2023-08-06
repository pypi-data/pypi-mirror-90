
from rest_framework import serializers
from rest_framework.relations import HyperlinkedRelatedField
from rest_framework.utils.field_mapping import get_nested_relation_kwargs

class InheritsModelSerializer(serializers.ModelSerializer):
    def build_field(self, field_name, info, model_class, nested_depth):
        '''
        inherits the error_messages of the model
        '''
        result: tuple = super().build_field(field_name, info, model_class, nested_depth)

        field = model_class._meta.get_field(field_name)
        error_messages = field.error_messages

        if error_messages:
            result[1]['error_messages'] = field.error_messages

        return result


class InheritsHyperlinkedModelSerializer(InheritsModelSerializer):
    serializer_related_field = HyperlinkedRelatedField

    def get_default_field_names(self, declared_fields, model_info):
        """
        Return the default list of field names that will be used if the
        `Meta.fields` option is not specified.
        """
        return (
            [self.url_field_name] +
            list(declared_fields) +
            list(model_info.fields) +
            list(model_info.forward_relations)
        )

    def build_nested_field(self, field_name, relation_info, nested_depth):
        """
        Create nested fields for forward and reverse relationships.
        """
        class NestedSerializer(InheritsModelSerializer):
            class Meta:
                model = relation_info.related_model
                depth = nested_depth - 1
                fields = '__all__'

        field_class = NestedSerializer
        field_kwargs = get_nested_relation_kwargs(relation_info)

        return field_class, field_kwargs
