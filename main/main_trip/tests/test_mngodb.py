import pytest

from feature.nosql_mongo.mongo_trip.db_helper import db_trip


def test_record_user_input():
    line_id = 'test_csl123'
    input_text = 'I want to sleep'

    result = db_trip.record_user_input(line_id, input_text)

    assert result is True


def test_save_plan():
    line_id = 'test_csl123'
    input_text = 'I want to sleep'
    requirement = '123'
    itinerary = 123

    plan_index = db_trip.save_plan(
        line_id,
        input_text,
        requirement,
        itinerary
    )

    assert plan_index is not None
    assert isinstance(plan_index, int)
    assert plan_index > 0


if __name__ == '__main__':
    pytest.main(['-v', __file__])
