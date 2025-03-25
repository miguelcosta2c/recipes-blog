from typing import List, Dict, Any
import math

from django.core.paginator import Paginator, Page
from django.db.models import QuerySet
from django.http import HttpRequest
from recipes.models import Recipe  # type: ignore


def make_pagination_range(
    page_range: list | range,
    qty_pages: int,
    current_page: int,
) -> Dict[str, Any]:
    if len(page_range) < qty_pages:
        start_range = 0
        stop_range = len(page_range)
        total_pages = len(page_range)
        first_page_out_of_range = False
        last_page_out_of_range = False
        pagination = page_range
    else:
        middle_page = math.ceil(qty_pages / 2)
        start_range = current_page - middle_page
        stop_range = current_page + middle_page
        total_pages = len(page_range)

        start_range_offset = abs(start_range) if start_range < 0 else 0

        if start_range < 0:
            start_range = 0
            stop_range += start_range_offset

        if stop_range >= total_pages:
            start_range -= abs(total_pages - stop_range)

        pagination = page_range[start_range:stop_range]
        first_page_out_of_range = current_page > middle_page
        last_page_out_of_range = stop_range < total_pages

    context_pagination = {
        'pagination': pagination,
        'page_range': page_range,
        'qty_pages': qty_pages,
        'current_page': current_page,
        'total_pages': total_pages,
        'start_range': start_range,
        'stop_range': stop_range,
        'first_page_out_of_range': first_page_out_of_range,
        'last_page_out_of_range': last_page_out_of_range
    }

    return context_pagination


def make_pagination_size(size: int) -> List[int]:
    return list(range(1, size+1))


def make_pagination(
    request: HttpRequest,
    queryset: QuerySet[Recipe, Recipe] | List[Recipe],
    per_page: int,
    qty_pages: int = 4
) -> tuple[Page[Recipe], Dict[str, Any]]:
    try:
        current_page = int(request.GET.get('page', 1))
    except ValueError:
        current_page = 1

    paginator = Paginator(queryset, per_page)
    page_obj = paginator.get_page(current_page)

    pagination_range = make_pagination_range(
        paginator.page_range,
        qty_pages,
        current_page,
    )

    return page_obj, pagination_range


if __name__ == '__main__':
    print(make_pagination_range(make_pagination_size(3), 10, 2))
