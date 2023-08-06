from boiler_plate.main import sumar

def test_sumar(a=1,b=2):
    result = sumar(a,b)
    assert result == 3