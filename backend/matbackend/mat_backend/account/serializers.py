from rest_framework import serializers
from account.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    #     fields = ['email', 'username', 'password']
        # extra_kwargs = {'password': {'write_only': True}}

    # def create(self, validated_data):
    #     return User.objects.create_user(**validated_data)

    # def update(self, user, validated_data):
    #     password = validated_data.pop('password', None)
    #     if password is not None:
    #         user.set_password(password)
    #     for field, value in validated_data.items():
    #         setattr(user, field, value)
    #     user.save()
    #     return user