import factory
from django.contrib.auth.models import User
from django.utils import timezone

from accounts.models import UserProfile
from checklist.models import Aircraft, Checklist, ChecklistItem, FlightSession
from logbook.models import Flight


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        skip_postgeneration_save = True

    username = factory.Sequence(lambda index: f"user_{index}")
    email = factory.LazyAttribute(lambda user: f"{user.username}@test.com")
    password = factory.PostGenerationMethodCall("set_password", "test1234")

    @factory.post_generation
    def profile(self, create, extracted, **kwargs):
        if not create:
            return
        self.save()
        UserProfile.objects.get_or_create(user=self)


class UserProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UserProfile

    user = factory.SubFactory(UserFactory)
    simbrief_pilot_id = "216664"


class AircraftFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Aircraft

    user = factory.SubFactory(UserFactory)
    name = "Fenix A320"
    icao_code = "A320"


class ChecklistFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Checklist

    aircraft = factory.SubFactory(AircraftFactory)
    name = "Before Start"
    phase = "pre-departure"
    order = 1


class ChecklistItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ChecklistItem

    checklist = factory.SubFactory(ChecklistFactory)
    action = "Parking brake"
    expected_value = "SET"
    order = 1


class FlightFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Flight

    user = factory.SubFactory(UserFactory)
    origin = "EIDW"
    destination = "LEIB"
    aircraft = "Fenix A320"
    departure_time = factory.LazyFunction(lambda: timezone.now())
    arrival_time = factory.LazyFunction(lambda: timezone.now())
    flight_level = 280
    score = 99.0
    notes = "Test flight"


class FlightSessionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = FlightSession

    user = factory.SubFactory(UserFactory)
    checklist = factory.SubFactory(ChecklistFactory)
    completed_items = []
