import django
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "system.settings")
django.setup()
from api.models import Place, Room, Tag, CancellationPolicy
from random import uniform, randint
from django.utils.crypto import get_random_string
from faker import Faker

fake = Faker()

# Generate 10 hotels
for _ in range(10):
    # Create a new place
    place = Place.objects.create(
        name=fake.company(),
        description=fake.paragraph(),
        address=fake.address(),
        latitude=uniform(55.75, 55.85),  # Increased latitude range
        longitude=uniform(37.60, 37.70),  # Increased longitude range
        photos=fake.image_url(),
        stars=randint(1, 5),
        check_in_time='14:00',
        check_out_time='12:00',
        cityName='Москва',
        cityId=1,
        cityTimezone='Europe/Moscow',
        price=fake.pydecimal(left_digits=4, right_digits=2, positive=True),
    )

    # Add the "Отель" tag to the place
    tag_otel, _ = Tag.objects.get_or_create(name='Отель')
    place.tags.add(tag_otel)

    # Generate two rooms for each hotel
    for _ in range(2):
        room = Room.objects.create(
            name=fake.word(),
            photos=fake.image_url(),
            description=fake.paragraph(),
            limit=randint(1, 10),
            children_limit=randint(1, 10),
            price=fake.pydecimal(left_digits=4, right_digits=2, positive=True),
            total_price=fake.pydecimal(left_digits=4, right_digits=2, positive=True),
            meal=fake.word(),
            place=place,
            cancellation_policy=CancellationPolicy.objects.create(
                free_cancellation_before=fake.future_datetime(),
                free_cancellation_possible=fake.boolean(),
                penalty_amount=fake.pydecimal(left_digits=4, right_digits=2, positive=True),
            ),
        )

# Generate 6 places with the "Отель" tag
for _ in range(6):
    place = Place.objects.create(
        name=fake.company(),
        description=fake.paragraph(),
        address=fake.address(),
        latitude=uniform(55.75, 55.85),  # Increased latitude range
        longitude=uniform(37.60, 37.70),  # Increased longitude range
        photos=fake.image_url(),
        stars=randint(1, 5),
        check_in_time='14:00',
        check_out_time='12:00',
        cityName='Москва',
        cityId=1,
        cityTimezone='Europe/Moscow',
        price=fake.pydecimal(left_digits=4, right_digits=2, positive=True),
    )
    place.tags.add(tag_otel)

# Generate 4 places with the "Коливинг" tag
tag_koliving, _ = Tag.objects.get_or_create(name='Коливинг')
for _ in range(4):
    place = Place.objects.create(
        name=fake.company(),
        description=fake.paragraph(),
        address=fake.address(),
        latitude=uniform(55.75, 55.85),  # Increased latitude range
        longitude=uniform(37.60, 37.70),  # Increased longitude range
        photos=fake.image_url(),
        stars=randint(1, 5),
        check_in_time='14:00',
        check_out_time='12:00',
        cityName='Москва',
        cityId=1,
        cityTimezone='Europe/Moscow',
        price=fake.pydecimal(left_digits=4, right_digits=2, positive=True),
    )
    place.tags.add(tag_koliving)
