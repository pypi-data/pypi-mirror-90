from allianceauth import hooks

from .models import (
    MemberAuditAssetFilter,
    MemberAuditComplianceFilter,
    MemberAuditSkillSetFilter,
)


@hooks.register("secure_group_filters")
def filters():
    return [
        MemberAuditComplianceFilter,
        MemberAuditSkillSetFilter,
        MemberAuditAssetFilter,
    ]
