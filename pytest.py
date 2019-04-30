#pytest.py


#pytest to determine if algorithm ran correctly
#This test checks if our model spits out any extreme values

def func (Final_score):
    return (Final_score)

def test_max():
    assert func(Final_score) < 200

def test_min():
    assert func(Final_score) > 50