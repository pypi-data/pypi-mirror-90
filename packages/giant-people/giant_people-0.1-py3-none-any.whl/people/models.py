from django.core.validators import URLValidator
from django.db import models

from filer.fields.image import FilerImageField

from mixins.models import PublishingMixin, PublishingQuerySetMixin, TimestampMixin


class PersonQueryset(PublishingQuerySetMixin):
    """
    Custom queryset
    """

    pass


class Person(TimestampMixin, PublishingMixin):
    """
    Represents a person object
    """

    ORGANISATION_BUSINESS = "business_team"
    ORGANISATION_CONSULTANT = "coach_consultant_team"
    ORGANISATION_EXECUTIVE = "executive_board"
    ORGANISATION_FACULTY = "faculty"
    ORGANISATION_GLOBAL = "global_partners"
    ORGANISATION_HONORARY = "honorary_president"
    ORGANISATION_CHOICES = (
        (ORGANISATION_BUSINESS, "Business Team"),
        (ORGANISATION_CONSULTANT, "Coach Consultant Team"),
        (ORGANISATION_EXECUTIVE, "Executive Board"),
        (ORGANISATION_FACULTY, "Faculty"),
        (ORGANISATION_GLOBAL, "Global Partners"),
        (ORGANISATION_HONORARY, "Honorary President"),
    )
    image = FilerImageField(related_name="person_image", null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=255)
    linkedin_url = models.URLField(
        help_text="Enter the full URL of the LinkedIn page",
        blank=True,
        validators=[
            URLValidator(
                schemes=["https"],
                regex="www.linkedin.com",
                message="Please enter the full URL of the LinkedIn page",
            )
        ],
    )
    job_role = models.ForeignKey(
        to="people.Role",
        on_delete=models.CASCADE,
        limit_choices_to={"category": "job"},
        related_name="persons_role",
        blank=True,
        null=True,
    )
    organisation_role = models.ManyToManyField(
        to="people.Role",
        limit_choices_to={"category": "organisation"},
        related_name="persons_org_role",
        blank=True,
    )
    popup_text = models.TextField(blank=True)
    programme = models.ManyToManyField(
        to="programmes.Programme", related_name="persons_programme", blank=True,
    )
    location = models.ForeignKey(
        to="people.Location",
        on_delete=models.CASCADE,
        related_name="persons_location",
        blank=True,
        null=True,
    )
    tags = models.ManyToManyField(to="tags.Tag", related_name="tag_people", blank=True)

    objects = PersonQueryset.as_manager()

    class Meta:
        verbose_name = "Person"
        verbose_name_plural = "People"
        ordering = ["name"]

    def __str__(self):
        """
        Return string representation
        """
        return self.name


class Role(TimestampMixin):
    """
    Represents a role object
    """

    CATEGORY_JOB = "job"
    CATEGORY_ORG = "organisation"
    CATEGORY_CHOICES = (
        (CATEGORY_JOB, "Job"),
        (CATEGORY_ORG, "Organisation"),
    )

    role = models.CharField(max_length=255)
    role_id = models.CharField(max_length=255)
    category = models.CharField(max_length=255, choices=CATEGORY_CHOICES)

    class Meta:
        verbose_name = "Role"
        verbose_name_plural = "Roles"
        ordering = ["role"]

    def __str__(self):
        """
        Return string representation
        """
        return self.role


class Location(TimestampMixin):
    """
    Represents a location object
    """

    location = models.CharField(max_length=255)
    department = models.ForeignKey("Department", blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = "Location"
        verbose_name_plural = "Locations"

    def __str__(self):
        """
        Return string representation
        """
        if self.department:
            return f"{self.department}, {self.location}"
        return f"{self.location}"


class Department(TimestampMixin):
    """
    Represents a department object
    """

    department = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Department"
        verbose_name_plural = "Departments"

    def __str__(self):
        """
        Return string representation
        """
        return self.department
