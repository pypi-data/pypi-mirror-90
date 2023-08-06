#!/usr/bin/env python
# -*- coding: utf-8 -*-

###################
#    This package implement an ordered dict.
#    Copyright (C) 2020  Maurice Lambert

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
###################

"""
    This package implement an ordered dict.
"""


class OrdDict:
    def __init__(self, *args, **kwargs):
        self.keys_ = []
        self.values_ = []
        for arg in args:
            self.update(arg)
        self.update(kwargs)

    def __setitem__(self, item, value):
        try:
            self[item]
        except ValueError:
            self.keys_.append(item)
            self.values_.append(value)
        else:
            self.modify(item, value)

    def __getitem__(self, item):
        return self.values_[self.keys_.index(item)]

    def __len__(self):
        return len(self.keys_)

    def __str__(self):
        return str(self.to_dict())

    def __repr__(self):
        return repr(self.to_dict())

    def __eq__(self, other):
        return self.values_ == other.values_ and self.keys_ == other.keys_

    def __contains__(self, item):
        return item in self.keys_

    def __add__(self, dict_):
        copy = self.copy()
        copy.update(dict_)
        return copy

    def __delitem__(self, item):
        self.delete(item)

    def __iadd__(self, dict_):
        return self.__add__(dict_)

    def __ne__(self, other):
        return self.values_ != other.values_ or self.keys_ != other.keys_

    def __reversed__(self):
        for key in self.keys_[::-1]:
            yield key, self[key]

    def __or__(self, other):
        return len(self) or other

    def __ror__(self, other):
        return len(self) or other

    def __next__ (self):
        yield from self.keys_

    def __iter__ (self):
        yield from self.keys_

    def to_dict(self):
        return dict(zip(self.keys_, self.values_))

    def add(self, item, value):
        self[item] = value

    def insert(self, index, item, value):
        try:
            self[item]
        except ValueError:
            self.keys_.insert(index, item)
            self.values_.insert(index, value)
        else:
            self.deplace(index, item)
            self.modify(item, value)

    def modify(self, item, value):
        index = self.keys_.index(item)
        self.values_[index] = value

    def deplace(self, index, item):
        value = self[item]
        self.delete(item)
        self.insert(index, item, value)

    def delete(self, item):
        index = self.keys_.index(item)
        self.delete_from_index(index)

    def values(self):
        for value in self.values_:
            yield value

    def keys(self):
        for key in self.keys_:
            yield key

    def items(self):
        for i in range(len(self)):
            yield self.keys_[i], self.values_[i]

    def get(self, item):
        if item in self.keys_:
            return self.values_[self.keys_.index(item)]

    def setdefault(self, item, value):
        value_ = self.get(item)
        if not value_:
            self[item] = value
            value_ = value
        return value_

    def index(self, item):
        return self.keys_.index(item)

    def index_from_value(self, value):
        return self.values_.index(value)

    def value_from_index(self, index):
        return self.values_[index]

    def key_from_index(self, index):
        return self.keys_[index]

    def get_from_index(self, index):
        return self.keys_[index], self.values_[index]

    def remove(self, index):
        del self.keys_[index]
        del self.values_[index]

    def reverse(self):
        self.keys_.reverse()
        self.values_.reverse()

    def copy(self):
        ord_dict = OrdDict()
        ord_dict.values_ = self.values_.copy()
        ord_dict.keys_ = self.keys_.copy()
        return ord_dict

    def update(self, dict_):
        for key, value in dict_.items():
            self[key] = value

    def get_key_from_value(self, value):
        return self.keys_[self.values_.index(value)]

    def delete_from_index(self, index):
        del self.keys_[index]
        del self.values_[index]

    def clear(self):
        self.keys_.clear()
        self.values_.clear()

    def count(self, value):
        return self.values_.count(value)

    def extend(self, dict_):
        for key, value in dict_.items():
            self.setdefault(key, value)

    def pop(self, item):
        value = self[item]
        self.delete(item)
        return value

    def pop_from_index(self, index):
        item = self.keys_[index]
        value = self[item]
        self.delete_from_index(index)
        return item, value

    def sort(self):
        v = self.values_.copy()
        k = self.keys_.copy()

        self.keys_.sort()

        for i, key in enumerate(k):
            index = self.keys_.index(key)
            self.values_[index] = v[i]

    def sort_by_values(self):
        v = self.values_.copy()
        k = self.keys_.copy()

        self.values_.sort()
        indexs = []

        for i, value in enumerate(v):
            index = self.values_.index(value)
            while index in indexs:
                index = self.values_.index(value, index + 1)
            indexs.append(index)
            self.keys_[index] = k[i]


if __name__ == "__main__":
    my_ord_dict = OrdDict(key1="value1")
    my_ord_dict["key3"] = "value3"
    my_ord_dict.insert(1, "key2", "value2")

    assert my_ord_dict["key1"] == "value1"
    assert my_ord_dict["key2"] == "value2"
    assert my_ord_dict["key3"] == "value3"
    assert my_ord_dict.keys_[1] == "key2"
    assert my_ord_dict.values_[1] == "value2"

    assert my_ord_dict.to_dict() == {
        "key1": "value1",
        "key2": "value2",
        "key3": "value3",
    }

    my_ord_dict.deplace(1, "key3")

    assert my_ord_dict.keys_[1] == "key3"
    assert my_ord_dict.values_[1] == "value3"
    assert my_ord_dict.keys_[2] == "key2"
    assert my_ord_dict.values_[2] == "value2"

    my_ord_dict.delete("key3")

    assert my_ord_dict.keys_[1] == "key2"
    assert my_ord_dict.values_[1] == "value2"
    assert len(my_ord_dict) == 2

    my_ord_dict["key2"] = "value3 (feinte)"

    assert my_ord_dict["key2"] == "value3 (feinte)"

    my_ord_dict.insert(0, "key2", "value2")

    assert my_ord_dict["key2"] == "value2"
    assert my_ord_dict.keys_[0] == "key2"
    assert my_ord_dict.values_[0] == "value2"
    assert len(my_ord_dict) == 2
    assert my_ord_dict["key1"] == "value1"
    assert my_ord_dict.keys_[1] == "key1"
    assert my_ord_dict.values_[1] == "value1"

    my_ord_dict.update({"key3": "value3"})

    assert len(my_ord_dict) == 3
    assert my_ord_dict["key3"] == "value3"
    assert my_ord_dict.keys_[2] == "key3"
    assert my_ord_dict.values_[2] == "value3"

    for i, value in enumerate(my_ord_dict.values()):
        assert value == my_ord_dict.values_[i]

    for i, key in enumerate(my_ord_dict.keys()):
        assert key == my_ord_dict.keys_[i]

    for i, (key, value) in enumerate(my_ord_dict.items()):
        assert key == my_ord_dict.keys_[i]
        assert value == my_ord_dict.values_[i]
        assert value == my_ord_dict[key]

    assert "value3" == my_ord_dict.get("key3")
    assert my_ord_dict.get("key4") is None

    assert "value3" == my_ord_dict.setdefault("key3", "value4")
    assert "value4" == my_ord_dict.setdefault("key4", "value4")

    assert 3 == my_ord_dict.index("key4")
    assert 3 == my_ord_dict.index_from_value("value4")

    assert "value4" == my_ord_dict.value_from_index(3)
    assert "key4" == my_ord_dict.key_from_index(3)
    assert ("key4", "value4") == my_ord_dict.get_from_index(3)

    my_ord_dict.remove(3)

    assert len(my_ord_dict) == 3
    assert "key4" not in my_ord_dict.keys_
    assert "value4" not in my_ord_dict.values_

    my_ord_dict.reverse()

    assert "value3" == my_ord_dict.values_[0]
    assert "key3" == my_ord_dict.keys_[0]
    assert "value2" == my_ord_dict.values_[2]
    assert "key2" == my_ord_dict.keys_[2]

    assert my_ord_dict == my_ord_dict.copy()
    assert my_ord_dict is not my_ord_dict.copy()

    assert "key3" == my_ord_dict.get_key_from_value("value3")

    assert "key4" not in my_ord_dict
    assert "key3" in my_ord_dict
    assert "value3" not in my_ord_dict

    my_ord_dict = my_ord_dict + {"key4": "value4"}
    my_ord_dict += {"key4": "value4"}

    assert my_ord_dict["key4"] == "value4"
    assert my_ord_dict.keys_[3] == "key4"
    assert my_ord_dict.values_[3] == "value4"

    del my_ord_dict["key4"]

    assert my_ord_dict.get("key4") is None
    assert "key4" not in my_ord_dict
    assert "key4" not in my_ord_dict.keys_
    assert "value4" not in my_ord_dict.values_

    my_ord_dict2 = my_ord_dict.copy()
    my_ord_dict2["key1"] = "value"

    assert my_ord_dict2 != my_ord_dict

    my_ord_dict2 = my_ord_dict.copy()
    my_ord_dict2.keys_[0] = "keys"

    assert my_ord_dict2 != my_ord_dict

    my_ord_dict2 = my_ord_dict.copy()
    my_ord_dict2.reverse()

    assert my_ord_dict2 != my_ord_dict

    for i, a in enumerate(reversed(my_ord_dict)):
        assert my_ord_dict2.get_from_index(i) == a

    my_ord_dict2.delete_from_index(0)

    assert len(my_ord_dict2) == 2
    assert my_ord_dict2.keys_[0] == "key1"
    assert "key3" not in my_ord_dict2.keys_[0]

    my_ord_dict2.clear()

    assert len(my_ord_dict2) == 0

    my_ord_dict2 = my_ord_dict.copy()
    my_ord_dict2["key1"] = "value2"

    assert my_ord_dict2.count("value2") == 2
    assert my_ord_dict2.count("value1") == 0

    my_ord_dict2.extend({"key1": "value1", "key5": "value5"})

    assert my_ord_dict2["key1"] != "value1"
    assert my_ord_dict2["key5"] == "value5"

    assert my_ord_dict2.pop("key1") == "value2"
    assert len(my_ord_dict2) == 3
    assert "key1" not in my_ord_dict2

    assert my_ord_dict2.pop_from_index(0) == ("key3", "value3")
    assert len(my_ord_dict2) == 2
    assert "key3" not in my_ord_dict2

    my_ord_dict2.add("key3", "value3")

    assert "key3" in my_ord_dict2
    assert "value3" == my_ord_dict2["key3"]

    my_ord_dict2 = OrdDict(
        {"key1": "value1", "key2": "value2"}, {"key3": "value3"}, key4="value4"
    )

    assert "key3" in my_ord_dict2
    assert "value3" == my_ord_dict2["key3"]
    assert len(my_ord_dict2) == 4
    assert ("key4", "value4") == my_ord_dict2.get_from_index(3)
    assert "value4" == my_ord_dict2.value_from_index(3)
    assert "key4" == my_ord_dict2.key_from_index(3)

    my_ord_dict2 = OrdDict(c="a", b="b", a="c", d="a")
    my_ord_dict2.sort()

    assert my_ord_dict2.index("a") == 0
    assert my_ord_dict2.index("b") == 1
    assert my_ord_dict2.index("c") == 2

    my_ord_dict2.sort_by_values()

    assert my_ord_dict2.index("a") == 3
    assert my_ord_dict2.index("b") == 2
    assert (my_ord_dict2.index("c") == 0 or my_ord_dict2.index("c") == 1) and (
        my_ord_dict2.index("d") == 0 or my_ord_dict2.index("d") == 1
    )

    for a in my_ord_dict2:
        assert a in my_ord_dict2.keys_