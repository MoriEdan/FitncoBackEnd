# -*- coding: utf-8 -*-
def get_nested_values_by_key(key, data):
    # https://stackoverflow.com/questions/9807634/find-all-occurrences-of-a-key-in-nested-python-dictionaries-and-lists

    # data dict içerisindeki key'lerden recursive olarak key değeri X'e eşit olan value'ları getirir

    """
        data = { "id" : "abcde",
            "key1" : "blah",
            "key2" : "blah blah",
            "nestedlist" : [
            { "id" : "qwerty",
                "nestednestedlist" : [
                { "id" : "xyz", "keyA" : "blah blah blah" },
                { "id" : "fghi", "keyZ" : "blah blah blah" }],
                "anothernestednestedlist" : [
                { "id" : "asdf", "keyQ" : "blah blah" },
                { "id" : "yuiop", "keyW" : "blah" }] } ] }

        get_nested_values_by_key("id", data)

        ['abcde', 'qwerty', 'xyz', 'fghi', 'asdf', 'yuiop']
    """

    if hasattr(data, 'iteritems'):
        for k, v in data.iteritems():
            if k == key:
                yield v
            if isinstance(v, dict):
                for result in get_nested_values_by_key(key, v):
                    yield result
            elif isinstance(v, list):
                for d in v:
                    for result in get_nested_values_by_key(key, d):
                        yield result


def get_value(key, data, default_value=None):
    if key in data:
        return data[key]

    return default_value
