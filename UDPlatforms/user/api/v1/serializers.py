from user.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    address = serializers.SerializerMethodField(required=False)

    class Meta:
        model = User
        fields = '__all__'

    def validate(self, data):
        is_child = data.get('is_child')
        parent = data.get('parent', None)

        # if user is child then it must have parent
        if is_child:
            if parent is None:
                raise serializers.ValidationError(
                    'Parent is required for this user.')
        return data

    def get_address(self, obj):
        if obj.street == '' and obj.city == '' and obj.state == '' and obj.zip == '':
            return ''
        return ', '.join([obj.street, obj.city, obj.state, obj.zip])
