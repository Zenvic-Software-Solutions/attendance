from contextlib import suppress
from rest_framework import status
from rest_framework.exceptions import MethodNotAllowed, NotFound
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.status import is_success
from rest_framework.views import APIView
from apps.BASE.config import API_RESPONSE_ACTION_CODES



class AppViewMixin:
    """
    A base mixin that provides utility methods and overrides for handling
    requests, responses, and exceptions in a consistent format.
    """
    def get_request(self):
        return self.request

    def get_user(self):
        """
        Returns the user object from the request.
        """
        return self.get_request().user

    def get_authenticated_user(self):
        """
        Returns the authenticated user or None if the user is not authenticated.
        """
        user = self.get_user()
        return user if user and user.is_authenticated else None

    def send_error_response(self, data=None):
        """
        Sends a standardized error response with a 400 Bad Request status code.
        """
        return self.send_response(data=data, status_code=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def send_response(data=None, status_code=status.HTTP_200_OK, action_code="DO_NOTHING", **other_response_data):
        """
        Sends a standardized JSON response with additional metadata.
        """
        return Response(
            data={
                "data": data,
                "status": "success" if is_success(status_code) else "error",
                "action_code": action_code,
                **other_response_data,
            },
            status=status_code,
        )

    def get_app_response_schema(self, response: Response, **kwargs):
        """
        Converts an existing Response object into the standardized format.
        """
        return self.send_response(
            data=response.data, status_code=response.status_code, **kwargs
        )

    def handle_exception(self, exc):
        """
        Overrides exception handling to include a standardized action_code.
        """
        action_code = API_RESPONSE_ACTION_CODES.get(
            "display_error_1", "UNKNOWN_ERROR"
        )
        if hasattr(exc, "status_code") and exc.status_code == 401:
            action_code = "AUTH_TOKEN_NOT_PROVIDED_OR_INVALID"

        return self.get_app_response_schema(
            super().handle_exception(exc), action_code=action_code
        )

    def list(self, request, *args, **kwargs):
        """
        Handles the list action, standardizing the response schema.
        """
        with suppress(AttributeError):
            return self.get_app_response_schema(super().list(request, *args, **kwargs))

        raise MethodNotAllowed(method=self.get_request().method)

    def retrieve(self, request, *args, **kwargs):
        """
        Handles the retrieve action, standardizing the response schema.
        """
        with suppress(AttributeError):
            return self.get_app_response_schema(
                super().retrieve(request, *args, **kwargs)
            )

        raise MethodNotAllowed(method=self.get_request().method)

    def create(self, request, *args, **kwargs):
        """
        Handles the create action, standardizing the response schema.
        """
        with suppress(AttributeError):
            return self.get_app_response_schema(
                super().create(request, *args, **kwargs)
            )

        raise MethodNotAllowed(method=self.get_request().method)

    def update(self, request, *args, **kwargs):
        """
        Handles the update action, standardizing the response schema.
        """
        with suppress(AttributeError):
            return self.get_app_response_schema(
                super().update(request, *args, **kwargs)
            )

        raise MethodNotAllowed(method=self.get_request().method)

    def destroy(self, request, *args, **kwargs):
        """
        Handles the destroy action, standardizing the response schema.
        """
        with suppress(AttributeError):
            return self.get_app_response_schema(
                super().destroy(request, *args, **kwargs)
            )

        raise MethodNotAllowed(method=self.get_request().method)

    def partial_update(self, request, *args, **kwargs):
        """
        Handles the partial update action, standardizing the response schema.
        """
        with suppress(AttributeError):
            return self.get_app_response_schema(
                super().partial_update(request, *args, **kwargs)
            )

        raise MethodNotAllowed(method=self.get_request().method)


class AppAPIView(AppViewMixin, APIView):
    """
    Custom base view that combines the AppViewMixin and APIView.
    """
    sync_action_class = None
    get_object_model = None
    serializer_class = None

    def get_valid_serializer(self, instance=None):
        """
        Validates the serializer with the provided data and context.
        """
        assert self.serializer_class, "serializer_class must be defined"

        serializer = self.serializer_class(
            data=self.request.data,
            context=self.get_serializer_context(),
            instance=instance,
        )
        serializer.is_valid(raise_exception=True)
        return serializer

    def get_serializer_context(self):
        """
        Provides context for the serializer, including the current request.
        """
        return {"request": self.get_request()}

    def adopt_sync_action_class(self, instance):
        """
        Executes a synchronous action class if defined and returns the result.
        """
        assert self.sync_action_class, "sync_action_class must be defined"

        success, result = self.sync_action_class(
            instance=instance, request=self.get_request()
        ).execute()

        if success:
            return self.send_response(data=result)

        return self.send_error_response(data=result)

    def get_object(self, exception=NotFound, identity="pk"):
        """
        Retrieves an object based on the identity. Raises an exception if not found.
        """
        if self.get_object_model:
            _object = self.get_object_model.objects.get_or_none(
                **{identity: self.kwargs[identity]}
            )

            if not _object:
                raise exception

            return _object

        return super().get_object()

    def choices_for_meta(self, choices: list):
        """
        Generates metadata for choices in the format {id, identity}.
        """
        from apps.BASE.helpers import get_display_name_for_slug

        return [{"id": _, "identity": get_display_name_for_slug(_)} for _ in choices]


class AppCreateAPIView(AppViewMixin, CreateAPIView):
    """
    Custom CreateAPIView that supports post-create processing.
    """
    def perform_create(self, serializer):
        """
        Saves the serializer and performs post-create actions.
        """
        instance = serializer.save()
        self.perform_post_create(instance=instance)

    def perform_post_create(self, instance):
        """
        Hook for additional operations after creating an object.
        """
        pass
