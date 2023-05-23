from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import pagination, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated

from ads.filters import AdFilter
from ads.models import Ad, Comment
from ads.permissions import IsOwner, AdAdminPermission, IsExecutor
from ads.serializers import AdSerializer, CommentSerializer


class AdPagination(pagination.PageNumberPagination):
    """
    Пагинация на страницу не более 4 объектов
    """
    page_size = 4


# TODO view функции. Предлагаем Вам следующую структуру - но Вы всегда можете использовать свою
class AdViewSet(viewsets.ModelViewSet):
    """
    Вьюсет который выводит список всех объектов
    """
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    pagination_class = AdPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = AdFilter
    permission_classes = [AllowAny]

    def get_permissions(self):
        if self.action == "list":
            self.permission_classes = [IsOwner, ]
        elif self.action == "retrieve":
            self.permission_classes = [IsAuthenticated, ]
        elif self.action in ["create", "update", "partial_update", "destroy", "me"]:
            self.permission_classes = [IsAuthenticated, AdAdminPermission | IsExecutor]

        return super().get_permissions()

    @action(detail=False, methods=['get'])
    def me(self, request, *args, **kwargs):
        self.queryset = Ad.objects.filter(author=request.user)
        return super().list(self, request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    """ Вьюсет который выводит список всех объектов """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    pagination_class = None

    def perform_create(self, serializer):
        ads_id = self.kwargs.get("ads_pk")
        ad_instance = get_object_or_404(Ad, id=ads_id)
        user = self.request.user
        serializer.save(author=user, ad=ad_instance)

    def get_queryset(self, *args, **kwargs):
        comment = self.kwargs.get('ads_pk')
        return super().get_queryset().filter(ad=comment)

    def get_permissions(self):
        if self.action == "retrieve":
            self.permission_classes = [IsAuthenticated, ]
        elif self.action in ["create", "update", "partial_update", "destroy", ]:
            self.permission_classes = [IsAuthenticated, AdAdminPermission | IsExecutor]
        return super().get_permissions()
