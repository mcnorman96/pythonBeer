from models.beer import Beer

def test_create_beer():
    beer = Beer(id=1, name='Test', description='Desc', brewery='Brew', type='Lager')
    expected = {
        'id': 1,
        'name': 'Test',
        'description': 'Desc',
        'brewery': 'Brew',
        'type': 'Lager'
    }
    assert beer.to_dict() == expected
