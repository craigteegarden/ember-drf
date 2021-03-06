from django.test import TestCase

from rest_framework.renderers import JSONRenderer
from rest_framework.serializers import ReturnDict

from ember_drf.renderers import EmberJSONRenderer, ActiveModelJSONRenderer, \
    convert_related_keys

from tests.serializers import ChildSideloadSerializer
from tests.models import ChildModel, ParentModel

class RendererTests(TestCase):

    def test_ember_json_renderer(TestCase):
        obj = {
            'under_score': [
                {'nested_underscore': 'some_thing'},
                {'nested_underscore': 'some_thing'},
                {'nested_underscore': 'some_thing'},
            ]
        }
        expected = {
            'underScore': [
                {'nestedUnderscore': 'some_thing'},
                {'nestedUnderscore': 'some_thing'},
                {'nestedUnderscore': 'some_thing'},
            ]
        }
        assert EmberJSONRenderer().render(obj) == \
            JSONRenderer().render(expected)

    def test_convert_related_keys_single(TestCase):
        parent = ParentModel.objects.create()
        old_parent = ParentModel.objects.create()
        child = ChildModel.objects.create(parent=parent, old_parent=old_parent)
        obj = ChildSideloadSerializer(child).data
        expected = {
            'child_model': {
                'id': child.id,
                'parent_id': parent.id,
                'old_parent_id': old_parent.id
            },
            'parent_models': [
                {'id': p.id, 'text': p.text, 'children_ids': p.child_ids,
                'old_children_ids': p.old_child_ids } for p in [parent, old_parent]
            ]
        }
        assert convert_related_keys(obj) == expected

    def test_active_model_json_renderer(TestCase):
        parents = [ParentModel.objects.create() for x in range(3)]
        children = [
            ChildModel.objects.create(parent=parents[1], old_parent=parents[2]),
            ChildModel.objects.create(parent=parents[1], old_parent=parents[2]),
            ChildModel.objects.create(parent=parents[0], old_parent=parents[1])
        ]
        obj = ChildSideloadSerializer(children, many=True).data
        expected = {
            'child_models': [
                {'id': c.id, 'parent_id': c.parent.id,
                'old_parent_id': c.old_parent.id} for c in children
            ],
            'parent_models': [
                {'id': p.id, 'text': p.text, 'children_ids': p.child_ids,
                'old_children_ids': p.old_child_ids } for p in parents
            ]

        }
        assert convert_related_keys(obj) == expected
