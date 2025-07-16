from models.event_participant import EventParticipant

def test_create_event_participant():
    ep = EventParticipant(id=1, event_id=2, user_id=3)
    assert ep.id == 1
    assert ep.event_id == 2
    assert ep.user_id == 3
