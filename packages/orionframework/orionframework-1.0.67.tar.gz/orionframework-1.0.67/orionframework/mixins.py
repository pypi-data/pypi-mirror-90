from rest_framework import exceptions, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.settings import api_settings


class CreateBulkModelMixin(object):
    """
    Create model instances in bulk.
    """

    @action(detail=False, methods=["POST"], url_path="bulk_create")
    def create_bulk(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        instances = self.perform_create_bulk(serializer)
        if isinstance(self, ActionSerializerView):
            serializer = self.get_serializer_for("list", instances, many=True)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create_bulk(self, serializer):
        return serializer.save()

    def get_success_headers(self, data):
        try:
            return {'Location': str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}


class UpdateBulkModelMixin(object):
    """
    Update model instances in bulk.
    """

    @action(detail=False, methods=["PATCH"], url_path="bulk_update")
    def update_bulk(self, request, *args, **kwargs):
        for data in request.data:
            instance = self.queryset.get(id=data.get("id"))
            serializer = self.get_serializer(instance=instance, data=data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()

        return Response("OK")


class MethodSerializerView(object):
    """
    Utility class for get different serializer class by http method.
    For example:
    method_serializer_classes = {
        ("GET", ): MyModelListViewSerializer,
        ("PUT", "PATCH"): MyModelCreateUpdateSerializer
    }
    """
    http_method_serializer_classes = None

    def get_serializer_class(self):
        assert self.http_method_serializer_classes is not None, (
                "Expected view %s should contain http_method_serializer_classes "
                "to get right serializer class." %
                (self.__class__.__name__,)
        )
        for methods, serializer_cls in self.http_method_serializer_classes.items():
            if self.request.method in methods:
                return serializer_cls

        raise exceptions.MethodNotAllowed(self.request.method)


class ActionSerializerView(object):
    """
    Utility class for get different serializer class by action name.
    For example:
    action_serializer_classes = {
        ("create", ): MyModelListViewSerializer,
        ("retrieve", "update"): MyModelCreateUpdateSerializer
    }
    """
    action_serializer_classes = None

    def get_serializer_for(self, action, *args, **kwargs):

        kwargs['context'] = self.get_serializer_context()

        return self.get_serializer_class_for(action)(*args, **kwargs)

    def get_serializer_class_for(self, action):
        if self.action_serializer_classes:
            for actions, serializer_cls in self.action_serializer_classes.items():
                if action in actions:
                    return serializer_cls

        return super(ActionSerializerView, self).get_serializer_class()

    def get_serializer_class(self):
        return self.get_serializer_class_for(self.action)


class SmartQuerysetView(object):

    def get_queryset(self):

        queryset = super(SmartQuerysetView, self).get_queryset()

        serializer_class = self.get_serializer_class()

        if hasattr(serializer_class, "Meta"):

            if hasattr(serializer_class.Meta, "select_related"):
                queryset = queryset.select_related(*serializer_class.Meta.select_related)

            if hasattr(serializer_class.Meta, "prefetch_related"):
                queryset = queryset.prefetch_related(*serializer_class.Meta.prefetch_related)

            if hasattr(serializer_class.Meta, "select_only"):
                queryset = queryset.only(*serializer_class.Meta.select_only)

            elif hasattr(serializer_class.Meta, "fields") and isinstance(serializer_class.Meta.fields, (list, tuple)):
                queryset = queryset.only(*serializer_class.Meta.fields)

        return queryset


class AbstractViewSet(ActionSerializerView,
                      SmartQuerysetView,
                      viewsets.GenericViewSet):
    """
    Base abstract viewset for convenience
    """
    pass
