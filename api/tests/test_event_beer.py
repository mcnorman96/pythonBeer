from models.event_beer import EventBeer
from datetime import datetime

def test_create_event_beer():
    added_at = datetime(2024, 1, 1, 12, 0)
    eb = EventBeer(id=1, event_id=2, beer_id=3, added_at=added_at)
    expected = {
        'id': 1,
        'event_id': 2,
        'beer_id': 3,
        'added_at': added_at,
    }
    assert eb.to_dict() == expected

