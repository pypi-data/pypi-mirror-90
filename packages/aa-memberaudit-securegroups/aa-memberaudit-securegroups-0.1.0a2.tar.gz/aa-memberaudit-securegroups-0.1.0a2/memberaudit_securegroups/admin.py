import humanize

from django.contrib import admin

from .models import (
    ActivityFilter,
    AgeFilter,
    AssetFilter,
    ComplianceFilter,
    SkillPointFilter,
    SkillSetFilter,
)


class SingletonModelAdmin(admin.ModelAdmin):
    """
    Prevents Django admin users deleting the singleton or adding extra rows.
    """

    actions = None  # Removes the default delete action.

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return self.model.objects.all().count() == 0


@admin.register(ActivityFilter)
class ActivityFilterAdmin(admin.ModelAdmin):
    list_display = ("description", "_inactivity_threshold")

    def _inactivity_threshold(self, obj):
        return "%(duration)i days" % {"duration": obj.inactivity_threshold}


@admin.register(AgeFilter)
class AgeFilterAdmin(admin.ModelAdmin):
    list_display = ("description", "_age_threshold")

    def _age_threshold(self, obj):
        return "%(duration)i days" % {"duration": obj.age_threshold}


@admin.register(AssetFilter)
class AssetFilterAdmin(admin.ModelAdmin):
    list_display = ("description",)
    filter_horizontal = ("assets",)


@admin.register(ComplianceFilter)
class ComplianceFilterAdmin(SingletonModelAdmin):
    list_display = ("description",)


@admin.register(SkillPointFilter)
class SkillPointFilterAdmin(admin.ModelAdmin):
    list_display = ("description", "_skill_point_threshold")

    def _skill_point_threshold(self, obj):
        return "%(skill_points)s skill points" % {
            "skill_points": humanize.intword(obj.skill_point_threshold)
        }


@admin.register(SkillSetFilter)
class SkillSetFilterAdmin(admin.ModelAdmin):
    list_display = ("description",)
    filter_horizontal = ("skill_sets",)
