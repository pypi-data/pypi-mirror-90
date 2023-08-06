from allianceauth import hooks

from .models import (
    ActivityFilter,
    AgeFilter,
    AssetFilter,
    ComplianceFilter,
    SkillPointFilter,
    SkillSetFilter,
)


@hooks.register("secure_group_filters")
def filters():
    return [
        ActivityFilter,
        AgeFilter,
        AssetFilter,
        ComplianceFilter,
        SkillPointFilter,
        SkillSetFilter,
    ]
