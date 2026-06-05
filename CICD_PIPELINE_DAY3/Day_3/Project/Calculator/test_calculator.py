from calculator import add, subtract

def test_add():
    assert add(4,5)==9 # asserts whether true or false
    assert add(4,3)==7
    assert subtract(5,3)==2