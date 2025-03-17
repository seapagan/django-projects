"""Configure the Admin pages."""

from typing import Any

from django.apps import apps
from django.contrib import admin
from django.contrib.admin import AdminSite
from django.http import HttpRequest
from solo.admin import SingletonModelAdmin

from app.models import (
    ContactSubmission,
    GitHubStats,
    Project,
    SiteConfiguration,
    Tag,
    UserProfile,
)


class CustomAdminSite(AdminSite):
    """Customize the Admin Site."""

    def get_app_list(
        self, request: HttpRequest, app_label: str | None = None
    ) -> list[dict[str, Any]]:
        """Customize the app list to add a count."""
        app_list = super().get_app_list(request, app_label)
        for app in app_list:
            for model in app["models"]:
                model_class = apps.get_model(
                    app["app_label"], model["object_name"]
                )
                model["name"] = (
                    f"{model['name']} ({model_class.objects.count()})"
                )

        return app_list


class TagAdmin(admin.ModelAdmin[Tag]):
    """Define the admin interface for Tags."""

    list_display = ("name", "slug", "created_at")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}  # noqa: RUF012


class ProjectAdmin(admin.ModelAdmin[Project]):
    """Define the admin interface for the Projects."""

    list_display = ("id", "title", "created_at", "updated_at", "tag_list")
    date_hierarchy = "created_at"
    ordering = ("created_at",)
    search_fields = ("title", "details")
    filter_horizontal = ("tags",)
    list_filter = ("tags",)

    def tag_list(self, obj: Project) -> str:
        """Return a comma-separated list of tags."""
        return ", ".join(tag.name for tag in obj.tags.all())

    tag_list.short_description = "Tags"  # type: ignore


class ContactSubmissionAdmin(admin.ModelAdmin[ContactSubmission]):
    """Define the admin interface for Contact Submissions."""

    list_display = ("name", "email", "created_at")
    search_fields = ("name", "email", "message")
    date_hierarchy = "created_at"
    readonly_fields = ("name", "email", "message", "created_at")

    def has_add_permission(self, _request: HttpRequest) -> bool:
        """Disable add permission."""
        return False

    def has_change_permission(
        self, _request: HttpRequest, _obj: ContactSubmission | None = None
    ) -> bool:
        """Disable change permission."""
        return False


class GitHubStatsAdmin(admin.ModelAdmin[GitHubStats]):
    """Define the admin interface for GitHub Stats."""

    list_display = (
        "project",
        "stars",
        "forks",
        "open_issues",
        "open_prs",
        "last_updated",
    )
    list_filter = ("last_updated",)
    date_hierarchy = "last_updated"
    readonly_fields = (
        "project",
        "stars",
        "forks",
        "open_issues",
        "open_prs",
        "last_updated",
    )

    def has_add_permission(self, _request: HttpRequest) -> bool:
        """Disable add permission."""
        return False

    def has_change_permission(
        self, _request: HttpRequest, _obj: GitHubStats | None = None
    ) -> bool:
        """Disable change permission."""
        return False


admin_site = CustomAdminSite(name="custom_admin")

admin_site.register(UserProfile)
admin_site.register(Project, ProjectAdmin)
admin_site.register(Tag, TagAdmin)
admin_site.register(GitHubStats, GitHubStatsAdmin)
admin_site.register(SiteConfiguration, SingletonModelAdmin)
admin_site.register(ContactSubmission, ContactSubmissionAdmin)
