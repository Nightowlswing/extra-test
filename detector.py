from tools import get
import orjson as json
import asyncio

sports = [6, 8, 4, 20, 13, 29, 2, 1, 14, 7, 11, 21, 9, 36, 24, 5, 16, 15, 12]


class ExtraDetector:
    loop = asyncio.get_event_loop()

    @staticmethod
    async def fetch() -> list:
        data = []
        for sport in sports:
            res = await get(f'http://51.15.66.141:5000/odds/1xbet/live/events?sport_id={sport}')
            data.append((sport, json.loads(res)))
        return data

    @staticmethod
    def filter_events(sports) -> list:
        result = []
        for sport in sports:
            result.append((sport[0], [(event['home'], event['away']) for event in sport[1] if
                           event['period_name'] == 'Extra-Time']))
        return result

    def get_extra(self):
        data = self.loop.run_until_complete(ExtraDetector.fetch())
        return ExtraDetector.filter_events(data)
