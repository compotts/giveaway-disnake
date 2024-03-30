import datetime
from db import Example


class GiveawayRepository:
    def __init__(self):
        pass

    async def example_create(self, name: str):
        example = await Example.objects.create(
            name=name
        )
        return example
        print('SUCCESS')