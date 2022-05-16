from rest_framework import serializers


class MixinCommentSerealizers(serializers.ModelSerializer):

    name = serializers.ReadOnlyField(source='name.username')
    email = serializers.ReadOnlyField(source='name.email')

