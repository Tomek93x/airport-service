from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APIClient
from rest_framework import status
from datetime import timedelta

from airport.models import (
    Airport,
    Route,
    AirplaneType,
    Airplane,
    Flight,
    Order,
)
from airport.serializers import AirportSerializer

AIRPORT_URL = reverse("airport:airport-list")
AIRPLANE_URL = reverse("airport:airplane-list")
FLIGHT_URL = reverse("airport:flight-list")
ORDER_URL = reverse("airport:order-list")


def sample_airport(**params):
    defaults = {
        "name": "Test Airport",
        "closest_big_city": "Test City",
    }
    defaults.update(params)
    return Airport.objects.create(**defaults)


def sample_airplane_type(name=None):
    """Create airplane type with unique name"""
    if name is None:
        import uuid
        name = f"Test Type {uuid.uuid4()}"
    return AirplaneType.objects.create(name=name)


def sample_airplane(**params):
    if "airplane_type" not in params:
        params["airplane_type"] = sample_airplane_type()
    defaults = {
        "name": "Test Airplane",
        "rows": 20,
        "seats_in_row": 6,
    }
    defaults.update(params)
    return Airplane.objects.create(**defaults)


def sample_route(**params):
    if "source" not in params:
        params["source"] = sample_airport(name="Source Airport")
    if "destination" not in params:
        params["destination"] = sample_airport(name="Destination Airport")
    defaults = {
        "distance": 1000,
    }
    defaults.update(params)
    return Route.objects.create(**defaults)


def sample_flight(**params):
    if "route" not in params:
        params["route"] = sample_route()
    if "airplane" not in params:
        params["airplane"] = sample_airplane()
    defaults = {
        "departure_time": timezone.now() + timedelta(days=1),
        "arrival_time": timezone.now() + timedelta(days=1, hours=2),
    }
    defaults.update(params)
    return Flight.objects.create(**defaults)


class UnauthenticatedAirportApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(AIRPORT_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedAirportApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpass123",
        )
        self.client.force_authenticate(self.user)

    def test_list_airports(self):
        sample_airport()
        sample_airport(name="Airport 2")

        res = self.client.get(AIRPORT_URL)

        airports = Airport.objects.all()
        serializer = AirportSerializer(airports, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["results"], serializer.data)

    def test_create_airport(self):
        payload = {
            "name": "New Airport",
            "closest_big_city": "New City",
        }
        res = self.client.post(AIRPORT_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        airport = Airport.objects.get(id=res.data["id"])
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(airport, key))


class AirplaneTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpass123",
        )
        self.client.force_authenticate(self.user)

    def test_list_airplanes(self):
        sample_airplane()
        sample_airplane(name="Airplane 2")

        res = self.client.get(AIRPLANE_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data["results"]), 2)

    def test_airplane_capacity(self):
        airplane = sample_airplane(rows=30, seats_in_row=6)
        self.assertEqual(airplane.capacity, 180)


class FlightTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpass123",
        )
        self.client.force_authenticate(self.user)

    def test_list_flights(self):
        sample_flight()
        sample_flight()

        res = self.client.get(FLIGHT_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data["results"]), 2)

    def test_filter_flights_by_source(self):
        airport1 = sample_airport(name="Warsaw")
        airport2 = sample_airport(name="New York")
        route1 = sample_route(source=airport1, destination=airport2)
        route2 = sample_route(
            source=airport2,
            destination=airport1
        )

        sample_flight(route=route1)
        sample_flight(route=route2)

        res = self.client.get(FLIGHT_URL, {"source": "Warsaw"})

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data["results"]), 1)


class OrderTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpass123",
        )
        self.client.force_authenticate(self.user)

    def test_create_order(self):
        flight = sample_flight()
        payload = {
            "tickets": [
                {"row": 1, "seat": 1, "flight": flight.id},
                {"row": 1, "seat": 2, "flight": flight.id},
            ]
        }

        res = self.client.post(ORDER_URL, payload, format="json")

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        order = Order.objects.get(id=res.data["id"])
        self.assertEqual(order.tickets.count(), 2)

    def test_list_orders_for_user(self):
        Order.objects.create(user=self.user)

        other_user = get_user_model().objects.create_user(
            username="otheruser",
            password="testpass123",
        )
        Order.objects.create(user=other_user)

        res = self.client.get(ORDER_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["count"], 1)
