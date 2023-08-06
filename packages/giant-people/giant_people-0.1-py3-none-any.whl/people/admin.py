from django.contrib import admin

from . import models


@admin.register(models.Person)
class PersonAdmin(admin.ModelAdmin):
    """
    Admin for Person model
    """

    list_display = ["name", "linkedin_url", "job_role", "location"]
    search_fields = ["name", "location__location", "job_role__role"]
    filter_horizontal = ["tags"]
    readonly_fields = [
        "created_at",
        "updated_at",
    ]
    fieldsets = [
        (None, {"fields": ["name", "linkedin_url", "image", "popup_text"]}),
        ("Job Role", {"fields": ["job_role", "organisation_role", "programme"]}),
        ("Location", {"fields": ["location"]}),
        ("Tags", {"fields": ["tags"]}),
        ("Publish", {"fields": ["is_published", "publish_at"]}),
        ("Meta Data", {"classes": ("collapse",), "fields": ["created_at", "updated_at"]}),
    ]


@admin.register(models.Role)
class RoleAdmin(admin.ModelAdmin):
    """
    Admin for Role model
    """

    list_display = ["role_id", "role", "category"]
    search_fields = ["role_id", "role", "category"]
    readonly_fields = [
        "created_at",
        "updated_at",
    ]
    list_filter = ["role_id", "role", "category"]
    fieldsets = [
        (None, {"fields": ["role", "category", "role_id"]}),
        ("Meta Data", {"classes": ("collapse",), "fields": ["created_at", "updated_at"]}),
    ]


@admin.register(models.Location)
class LocationAdmin(admin.ModelAdmin):
    """
    Admin for Location model
    """

    list_display = ["location", "department"]
    search_fields = ["location", "department__department"]
    readonly_fields = [
        "created_at",
        "updated_at",
    ]
    list_filter = ["location", "department"]
    fieldsets = [
        (None, {"fields": ["location", "department"]}),
        ("Meta Data", {"classes": ("collapse",), "fields": ["created_at", "updated_at"]}),
    ]


@admin.register(models.Department)
class DepartmentAdmin(admin.ModelAdmin):
    """
    Admin for Department model
    """

    list_display = ["department"]
    search_fields = ["department"]
    readonly_fields = [
        "created_at",
        "updated_at",
    ]
    list_filter = ["department"]
    fieldsets = [
        (None, {"fields": ["department"]}),
        ("Meta Data", {"classes": ("collapse",), "fields": ["created_at", "updated_at"]}),
    ]
