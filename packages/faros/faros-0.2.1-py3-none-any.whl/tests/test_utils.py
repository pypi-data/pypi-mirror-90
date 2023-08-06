import unittest
from faros import utils
from datetime import datetime, timedelta
from time_window import TimeWindow


class UtilsTest(unittest.TestCase):
    def test_list_of_identical_scalars(self):
        list1 = ["a", "b", "c", "d"]
        diff = utils.diff_lists_of_scalars(list1, list1)
        self.assertFalse(diff.is_diff())

    def test_list_of_scalars_additions(self):
        list1 = ["a", "b", ]
        list2 = ["a", "b", "c", "d"]
        diff = utils.diff_lists_of_scalars(list1, list2)
        self.assertEqual(0, len(diff.removed_items()))
        self.assertEqual(2, len(diff.added_items()))

    def test_list_of_scalars_removals(self):
        list1 = ["a", "b", "c", "d"]
        list2 = ["a", ]
        diff = utils.diff_lists_of_scalars(list1, list2)
        self.assertEqual(3, len(diff.removed_items()))

    def test_list_of_scalars_mixed(self):
        list1 = [1, 2, 3, "c", "d"]
        list2 = [1, "c", "d", "e"]
        diff = utils.diff_lists_of_scalars(list1, list2)
        self.assertEqual(2, len(diff.removed_items()))
        self.assertEqual(1, len(diff.added_items()))
        self.assertEqual(["2", "3", "e"], [x.item for x in diff.diffs])

    def test_list_of_empty_scalars(self):
        list1 = []
        diff = utils.diff_lists_of_scalars(list1, list1)
        self.assertFalse(diff.is_diff())

    def test_list_of_empty_objects(self):
        list1 = utils.DiffObj("", "", [])
        diff = utils.diff_lists(list1, list1)
        self.assertFalse(diff.is_diff())

    def test_diff_lists_only_additions(self):
        list1 = utils.DiffObj("", "", [])
        list2 = utils.DiffObj("", "", [{}, {}, {}])
        diff = utils.diff_lists(list1, list2)
        self.assertEqual(3, len(diff.added_items()))

    def test_diff_lists_only_removals(self):
        list1 = utils.DiffObj("", "", [{}, {}])
        list2 = utils.DiffObj("", "", [])
        diff = utils.diff_lists(list1, list2)
        self.assertEqual(2, len(diff.removed_items()))

    def test_diff_lists_scalars(self):
        list1 = utils.DiffObj("", "", [1, 2, 3])
        list2 = utils.DiffObj("", "", [3, 4, 5])
        diff = utils.diff_lists(list1, list2)
        self.assertEqual(2, len(diff.removed_items()))
        self.assertEqual(2, len(diff.added_items()))

    def test_diff_empty_lists_of_objects(self):
        list1 = utils.DiffObj("", "", [])
        diff = utils.diff_lists_of_objects(list1, list1, {"": ""})
        self.assertFalse(diff.is_diff())

    def test_diff_lists_of_objects_only_additions(self):
        list1 = utils.DiffObj("", "", [])
        list2 = utils.DiffObj("", "", [{"key": 1}, {"key": 3}, {"key": 2}])
        diff = utils.diff_lists_of_objects(list1, list2, {"": "key"})
        self.assertEqual(3, len(diff.added_items()))

    def test_diff_lists_of_objects_only_removals(self):
        list2 = utils.DiffObj("", "", [])
        list1 = utils.DiffObj("", "", [{"key": 1}, {"key": 3}])
        diff = utils.diff_lists_of_objects(list1, list2, {"": "key"})
        self.assertEqual(2, len(diff.removed_items()))

    def test_diff_lists_of_objects_mixed(self):
        list2 = utils.DiffObj("", "", [{"key": 1}, {"key": 3, "a": 1}])
        list1 = utils.DiffObj("", "", [{"key": 1}, {"key": 3, "a": 2, "b": 3}])
        diff = utils.diff_lists_of_objects(list1, list2, {"": "key"})
        self.assertEqual(1, len(diff.modified_items()))

    def test_diff_empty_objects(self):
        obj1 = utils.DiffObj("", "", {})
        diff = utils.diff_objects(obj1, obj1)
        self.assertFalse(diff.is_diff())

    def test_diff_objects_only_additions(self):
        obj1 = utils.DiffObj("", "", {})
        obj2 = utils.DiffObj("", "", {1: 1, 2: 2, 3: 3})
        diff = utils.diff_objects(obj1, obj2)
        self.assertEqual(3, len(diff.added_items()))

    def test_diff_objects_only_removals(self):
        obj2 = utils.DiffObj("", "", {})
        obj1 = utils.DiffObj("", "", {1: 1, 2: 2})
        diff = utils.diff_objects(obj1, obj2)
        self.assertEqual(2, len(diff.removed_items()))

    def test_diff_objects_mixed(self):
        obj1 = utils.DiffObj("", "", {"b": "c", "c": "c", "d": "d"})
        obj2 = utils.DiffObj("", "", {"a": "a", "c": "c", "b": "b"})
        diff = utils.diff_objects(obj1, obj2)
        self.assertEqual(2, len(diff.removed_items()))
        self.assertEqual(2, len(diff.added_items()))

    def test_diff_complex_objects(self):
        obj1 = utils.DiffObj("", "", {"key": 1, "a": [1, 2]})
        obj2 = utils.DiffObj("", "", {"key": 1, "a": [2, 3], "b": {"key": 1}})
        diff = utils.diff_objects(obj1, obj2)
        self.assertEqual(1, len(diff.added_items()))
        self.assertEqual(1, len(diff.modified_items()))

    def test_deep_diff(self):
        obj1 = utils.DiffObj("", "", [
            {"key": 1, "a": [1, 2]},
            {"key": 3, "a": 1, "b": 2},
            {"key": 4},
            {"key": 5, "a": {"data": [{"key": 1}, {"key": 2}]}},
            {
                "key": 6,
                "groups": {"data": [{"name": "group1", "a": "a"}]},
                "mfa": {"data": [{"serial": "abc"}]}
            }])
        obj2 = utils.DiffObj("", "", [
            {"key": 1, "a": [2, 3], "b": {"key": 1}},
            {"key": 3, "a": 2},
            {"key": 2},
            {"key": 5, "a": {"data": [{"key": 3}, {"key": 2}]}},
            {
                "key": 6,
                "groups": {"data": [{"name": "group1", "a": "b"}]},
                "mfa": {"data": []}
            }])
        diff = utils.diff_lists(obj1, obj2, {"": "key", ".b": "key",
                                             ".a.data": "key",
                                             ".groups.data": "name",
                                             ".mfa.data": "serial"})
        self.assertEqual(1, len(diff.added_items()))
        self.assertEqual(1, len(diff.removed_items()))
        self.assertEqual(4, len(diff.modified_items()))
        self.assertEqual(diff.pretty_string(),
                         '[\n\t{\n\t\t\"key\": 1,\n\t\t\"a\": [\n\u001b[31m\t\t\t1\u001b[0m,\n\u001b[32m\t\t\t3\u001b[0m\n\t\t],\n\u001b[32m\t\t\"b\": {\n\t\t\t\"key\": 1\n\t\t}\u001b[0m\n\t},\n\u001b[32m\t{\n\t\t\"key\": 2\n\t}\u001b[0m,\n\t{\n\t\t\"key\": 3,\n\u001b[31m\t\t\"a\": 1\u001b[0m,\n\u001b[32m\t\t\"a\": 2\u001b[0m,\n\u001b[31m\t\t\"b\": 2\u001b[0m\n\t},\n\u001b[31m\t{\n\t\t\"key\": 4\n\t}\u001b[0m,\n\t{\n\t\t\"key\": 5,\n\t\t\"a\": {\n\t\t\t\"data\": [\n\u001b[31m\t\t\t\t{\n\t\t\t\t\t\"key\": 1\n\t\t\t\t}\u001b[0m,\n\u001b[32m\t\t\t\t{\n\t\t\t\t\t\"key\": 3\n\t\t\t\t}\u001b[0m\n\t\t\t]\n\t\t}\n\t},\n\t{\n\t\t\"key\": 6,\n\t\t\"groups\": {\n\t\t\t\"data\": [\n\t\t\t\t{\n\t\t\t\t\t\"name\": \"group1\",\n\u001b[31m\t\t\t\t\t\"a\": \"a\"\u001b[0m,\n\u001b[32m\t\t\t\t\t\"a\": \"b\"\u001b[0m\n\t\t\t\t}\n\t\t\t]\n\t\t},\n\t\t\"mfa\": {\n\t\t\t\"data\": [\n\u001b[31m\t\t\t\t{\n\t\t\t\t\t\"serial\": \"abc\"\n\t\t\t\t}\u001b[0m\n\t\t\t]\n\t\t}\n\t}\n]')  # noqa: E501

    def test_days_elapsed(self):
        now = datetime.utcnow()
        date_time1 = (now - timedelta(days=2)).strftime(utils.DATE_FORMAT)
        time_elapsed = utils.time_diff(date_time1).days
        self.assertEqual(time_elapsed, 2)

        date_time2 = now.strftime(utils.DATE_FORMAT)
        time_elapsed = utils.time_diff(date_time2).days
        self.assertTrue(time_elapsed < 1)

        date_time = (now + timedelta(minutes=2))
        date_time2 = date_time.strftime(utils.DATE_FORMAT)
        time_elapsed = utils.time_diff(date_time2).total_seconds() / 60
        self.assertTrue(time_elapsed < 2)

        date3 = now.strftime("%m/%d/%Y, %H:%M:%S")
        with self.assertRaises(ValueError) as ex:
            utils.time_diff(date3)

        self.assertIn(utils.DATE_FORMAT, str(ex.exception))

    def test_get_windows(self):
        reference_time = datetime.now()
        w1, w2 = utils.get_comparison_windows(reference_time, 30, 7)
        self.assertEqual(w1, TimeWindow(
            reference_time - timedelta(days=37), reference_time - timedelta(days=7)))
        self.assertEqual(w2, TimeWindow(
            reference_time - timedelta(days=30), reference_time))

    def test_relative_change(self):
        self.assertEqual(utils.relative_change(9, 0), None)
        self.assertEqual(utils.relative_change(9, None), None)
        self.assertEqual(utils.relative_change(None, 9), None)
        self.assertEqual(utils.relative_change(None, None), None)
        self.assertEqual(utils.relative_change(9, 18), -0.5)
        self.assertEqual(utils.relative_change(18, 9), 1)


if __name__ == '__main__':
    unittest.main()
