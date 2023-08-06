from __future__ import absolute_import

import attr
import json

from enum import Enum
from datetime import datetime, timedelta
from termcolor import colored
from time_window import TimeWindow

INDENT = "\t"
DATE_FORMAT = "%Y-%m-%dT%H:%M:%SZ"


@attr.s
class DiffObj:
    """
    Diff object to pass for making comparisons
    """
    name = attr.ib()
    key = attr.ib()
    obj = attr.ib()


@attr.s
class Modification:
    before = attr.ib()
    after = attr.ib()


@attr.s
class Entry:
    key = attr.ib()
    value = attr.ib()

    def __str__(self):
        if self.key:
            return json.dumps(self.key) + ": " + \
                json.dumps(self.value, indent=INDENT)
        else:
            return json.dumps(self.value, indent=INDENT)


class Modifier(Enum):
    INFO = 0
    REMOVED = 1
    ADDED = 2
    MODIFIED = 3


class DiffType(Enum):
    LIST = 1
    OBJECT = 2


@attr.s
class Diff:
    modifier = attr.ib()
    item = attr.ib()


@attr.s
class JsonDiff:
    """
    A structure representing the differences between two Jsons
    """
    diffs = attr.ib(factory=list)
    key = attr.ib(factory=str)
    diff_type = attr.ib(default=DiffType.LIST)
    object_key = attr.ib(factory=str)

    def prepend(self, item):
        self.diffs.insert(0, item)

    def append(self, item):
        self.diffs.append(item)

    def extend(self, list):
        self.diffs.extend(list)

    def removed_items(self):
        return [x.item for x in self.diffs if x.modifier == Modifier.REMOVED]

    def added_items(self):
        return [x.item for x in self.diffs if x.modifier == Modifier.ADDED]

    def modified_items(self):
        return [x.item for x in self.diffs if x.modifier == Modifier.MODIFIED]

    def is_diff(self):
        return len(self.removed_items()) + len(self.added_items()) + \
            len(self.modified_items()) > 0

    def pretty_string(self, depth=0, outer_type=None):
        def indent(s):
            parts = s.split("\n")
            pad = INDENT * (depth + 1)

            return "\n".join([pad + p for p in parts])

        if not self.diffs:
            return ""

        opener = "[" if self.diff_type == DiffType.LIST else "{"
        closer = "]" if self.diff_type == DiffType.LIST else "}"

        ret = ""
        key = self.key[1:]
        key = key[key.rfind(".") + 1:]
        pad = INDENT * depth
        opener = f"{json.dumps(key)}: {opener}" \
            if key and outer_type == DiffType.OBJECT else opener
        ret += f"{pad}{opener}" if depth else opener
        ret += "\n"
        for diff in self.diffs:
            if diff.modifier == Modifier.REMOVED:
                ret += colored(indent(str(diff.item)), "red")
            elif diff.modifier == Modifier.ADDED:
                ret += colored(indent(str(diff.item)), "green")
            elif diff.modifier == Modifier.INFO:
                ret += indent(str(diff.item))
            else:
                ret += diff.item.pretty_string(depth + 1, self.diff_type)
            ret += ",\n"

        ret = ret[:-2] + "\n"
        ret += f"{pad}{closer}" if depth else closer

        return ret


def diff_lists_of_scalars(list1, list2, prefix=""):
    """
    Compare lists list1 and list2 and returns a delta in color coded format

    :param list list1: list of elements
    :param list list2: list of elements
    :param string prefix: the prefix of the elements in the tree

    :return: the difference in human readable color coded format
    :rtype: list
    """
    list1 = sorted(list1, key=str)
    list2 = sorted(list2, key=str)

    pointer1 = 0
    pointer2 = 0
    diffs = JsonDiff(key=prefix)
    while pointer1 < len(list1) and pointer2 < len(list2):
        item1 = str(list1[pointer1])
        item2 = str(list2[pointer2])

        if item1 < item2:
            diffs.append(Diff(Modifier.REMOVED, item1))
            pointer1 += 1
        elif item1 > item2:
            diffs.append(Diff(Modifier.ADDED, item2))
            pointer2 += 1
        else:
            pointer1 += 1
            pointer2 += 1

    if pointer1 < len(list1):
        diffs.extend([Diff(Modifier.REMOVED, x) for x in list1[pointer1:]])
    if pointer2 < len(list2):
        diffs.extend([Diff(Modifier.ADDED, x) for x in list2[pointer2:]])

    return diffs


def _append_if_modified(outer_diff, inner_diff, key=None, value=None):
    if inner_diff.is_diff():
        if key:
            inner_diff.prepend(Diff(Modifier.INFO, Entry(key, value)))
        outer_diff.append(Diff(Modifier.MODIFIED, inner_diff))


def diff_lists_of_objects(named_list1, named_list2, keys, prefix=""):
    """
    Compares two lists of dicts to find the delta

    :param DiffObj named_list1: first list of objects
    :param DiffObj named_list2: second list of objects
    :param keys: dictionary of keys
    :param prefix: current prefix (padding)
    :return: string representing the differences
    """

    key = keys[prefix]
    list1 = sorted(named_list1.obj, key=lambda x: x[key])
    list2 = sorted(named_list2.obj, key=lambda x: x[key])

    pointer1 = 0
    pointer2 = 0
    diffs = JsonDiff(key=prefix)
    while pointer1 < len(list1) and pointer2 < len(list2):
        item1 = list1[pointer1]
        item2 = list2[pointer2]

        if item1[key] < item2[key]:
            diffs.append(Diff(Modifier.REMOVED, Entry(None, item1)))
            pointer1 += 1
        elif item1[key] > item2[key]:
            diffs.append(Diff(Modifier.ADDED, Entry(None, item2)))
            pointer2 += 1
        else:
            obj1 = DiffObj(named_list1.name, named_list1.key, item1)
            obj2 = DiffObj(named_list2.name, named_list2.key, item2)
            object_diffs = diff_objects(obj1, obj2, keys, prefix)
            _append_if_modified(diffs, object_diffs, key, item1[key])
            pointer1 += 1
            pointer2 += 1

    if pointer1 < len(list1):
        diffs.extend([Diff(Modifier.REMOVED, Entry(None, x))
                      for x in list1[pointer1:]])
    if pointer2 < len(list2):
        diffs.extend([Diff(Modifier.ADDED, Entry(None, x))
                      for x in list2[pointer2:]])

    return diffs


def diff_lists(obj1, obj2, keys={}, prefix=""):
    """
    Compares two lists and returns the delta

    :param DiffObj obj1: list of objects
    :param DiffObj obj2: list of objects
    :param dict keys: key to compare on
    :param str prefix: key prefix

    :return: the delta in the objects
    :rtype: list
    """

    if not obj1.obj and not obj2.obj:
        return JsonDiff(key=prefix)
    elif not obj1.obj and obj2.obj:
        return JsonDiff([Diff(Modifier.ADDED, Entry(None, x))
                         for x in obj2.obj], prefix)
    elif obj1.obj and not obj2.obj:
        return JsonDiff([Diff(Modifier.REMOVED, Entry(None, x))
                         for x in obj1.obj], prefix)
    else:
        if isinstance(obj1.obj[0], dict):
            return diff_lists_of_objects(obj1, obj2, keys, prefix)
        else:
            return diff_lists_of_scalars(obj1.obj, obj2.obj, prefix)


def diff_objects(diff_obj1, diff_obj2, keys=None, prefix=""):  # noqa: C901
    """
    Find the delta between two dict objects. The objects assume to have the
    same types of elements

    :param DiffObj diff_obj1: objects 1 to compare as base
    :param DiffObj diff_obj2: object 2 to compare with
    :param keys: keys to compare in the json
    :param prefix: key prefix when getting object properties

    :return: the delta of the objects
    :rtype list
    """

    if keys is None:
        keys = {}
    obj1 = diff_obj1.obj
    obj2 = diff_obj2.obj

    keys1 = sorted(obj1.keys())
    keys2 = sorted(obj2.keys())

    index1 = 0
    index2 = 0
    diffs = JsonDiff(key=prefix, diff_type=DiffType.OBJECT)
    while index1 < len(keys1) and index2 < len(keys2):
        key1 = keys1[index1]
        key2 = keys2[index2]
        item1 = obj1[key1]
        item2 = obj2[key2]

        if key1 < key2:
            diffs.append(Diff(Modifier.REMOVED, Entry(key1, item1)))
            index1 += 1
        elif key1 > key2:
            diffs.append(Diff(Modifier.ADDED, Entry(key2, item2)))
            index2 += 1
        else:
            named_sub_list1 = DiffObj(diff_obj1.name, diff_obj1.key, item1)
            named_sub_list2 = DiffObj(diff_obj2.name, diff_obj2.key, item2)

            if isinstance(item1, dict):
                dict_diffs = diff_objects(named_sub_list1, named_sub_list2,
                                          keys, f"{prefix}.{key1}")
                _append_if_modified(diffs, dict_diffs)
            elif isinstance(item1, list):
                list_diffs = diff_lists(named_sub_list1, named_sub_list2,
                                        keys, f"{prefix}.{key1}")
                _append_if_modified(diffs, list_diffs)
            elif isinstance(item1, str):
                if item1.replace(diff_obj1.name, "") \
                        != item2.replace(diff_obj2.name, ""):
                    diffs.append(Diff(Modifier.REMOVED, Entry(key1, item1)))
                    diffs.append(Diff(Modifier.ADDED, Entry(key2, item2)))
            else:
                if item1 != item2:
                    diffs.append(Diff(Modifier.REMOVED, Entry(key1, item1)))
                    diffs.append(Diff(Modifier.ADDED, Entry(key2, item2)))

            index1 += 1
            index2 += 1

    if index1 < len(keys1):
        diffs.extend([Diff(Modifier.REMOVED, Entry(x, obj1[x]))
                      for x in keys1[index1:]])
    if index2 < len(keys2):
        diffs.extend([Diff(Modifier.ADDED, Entry(x, obj2[x]))
                      for x in keys2[index2:]])

    return diffs


def time_diff(date_string):
    """
    Gets the time that have elapsed between now and the supplied date string.
    The date string must be of format "%Y-%m-%dT%H:%M:%SZ"

    :param date_string: the date to find the difference between
    :return: number of days that have elapsed
    :rtype: timedelta
    """
    date = datetime.strptime(date_string, DATE_FORMAT)
    date_diff = datetime.utcnow() - date
    return date_diff


def get_comparison_windows(reference_time, window_size, compare_to):
    """
    Given a window size for a time-aggregated metric computation, and a comparison time frame for said metric,
    returns two time windows over which the metric should be computed.
    E.g., if window size is 30 days, and we would like to compare the metric today to the
    metric 7 days ago, the return value would represent the time windows: [now-37d, now-7d) and [now-30d, now)

    :param reference_time: the point in time (as a datetime) when the metric needs to be calcuated
    :param window_size: the number of days over which the metric needs to be calculated
    :param compare_to: the number of days prior to the reference_time that the metric needs to be compared to
    :return: two time windows
    :rtype: TimeWindow, TimeWindow
    """
    reference_start_time = reference_time - timedelta(days=window_size)
    previous_end_time = reference_time - timedelta(days=compare_to)
    previous_start_time = previous_end_time - timedelta(days=window_size)
    return TimeWindow(previous_start_time, previous_end_time), TimeWindow(reference_start_time, reference_time)


def relative_change(new, old):
    """
    Return the relative difference of two numbers, handling nulls and zeros appropriately.

    :param new: the new number
    :param old: the old number
    :return: the relative difference between new and old
    :rtype: float
    """
    if (new is None or old is None or old == 0):
        return None
    else:
        return (float(new-old)/old)
