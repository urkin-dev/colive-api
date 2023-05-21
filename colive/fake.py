import django
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "system.settings")
django.setup()
from api.models import CancellationPolicy, Room, Hotel
from faker import Faker
import random

fake = Faker('ru_RU')

cities = [
    {"name": "Moscow", "id": 9213, "latitude": 55.751244, "longitude": 37.618423},
    {"name": "Saint Petersburg", "id": 124124,
        "latitude": 59.934280, "longitude": 30.335099},
    {"name": "Sochi", "id": 123213213213,
        "latitude": 43.585525, "longitude": 39.723062}
]


def create_fake_hotels(num_hotels_per_city, num_rooms_per_hotel):
    hotels = []

    for city in cities:
        city_id = city["id"]
        for _ in range(num_hotels_per_city):
            hotel = Hotel(
                name=fake.company(),
                description=fake.text(),
                address=fake.address(),
                is_favorite=fake.boolean(),
                latitude=city["latitude"] + random.uniform(-0.05, 0.05),
                longitude=city["longitude"] + random.uniform(-0.05, 0.05),
                photos=fake.image_url(),
                rating=random.uniform(0, 5),
                count_reviews=random.randint(0, 100),
                stars=random.randint(1, 5),
                check_in_time=fake.time(pattern='%H:%M'),
                check_out_time=fake.time(pattern='%H:%M'),
                cityName=city["name"],
                cityId=city_id,
                cityTimezone=fake.timezone(),
                distance=random.uniform(0, 10),
                price=random.uniform(50, 500)
            )
            hotel.save()

            for _ in range(num_rooms_per_hotel):
                cancellation_policy = CancellationPolicy(
                    free_cancellation_before=fake.future_datetime(
                        end_date='+1y'),
                    free_cancellation_possible=fake.boolean(),
                    penalty_amount=random.uniform(0, 100),
                )
                cancellation_policy.save()

                room = Room(
                    hotel=hotel,
                    name=fake.word(),
                    photos=fake.image_url(),
                    description=fake.text(),
                    limit=random.randint(1, 10),
                    children_limit=random.randint(1, 10),
                    price=random.uniform(50, 300),
                    total_price=random.uniform(50, 300),
                    meal=fake.word(),
                    cancellation_policy=cancellation_policy
                )
                room.save()

            hotels.append(hotel)

    return hotels


if __name__ == "__main__":
    num_hotels_per_city = 10
    num_rooms_per_hotel = 5
    fake_hotels = create_fake_hotels(num_hotels_per_city, num_rooms_per_hotel)
    print(f"{num_hotels_per_city} fake hotels with {num_rooms_per_hotel} rooms each have been created successfully for Moscow, Saint Petersburg, and Sochi.")
