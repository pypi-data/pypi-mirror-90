from django.utils import timezone

import pytest
from events.models import Event, Tag


class TestTag:
    """
    Test case for the EventTag model
    """

    def test_str_method(self):
        """
        Testing object str method by asserting against a known tag string
        """

        tag = Tag(name="Test Tag")
        assert str(tag) == "Test Tag"


class TestEvent:
    """
    Test case for the Event model
    """

    def test_str_method(self):
        """
        Testing object str method by asserting against a known title string
        """

        event = Event(title="Test Title")
        assert str(event) == "Test Title"

    @pytest.mark.django_db
    def test_get_absolute_url_method(self):
        """
        Testing the get absolute url method on the Event model
        """

        event = Event(title="Test Title", slug="test-title")
        assert event.get_absolute_url() == "/events/test-title/"


class TestEventQuerySet:
    """
    Test case for the EventQuerySet class
    """

    @pytest.mark.django_db
    def test_published_queryset(self):
        """
        Test that the .published method returns the correct queryset objects
        """

        # Should not be present in the queryset
        event_one = Event.objects.create(
            title="Event One",
            slug="event-one",
            start_at=timezone.now(),
            is_published=False,
            publish_at=timezone.now() + timezone.timedelta(hours=1),
        )
        # Should be present in the queryset
        event_two = Event.objects.create(
            title="Event Two",
            slug="event-two",
            start_at=timezone.now(),
            is_published=True,
            publish_at=timezone.now() - timezone.timedelta(hours=1),
        )

        expected_number_of_objects = 1
        assert Event.objects.published().count() == expected_number_of_objects
        assert event_two in Event.objects.published()
        assert event_one not in Event.objects.published()
