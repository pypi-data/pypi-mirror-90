from memberaudit.models import Character, CharacterAsset, SkillSet

from django.contrib.auth.models import User
from django.core.cache import cache
from django.db import models
from django.utils.translation import gettext_lazy as _

from allianceauth.authentication.models import CharacterOwnership
from eveuniverse.models import EveType


class SingletonModel(models.Model):
    class Meta:
        abstract = True

    def delete(self, *args, **kwargs):
        pass

    def set_cache(self):
        cache.set(self.__class__.__name__, self)

    def save(self, *args, **kwargs):
        self.pk = 1
        super(SingletonModel, self).save(*args, **kwargs)

        self.set_cache()

    @classmethod
    def load(cls):
        if cache.get(cls.__name__) is None:
            obj, created = cls.objects.get_or_create(pk=1)
            if not created:
                obj.set_cache()
        return cache.get(cls.__name__)


class BaseFilter(models.Model):

    description = models.CharField(max_length=500)  # this is what is shown to the user

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.name}: {self.description}"

    @property
    def name(self):
        return "Member Audit Compliance"

    def process_filter(
        self, user: User
    ):  # this is the check run against a users characters
        raise NotImplementedError("Please Create a filter!")


class MemberAuditComplianceFilter(BaseFilter, SingletonModel):
    class Meta:
        verbose_name = "compliance filter"
        verbose_name_plural = "compliance filters"

    def process_filter(self, user: User):
        return (
            CharacterOwnership.objects.filter(
                user=user, memberaudit_character=None
            ).count()
            == 0
        )


class MemberAuditSkillSetFilter(BaseFilter):

    skill_sets = models.ManyToManyField(
        SkillSet,
        help_text=_(
            "Users must possess all of the skills in <strong>one</strong> of the selected skillsets."
        ),
    )

    class Meta:
        verbose_name = "skill set filter"
        verbose_name_plural = "skill set filters"

    @property
    def name(self):
        return "Member Audit Skill Set"

    def process_filter(self, user: User):
        characters = Character.objects.filter(character_ownership__user=user)
        for character in characters:
            for check in character.skill_set_checks.filter(
                skill_set__in=self.skill_sets.all()
            ):
                if check.failed_required_skills.count() == 0:
                    return True
        return False


class MemberAuditAssetFilter(BaseFilter):

    assets = models.ManyToManyField(
        EveType,
        help_text=_("User must possess <strong>one</strong> of the selected assets"),
    )

    class Meta:
        verbose_name = "asset filter"
        verbose_name_plural = "asset filters"

    @property
    def name(self):
        return "Member Audit Asset"

    def process_filter(self, user: User):
        characters = Character.objects.filter(character_ownership__user=user)
        return (
            CharacterAsset.objects.filter(
                character__in=characters, eve_type__in=self.assets.all()
            ).count()
            > 0
        )
