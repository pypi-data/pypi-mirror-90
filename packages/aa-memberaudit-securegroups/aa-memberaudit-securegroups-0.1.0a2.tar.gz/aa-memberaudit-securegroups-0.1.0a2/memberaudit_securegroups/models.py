import datetime

import humanize

from django.contrib.auth.models import User
from django.core.cache import cache
from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from allianceauth.authentication.models import CharacterOwnership

from eveuniverse.models import EveType
from memberaudit.models import Character, CharacterAsset, SkillSet


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

    description = models.CharField(
        max_length=500, help_text="The filter description that is shown to end users."
    )  # this is what is shown to the user

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.name}: {self.description}"

    @property
    def name(self):
        return "Compliance"

    def process_filter(
        self, user: User
    ):  # this is the check run against a users characters
        raise NotImplementedError("Please Create a filter!")


class ActivityFilter(BaseFilter):
    inactivity_threshold = models.PositiveIntegerField(
        help_text=_("Maximum allowable inactivity, in <strong>days</strong>."),
    )

    @property
    def name(self):
        return f"Activity [days={self.inactivity_threshold}]"

    def process_filter(self, user: User):
        threshold_date = datetime.datetime.now(
            datetime.timezone.utc
        ) - datetime.timedelta(days=self.inactivity_threshold)
        return Character.objects.filter(
            Q(character_ownership__user=user),
            Q(online_status__last_login__gt=threshold_date)
            | Q(online_status__last_logout__gt=threshold_date),
        ).count()


class AgeFilter(BaseFilter):

    age_threshold = models.PositiveIntegerField(
        help_text=_("Minimum allowable age, in <strong>days</strong>."),
    )

    @property
    def name(self):
        return f"Member Audit Age [days={self.age_threshold}]"

    def process_filter(self, user: User):
        threshold_date = datetime.datetime.now(
            datetime.timezone.utc
        ) - datetime.timedelta(days=self.age_threshold)
        return (
            Character.objects.filter(
                character_ownership__user=user, details__birthday__lt=threshold_date
            ).count()
            > 0
        )


class AssetFilter(BaseFilter):

    assets = models.ManyToManyField(
        EveType,
        help_text=_("User must possess <strong>one</strong> of the selected assets."),
    )

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


class ComplianceFilter(BaseFilter, SingletonModel):
    def process_filter(self, user: User):
        return (
            CharacterOwnership.objects.filter(user=user).count() > 0
            and CharacterOwnership.objects.filter(
                user=user, memberaudit_character=None
            ).count()
            == 0
        )


class SkillPointFilter(BaseFilter):

    skill_point_threshold = models.PositiveBigIntegerField(
        help_text=_("Minimum allowable skillpoints."),
    )

    @property
    def name(self):
        return f"Member Audit Skill Points [sp={humanize.intword(self.skill_point_threshold)}]"

    def process_filter(self, user: User):
        return (
            Character.objects.filter(
                skillpoints__total__gt=self.skill_point_threshold
            ).count()
            > 0
        )


class SkillSetFilter(BaseFilter):

    skill_sets = models.ManyToManyField(
        SkillSet,
        help_text=_(
            "Users must possess all of the skills in <strong>one</strong> of the selected skillsets."
        ),
    )

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
