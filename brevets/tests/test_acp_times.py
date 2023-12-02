"""
Nose tests for acp_times.py
Write your tests HERE AND ONLY HERE.
Ethan Robb
"""
from acp_times import open_time, close_time
import arrow
import nose    # Testing framework
import logging
from nose.tools import assert_equal

logging.basicConfig(format='%(levelname)s:%(message)s',
                    level=logging.WARNING)
log = logging.getLogger(__name__)

START_TIME1 = '2023-08-01T00:00' #GLOBAL

def test_control_dist_set_0():
    """
    Test for when the control distance is set to 0
    """
    # Setup
    start_time = arrow.get(START_TIME1)

    open = open_time(0, 200, start_time)
    close = close_time(0, 200, start_time)
    
    # Assert
    assert open == start_time
    assert close == start_time.shift(minutes=60)
    return

def test_open_function_regular():
    """
    Regular test cases for open_time function
    """
    # Setup
    start_time = arrow.get(START_TIME1)

    test1 = open_time(150, 200, start_time)
    test2 = open_time(300, 300, start_time)
    test3 = open_time(500, 600, start_time)

    # Assert
    assert test1 == start_time.shift(minutes=+265)
    assert test2 == start_time.shift(minutes=+540)
    assert test3 == start_time.shift(minutes=+928)
    return
    

def test_open_function_edge():
    """
    Edge test cases for open_time function
    """
    # Setup
    start_time = arrow.get(START_TIME1)

    test1 = open_time(0, 200, start_time)
    test2 = open_time(40, 200, start_time)
    
    # Assert
    assert test1 == start_time
    assert test2 == start_time.shift(minutes=+71)
    return

def test_close_function_regular():
    """
    Regular test cases for close_time function
    """
    # Setup
    start_time = arrow.get(START_TIME1)

    test1 = close_time(150, 200, start_time)
    test2 = close_time(500, 600, start_time)
    test3 = close_time(300, 300, start_time)
   
    # Assert
    assert test1 == start_time.shift(minutes=+600)
    assert test2 == start_time.shift(minutes=+2000)
    assert test3 == start_time.shift(minutes=+1200)
    return

def test_close_function_edge():
    """
    Edge test cases for close_time function
    """
    # Setup
    start_time = arrow.get(START_TIME1)

    test1 = close_time(205, 200, start_time)
    test2 = close_time(0, 200, start_time)

    # Assert
    assert test1 == start_time.shift(minutes=+800)
    assert test2 == start_time.shift(minutes=+60)
    return

def test_db_insertion():
    from flask_brevets import app, mongo

    app.testing = True
    with app.app_context():
        test_data = {"miles": 100, "km": 160.934, "location": "Test Location", "open": "2021-01-01T06:00", "close": "2021-01-01T12:00"}
        mongo.db.control_times.insert_one(test_data)

        inserted_data = mongo.db.control_times.find_one({"location": "Test Location"}, {'_id': 0})
        assert_equal(inserted_data, test_data)


def test_db_retrieval():
    from flask_brevets import app, mongo

    app.testing = True
    with app.app_context():
        test_data = {"miles": 50, "km": 80.4672, "location": "Test Retrieval", "open": "2021-01-01T03:00", "close": "2021-01-01T09:00"}
        mongo.db.control_times.insert_one(test_data)

        retrieved_data = mongo.db.control_times.find_one({"location": "Test Retrieval"}, {'_id': 0})
        assert_equal(retrieved_data, test_data)