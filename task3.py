from datetime import datetime

def logger(path):
    def __logger(func):
        def wrapper(*args, **kwargs):
            call_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            function_name = func.__name__
            args_repr = [repr(a) for a in args[1:]]  # Пропускаем self
            kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
            signature = ", ".join(args_repr + kwargs_repr)
            result = func(*args, **kwargs)
            with open(path, 'a') as log_file:
                log_file.write(f"{call_time} - Called method: {function_name} with args: ({signature}) returns: {result}\n")
            return result
        return wrapper
    return __logger


class FlatIterator:
    def __init__(self, list_of_list):
        self.list_of_list = list_of_list
        self.outer_index = 0
        self.inner_index = 0

    def __iter__(self):
        self.outer_index = 0
        self.inner_index = 0
        return self

    @logger("flat_iterator.log")  
    def __next__(self):
        if self.outer_index >= len(self.list_of_list):
            raise StopIteration
        if self.inner_index >= len(self.list_of_list[self.outer_index]):
            self.outer_index += 1
            self.inner_index = 0
            return self.__next__()
        item = self.list_of_list[self.outer_index][self.inner_index]
        self.inner_index += 1
        return item


def test_1():

    list_of_lists_1 = [
        ['a', 'b', 'c'],
        ['d', 'e', 'f', 'h', False],
        [1, 2, None]
    ]

    for flat_iterator_item, check_item in zip(
            FlatIterator(list_of_lists_1),
            ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]
    ):

        assert flat_iterator_item == check_item

    assert list(FlatIterator(list_of_lists_1)) == ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]


if __name__ == '__main__':
    test_1()
