import datetime
import pytest
import road_sweeper


class TestRoadSweeper:
    def test_days_until_next(self):
        assert road_sweeper.days_until_next(1, 5) == 4

    def test_days_until_next_dest_gt_src(self):
        assert road_sweeper.days_until_next(5, 1) == 3

    def test_days_until_next_if_equal(self):
        assert road_sweeper.days_until_next(5, 5) == 0

    @pytest.mark.parametrize("year,month,expected", [(2023, 1, 6), (2023, 2, 3), (2023, 3, 3), (2023, 4, 7), (2023, 5, 5), (2023, 6, 2), (2023, 7, 7), (2023, 8, 4), (2023, 9, 1), (2023, 10, 6), (2023, 11, 3), (2023, 12, 1)])
    def test_first_friday_of_the_month(self, year, month, expected):
        assert road_sweeper.first_friday_date_of_month(year, month) == datetime.date(year, month, expected)
