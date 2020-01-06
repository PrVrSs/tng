import collections


class ListIterator(collections.Iterator):
    def __init__(self, collection, cursor):
        self._collection = collection
        self._cursor = cursor

    def __next__(self):
        if self._cursor + 1 >= len(self._collection):
            raise StopIteration()
        self._cursor += 1
        return self._collection[self._cursor]


class ListCollection(collections.Iterable):
    def __init__(self, collection):
        self._collection = collection

    def __iter__(self):
        return ListIterator(self._collection, -1)


def main():
    collection = [1, 2, 5, 6, 8]
    aggregate = ListCollection(collection)

    for item in aggregate:
        print(item)


if __name__ == "__main__":
    main()
