#pytest.py


#pytest to determine if algorithm ran correctly
#This test checks if our model spits out any extreme values

from Freestyle_final import Final_score

def test_max():
    assert Final_score < 200

def test_min():
    assert Final_score > 50
