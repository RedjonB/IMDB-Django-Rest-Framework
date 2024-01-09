from rest_framework import serializers
from watchlist_app.models import WatchList, StreamPlatform, Review

# from django_filters import rest_framework as filters


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        exclude = ['watchlist']
        # fields = '__all__'

    review_user = serializers.StringRelatedField(read_only=True)


class WatchListSerializer(serializers.ModelSerializer):
    class Meta:
        model = WatchList
        fields = '__all__'

    # reviews = ReviewSerializer(many=True, read_only=True)
    platform = serializers.CharField(source="platform.name")


class StreamPlatformSerializer(serializers.ModelSerializer):
    class Meta:
        model = StreamPlatform
        fields = '__all__'

    watchlist = WatchListSerializer(many=True, read_only=True)
    # average = serializers.SerializerMethodField()
    #
    # @staticmethod
    # def get_average(obj):
    #     return obj.name + obj.about

#
# class StreamPlatformFilterSerializer(filters.FilterSet):
#     class Meta:
#         model = StreamPlatform
#         fields = ['watchlist__id']

    # @staticmethod
    # def get_len_name(obj):
    #     length = len(obj.name)
    #     return length
    #
    # def validate(self, data):
    #     if data['name'] == data['description']:
    #         raise serializers.ValidationError('Name and description cant be the same')
    #     return data
    #
    # @staticmethod
    # def validate_name(value):
    #     if len(value) < 2:
    #         raise serializers.ValidationError('Name is too short')
    #     else:
    #         return value

# def name_length(value):
#     if len(value) < 2:
#         raise serializers.ValidationError('Name is too short')
#     else:
#         return value
#
# class MovieSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     name = serializers.CharField(validators=[name_length])
#     description = serializers.CharField()
#     active = serializers.BooleanField()
#
#    def create(self, validated_data):
#         return Movie.objects.create(**validated_data)
#
#     def update(self, instance, validated_data):
#         instance.name = validated_data.get('name', instance.name)
#         instance.description = validated_data.get('description', instance.description)
#         instance.active = validated_data.get('active', instance.active)
#         instance.save()
#         return instance
#
#     def validate(self, data):
#         if data['name'] == data['description']:
#             raise serializers.ValidationError('Name and description cant be the same')

#     def validate_name(self, value):
#       if len(value) < 2:
#           raise serializers.ValidationError('Name is too short')
#       else:
#           return value
