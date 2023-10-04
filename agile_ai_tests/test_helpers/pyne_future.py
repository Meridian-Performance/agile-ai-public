import numpy as np

from pynetest.lib.matcher import EqualToMatcher, Matcher, is_matcher
from pynetest.pyne_test_collector import xit


class CustomEqualToMatcher(EqualToMatcher):
    def __init__(self, equal_to_comparator, *params):
        super().__init__("equal_to", self.comparator, *params)
        self.equal_to_comparator = equal_to_comparator

    def comparator(self, subject, *params):
        if len(params) == 0:
            self._reason = "there was nothing to compare to"
            return False
        if is_matcher(subject):
            matches = subject.matches(params[0])
            self._reason = subject.reason()
            return matches
        elif is_matcher(params[0]):
            matches = params[0].matches(subject)
            self._reason = params[0].reason()
            return matches
        else:
            return self.equal_to_comparator(subject, params[0])


class ExactlyEqualToArrayMatcher(Matcher):
    def __init__(self, *params):
        super().__init__("exactly_equal_to", self.equal_to_comparator, *params)

    def equal_to_comparator(self, a, b):
        a = np.asarray(a)
        b = np.asarray(b)
        if a.shape != b.shape:
            return False
        return np.isclose(a, b, atol=0, rtol=0, equal_nan=True).all()


class CloseToArrayMatcher(Matcher):
    def __init__(self, *params):
        super().__init__("closely_equal_to", self.equal_to_comparator, *params)

    def equal_to_comparator(self, a, b):
        a = np.asarray(a)
        b = np.asarray(b)
        if a.shape != b.shape:
            return False
        return np.isclose(a, b, equal_nan=True).all()


class TrueByPredicate(Matcher):
    def __init__(self, *params, predicate=lambda: False, display_string="true_by_predicate"):
        self.predicate = predicate
        super().__init__(display_string, self.predicate, *params)



def true_by_predicate(predicate, display_string):
    return TrueByPredicate(predicate=predicate, display_string=display_string)


def an_existing_path():
    return true_by_predicate(predicate=lambda path: path.exists(), display_string="an_existing_path")


class FalseByPredicate(Matcher):
    def __init__(self, *params):
        super().__init__("false_by_predicate", self.violates_predicate_comparator, *params)

    def violates_predicate_comparator(self, a, predicate):
        return not predicate(a)


def false_by_predicate(predicate):
    return FalseByPredicate(predicate)


class DictionaryMatcher(Matcher):
    def __init__(self, *params):
        super().__init__("dictionary_equal_to", self.equal_to_comparator, *params)

    def equal_to_comparator(self, a, b):
        return a.__dict__ == b.__dict__


def exactly_equal_to_array(array):
    return ExactlyEqualToArrayMatcher(array)


def close_to_array(array):
    return CloseToArrayMatcher(array)


def matching_dictionary_of(object):
    return DictionaryMatcher(object)


def equal_by(expected_value, comparator):
    class EqualByMatcher(Matcher):
        def __init__(self, *params):
            super().__init__("equal_by", comparator, *params)

    return EqualByMatcher(expected_value)


class SharedContext:
    def update(self, context):
        if hasattr(context, '_shared'):
            context._shared.__dict__.update(self.__dict__)
        else:
            context._shared = self
        context.__dict__.update(context._shared.__dict__)


def main_only(fun):
    if "__name__" in fun.__globals__ and fun.__globals__["__name__"] == "__main__":
        return fun

    def null_fun(*args, **kwargs):
        return null_fun

    xit("The it below will only run in main")(null_fun)
    return null_fun
