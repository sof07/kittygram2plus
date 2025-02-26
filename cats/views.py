from rest_framework import viewsets
from rest_framework.throttling import AnonRateThrottle
from .models import Achievement, Cat, User
from .permissions import OwnerOrReadOnly, ReadOnly

from .serializers import AchievementSerializer, CatSerializer, UserSerializer


class CatViewSet(viewsets.ModelViewSet):
    queryset = Cat.objects.all()
    serializer_class = CatSerializer
    # Проверка на авторизацию и на автора поста
    permission_classes = (OwnerOrReadOnly,)
    # При такой реализации лимит «1000 запросов в день для анонимных
    # пользователей» сработает точно также, как если бы он был объявлен
    # в settings.py. При превышении лимита будет возвращён код ответа 429
    # Too Many Requests, а в теле ответа вернётся сообщение об ограничении
    # доступа и информация о том, через какой период времени можно
    # будет повторить запрос.
    throttle_classes = (AnonRateThrottle,)  # Подключили класс AnonRateThrottle

    def get_permissions(self):
        # Если в GET-запросе требуется получить информацию об объекте
        if self.action == 'retrieve':
            # Вернем обновленный перечень используемых пермишенов
            return (ReadOnly(),)
    # Для остальных ситуаций оставим текущий перечень пермишенов без изменений
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class AchievementViewSet(viewsets.ModelViewSet):
    queryset = Achievement.objects.all()
    serializer_class = AchievementSerializer
