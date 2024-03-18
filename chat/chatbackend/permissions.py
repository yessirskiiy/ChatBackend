from rest_framework import permissions


class IsDialogParticipant(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user or obj.author == request.user


class CanAccessMessage(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user
