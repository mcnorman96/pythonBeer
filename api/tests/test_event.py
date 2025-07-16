from models.event import Event
from datetime import datetime

def test_create_event():
    start = datetime(2024, 1, 1, 12, 0)
    end = datetime(2024, 1, 2, 12, 0)
    event = Event(id=1, name='Party', start_date=start, end_date=end, description='Fun')
    expected = {
        'id': 1,
        'name': 'Party',
        'start_date': start.isoformat(),
        'end_date': end.isoformat(),
        'description': 'Fun',
    }
    assert event.to_dict() == expected
