from .models import User,Message
from rest_framework import routers, serializers, viewsets

# Serializers define the API representation.
class UserSerializer(serializers.Serializer):
    class Meta:
        model = User
        fields = [ 'username', 'email']

class MessageSerializer(serializers.Serializer):
    class Meta:
        model = Message
        fields = [ 'sender', 'receiver','message','timestamp','is_read']