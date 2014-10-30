from rest_framework import serializers

from drf_ember.serializers import SideloadSerializer

from tests.models import ChildModel, ParentModel, OptionalChildModel, \
    OneToOne, ReverseOneToOne


class ChildSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChildModel

class OptionalChildSerializer(serializers.ModelSerializer):
    class Meta:
        model = OptionalChildModel

class OneToOneSerializer(serializers.ModelSerializer):
    class Meta:
        model = OneToOne

class ReverseOneToOneSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'one_to_one')
        model = ReverseOneToOne

class ParentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParentModel
        fields = ('id', 'text', 'children', 'old_children')


class ChildSideloadSerializer(SideloadSerializer):
    class Meta:
        sideload_fields = ['parent', 'old_parent']
        base_serializer = ChildSerializer
        sideloads = [(ParentModel, ParentSerializer)]


class OptionalChildSideloadSerializer(SideloadSerializer):
    class Meta:
        sideload_fields = ['parent']
        base_serializer = OptionalChildSerializer
        sideloads = [(ParentModel, ParentSerializer)]

class OneToOneSideloadSerializer(SideloadSerializer):
    class Meta:
        sideload_fields = ['reverse_one_to_one']
        base_serializer = OneToOneSerializer
        sideloads = [(ReverseOneToOne, ReverseOneToOneSerializer)]

class ReverseOneToOneSideloadSerializer(SideloadSerializer):
    class Meta:
        sideload_fields = ['one_to_one']
        base_serializer = ReverseOneToOneSerializer
        sideloads = [(OneToOne, OneToOneSerializer)]
