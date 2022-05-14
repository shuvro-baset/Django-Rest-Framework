from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from message_app.models import Message
from message_app.serializers import MessageSerializer


class MessageCreate(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = MessageSerializer

    def all_message_list(self, request):
        queryset = Message.objects.all()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        data = request.data
        data['create_by'] = request.user

        serializer = self.serializer_class(data=data, context={"context": request})
        if serializer.is_valid():
            serializer.save()
            s = serializer.data
            s['create_by'] = {
                "id": request.user.id,
                "username": request.user.first_name,
                "email": request.user.username
            }
            return Response(s, status=status.HTTP_201_CREATED)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
