import random

# rand_list =
def get_10_random_numbers() -> list[int]:
    return [random.randint(1, 20) for _ in range(10)]

# list_comprehension_below_10 =
def filter_numbers_below_10_using_comprehension(number_list: list[int]) -> list[int]:
    return [number for number in number_list if number > 10]

# list_comprehension_using_filter =
def filter_numbers_below_10_using_filter(number_list: list[int]) -> list[int]:
    def is_greater_than_10(n):
        return n > 10
    filtered_numbers = list(filter(is_greater_than_10, number_list))
    return filtered_numbers
