import json
from core.models import Activity, Lesson, StudentProgress, Unit, Video
from rest_framework import serializers


class JSONSerializerField(serializers.WritableField):

    def to_native(self, data):
        # return json.dumps(data) # data is a json already
        return data

    def from_native(self, obj):
        return json.loads(obj)


class VideoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Video
        fields = ('youtube_id',)


class ActivitySerializer(serializers.HyperlinkedModelSerializer):
    data = JSONSerializerField('data')

    class Meta:
        model = Activity
        fields = ('type','data')


class StudentProgressSerializer(serializers.ModelSerializer):
    complete = serializers.DateTimeField(required=False)

    class Meta:
        model = StudentProgress
        fields = ('unit', 'complete', 'last_access')


class UnitSerializer(serializers.HyperlinkedModelSerializer):
    video = VideoSerializer()
    activity = ActivitySerializer()

    class Meta:
        model = Unit
        fields = ('id', 'video', 'activity', 'position')


class LessonSerializer(serializers.HyperlinkedModelSerializer):
    units = UnitSerializer(many=True)
    url = serializers.HyperlinkedIdentityField(
        view_name='lesson',
        lookup_field='slug'
    )

    class Meta:
        model = Lesson
        fields = ('slug', 'desc', 'name', 'url', 'units',)
