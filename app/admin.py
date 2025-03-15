"""Configure the Admin pages."""

from typing import Any

from django.apps import apps
from django.contrib import admin
from django.contrib.admin import AdminSite
from django.http import HttpRequest

from app.models import Project, Tag, UserProfile


class CustomAdminSite(AdminSite):
    """Customize the Admin Site."""

    def get_app_list(self, request: HttpRequest) -> list[dict[str, Any]]:  # type: ignore
        """Customize the app list to add a count."""
        app_list = super().get_app_list(request)
        for app in app_list:
            for model in app["models"]:
                model_class = apps.get_model(
                    app["app_label"], model["object_name"]
                )
                model["name"] = (
                    f"{model['name']} ({model_class.objects.count()})"
                )
        return app_list


admin_site = CustomAdminSite(name="custom_admin")


class TagAdmin(admin.ModelAdmin[Tag]):
    """Define the admin interface for Tags."""

    list_display = ("name", "slug", "created_at")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}


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


admin_site.register(Project, ProjectAdmin)
admin_site.register(Tag, TagAdmin)
admin_site.register(UserProfile)
