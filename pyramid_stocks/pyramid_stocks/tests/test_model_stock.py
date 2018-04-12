def test_constructed_stock_correct_username(db_session):
    from ..models import Stock

    assert len(db_session.query(Stock).all()) == 0
    stock = Stock(symbol='fake')
    db_session.add(stock)
    assert len(db_session.query(Stock).all()) == 1
'''
def test_create_stock_without_symbol(db_session):
    from ..models import Stock
    import pytest

    with pytest.raises(Exception):
        stock = Stock()
''' 
def test_duplicate(db_session):
    from sqlalchemy.exc import IntegrityError
    import pytest
    from ..models import Stock
    stock = Stock(symbol='fake')
    stock_two = Stock(symbol='fake')
    db_session.add(stock)
    db_session.commit()
    with pytest.raises(IntegrityError):
        db_session.add(stock_two)
        db_session.flush()
