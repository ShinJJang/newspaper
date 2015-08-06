from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie import fields
from django.contrib.auth.models import User
from news.models import Comment, Thread
import json


class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        fields = ['username', 'id']
        include_resource_uri = False
        allowed_methods = ['get']


class ThreadResource(ModelResource):
    class Meta:
        queryset = Thread.objects.all()
        include_resource_uri = False
        allowed_methods = ['get']
        filtering = {
            "id": ALL,
        }


class CommentResource(ModelResource):
    thread = fields.ForeignKey(ThreadResource, 'thread')
    writer = fields.ForeignKey(UserResource, 'writer', full=True)
    parent_comment = fields.ForeignKey('news.api.CommentResource', 'parent_comment', null=True)

    class Meta:
        queryset = Comment.objects.all()
        include_resource_uri = False
        filtering = {
            'thread': ALL_WITH_RELATIONS,
            'comment': ALL_WITH_RELATIONS,
            'parent_comment': ALL_WITH_RELATIONS,
        }

    def dehydrate(self, bundle):
        child_comments = Comment.objects.filter(parent_comment_id=bundle.data["id"])
        if child_comments.count() > 0:
            print(child_comments)
            print()
            objects = []
            for q in child_comments:
                data = self.build_bundle(obj=q, request=bundle.request)
                data = self.full_dehydrate(data)
                objects.append(data)
            desired_format = self.determine_format(bundle.request)
            json_data = self.serialize(bundle.request, objects, desired_format)
            bundle.data["childs"] = json.loads(json_data)
        return bundle