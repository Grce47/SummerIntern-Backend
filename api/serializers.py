from rest_framework.serializers import ModelSerializer,StringRelatedField
from django.contrib.auth.models import User
from myUser.models import pythonCode

class UserSerializers(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class PythonCodeSerializer(ModelSerializer):
    user = StringRelatedField(many=False)
    class Meta:
        model = pythonCode
        fields = '__all__'