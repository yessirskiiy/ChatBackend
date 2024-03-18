from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from .serializers import *
from .permissions import IsDialogParticipant, CanAccessMessage
from rest_framework import status, mixins
from rest_framework.decorators import action


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class MessageViewSet(mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     mixins.ListModelMixin,
                     GenericViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = (CanAccessMessage, IsAuthenticatedOrReadOnly, )
    authentication_classes = (JWTAuthentication, )

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['text']
    filterset_fields = ['author', 'dialog']
    ordering_fields = ['send_at', 'author']

    def get_queryset(self):
        user = self.request.user
        return Message.objects.filter(author=user) | \
            Message.objects.filter(dialog__author=user) | \
            Message.objects.filter(dialog__user=user)


class DialogViewSet(ModelViewSet):
    queryset = Dialog.objects.all()
    serializer_class = DialogSerializer
    permission_classes = (IsDialogParticipant, IsAuthenticatedOrReadOnly,)

    authentication_classes = (JWTAuthentication, )

    def get_queryset(self):
        user = self.request.user
        return Dialog.objects.filter(author=user) | Dialog.objects.filter(user=user)

    def create(self, request, *args, **kwargs):
        author = request.user
        user_id = request.data.get('user')
        existing_dialog = Dialog.objects.filter(author=author, user_id=user_id).exists()
        existing_dialog_reverse = Dialog.objects.filter(author_id=user_id, user=author).exists()
        if existing_dialog:
            return Response({'error': 'Диалог между этими пользователями уже существует'},
                            status=status.HTTP_400_BAD_REQUEST)
        if existing_dialog_reverse:
            return Response({'error': 'Диалог между этими пользователями уже существует'},
                            status=status.HTTP_400_BAD_REQUEST)
        if not user_id:
            return Response({'error': 'Пользователь не найден'}, status=status.HTTP_400_BAD_REQUEST)
        if int(user_id) == author.id:
            return Response({'error': 'Вы не можете начать диалог с собой'}, status=status.HTTP_400_BAD_REQUEST)
        dialog = Dialog.objects.create(author=author, user_id=user_id)
        serializer = self.get_serializer(dialog)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(methods=['post', 'get'], detail=True)
    def create_message(self, request, pk=None):
        dialog = self.get_object()
        if dialog.author != request.user and dialog.user != request.user:
            return Response({'error': 'Вы не являетесь участником этого диалога'}, status=status.HTTP_403_FORBIDDEN)
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(dialog=dialog, author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
