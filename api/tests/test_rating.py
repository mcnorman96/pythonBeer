from models.rating import Rating

def test_create_rating():
    rating = Rating(id=1, event_id=2, beer_id=3, user_id=4, taste=5, aftertaste=6, smell=7, design=8, score=9)
    expected = {
        'id': 1,
        'event_id': 2,
        'beer_id': 3,
        'user_id': 4,
        'taste': 5,
        'aftertaste': 6,
        'smell': 7,
        'design': 8,
        'score': 9
    }
    assert rating.to_dict() == expected
