from rest_framework.permissions import BasePermission, SAFE_METHODS


class PermanentJobPostingPermission(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.groups.filter(
                name__iexact="job posting (permanent)"
            ).exists()
        )


class TemporaryJobPostingPermission(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.groups.filter(
                name__iexact="job posting (temporary)"
            ).exists()
        )


class ApplicantScrutiny(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.groups.filter(name__iexact="applicant scrutiny").exists()
        )


class Management(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.groups.filter(name__iexact="management").exists()
        )


class TraineePermission(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.groups.filter(name__iexact="trainee").exists()
        )


class MasterDataPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.method in SAFE_METHODS
            or request.user.groups.filter(name__iexact="admin").exists()
            or request.user.is_superuser
        )


class ApplicantPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.groups.filter(
            name__iexact="applicant"
        )
