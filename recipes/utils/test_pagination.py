from unittest import TestCase
from recipes.utils.make_pagination import (make_pagination_range,
                                           make_pagination_size)
SIZE = make_pagination_size(20)


class PaginationTest(TestCase):
    def test_make_pagination_range_returns_pagination_range(self):
        pagination = make_pagination_range(
            page_range=SIZE,
            qty_pages=4,
            current_page=1
        )['pagination']
        self.assertEqual([1, 2, 3, 4], pagination)

    def test_first_range_stay_static_if_current_page_is_less_than_middle_page(self):  # noqa: E501
        # * Current Page = 2; Qty Pages = 4; Middle Page = 2
        pagination = make_pagination_range(
            page_range=SIZE,
            qty_pages=4,
            current_page=2
        )['pagination']
        self.assertEqual([1, 2, 3, 4], pagination)

        # * Current Page = 3; Qty Pages = 4; Middle Page = 2
        # ! Here range should change
        pagination = make_pagination_range(
            page_range=SIZE,
            qty_pages=4,
            current_page=3
        )['pagination']
        self.assertEqual([2, 3, 4, 5], pagination)

    def test_make_sure_middle_range_is_correct(self):
        # * Current Page = 10; Qty Pages = 4; Middle Page = 2
        pagination = make_pagination_range(
            page_range=SIZE,
            qty_pages=4,
            current_page=10
        )['pagination']
        self.assertEqual([9, 10, 11, 12], pagination)

        # * Current Page = 14; Qty Pages = 4; Middle Page = 2
        pagination = make_pagination_range(
            page_range=SIZE,
            qty_pages=4,
            current_page=14
        )['pagination']
        self.assertEqual([13, 14, 15, 16], pagination)

    def test_make_pagination_range_stay_static_when_last_page_is_close(self):
        # * Current Page = 18; Qty Pages = 4; Middle Page = 2
        pagination = make_pagination_range(
            page_range=SIZE,
            qty_pages=4,
            current_page=18
        )['pagination']
        self.assertEqual([17, 18, 19, 20], pagination)

        # * Current Page = 19; Qty Pages = 4; Middle Page = 2
        pagination = make_pagination_range(
            page_range=SIZE,
            qty_pages=4,
            current_page=19
        )['pagination']
        self.assertEqual([17, 18, 19, 20], pagination)

        # * Current Page = 20; Qty Pages = 4; Middle Page = 2
        pagination = make_pagination_range(
            page_range=SIZE,
            qty_pages=4,
            current_page=20
        )['pagination']
        self.assertEqual([17, 18, 19, 20], pagination)

        # * Current Page = 21; Qty Pages = 4; Middle Page = 2
        pagination = make_pagination_range(
            page_range=SIZE,
            qty_pages=4,
            current_page=21
        )['pagination']
        self.assertEqual([17, 18, 19, 20], pagination)
