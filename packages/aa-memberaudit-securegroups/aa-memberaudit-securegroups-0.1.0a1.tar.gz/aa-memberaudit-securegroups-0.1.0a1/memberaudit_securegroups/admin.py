from django.contrib import admin

from .models import (
    MemberAuditAssetFilter,
    MemberAuditComplianceFilter,
    MemberAuditSkillSetFilter,
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


@admin.register(MemberAuditComplianceFilter)
class MemberAuditComplianceFilterAdmin(SingletonModelAdmin):
    pass


@admin.register(MemberAuditSkillSetFilter)
class MemberAuditSkillSetFilterAdmin(admin.ModelAdmin):
    filter_horizontal = ("skill_sets",)


@admin.register(MemberAuditAssetFilter)
class MemberAuditAssetFilterAdmin(admin.ModelAdmin):
    filter_horizontal = ("assets",)
