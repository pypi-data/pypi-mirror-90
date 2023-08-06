"""




"""
import os
import json

from .context import Context
from .qatest import QATest
from . import html_tree_export


class _SessionRootTest(QATest):

    SESSION = None

    @classmethod
    def get_sub_test_types(cls):
        return cls.SESSION._test_types

    def can_fix(self, context):
        return False, "Can't fix the whole world :/"


class Session(object):
    def __init__(self):
        super(Session, self).__init__()

        # This is sooooooooooo hacky !!! ^o^
        # I'll burn in hell for this :p
        class Root(_SessionRootTest):
            SESSION = self

        self._root_test_type = Root

        self._stop_on_fail = None
        self._allow_auto_fix = None
        self._context = Context(None)

        self._runs = []

    def register_test_types(self, test_types):
        self._test_types = list(test_types)

    def context_set(self, **values):
        self._context.update(**values)

    def run(self):
        root_test = self._root_test_type()
        self._runs.append(root_test)

        # use a copy of the context, tests will modify it:
        context = Context(self._context)

        # configure the context as requested:
        if self._stop_on_fail is not None:
            root_test.set_stop_on_fail(context, self._stop_on_fail)
        if self._allow_auto_fix is not None:
            root_test.set_allow_auto_fix(context, self._allow_auto_fix)

        # run all the tests:
        result = root_test.run(context)
        return result

    def to_lines(self):
        lines = []
        for run in self._runs:
            lines.extend(run.to_lines())
        return lines

    def to_dict_list(self):
        ret = []
        for run in self._runs:
            ret.append(run.to_dict())
        return ret

    def to_json(self):
        as_dict_list = self.to_dict_list()
        return json.dumps(as_dict_list)

    def to_json_file(self, filename, force_overwrite=False):
        as_list = self.to_dict_list()
        if os.path.exists(filename) and not force_overwrite:
            raise ValueError(f"filename {filename} already exists !")
        with open(filename, "w") as fp:
            json.dump(as_list, fp)

    def to_html_tree(self, filename, force_overwrite=False):
        session_json = self.to_json()
        content = html_tree_export.html_tree(session_json)
        if os.path.exists(filename) and not force_overwrite:
            raise ValueError(f"filename {filename} already exists !")
        with open(filename, "w") as fp:
            fp.write(content)
