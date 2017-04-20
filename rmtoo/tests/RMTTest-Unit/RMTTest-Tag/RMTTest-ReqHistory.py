'''
 rmtoo
   Free and Open Source Requirements Management Tool

  Unit test for ReqHistory

 (c) 2010-2012,2017 by flonatel GmbH & Co. KG

 For licensing details see COPYING
'''
import unittest

from rmtoo.inputs.ReqHistory import ReqHistory
from rmtoo.tests.lib.ReqTag import create_parameters


class RMTTest_ReqHistory(unittest.TestCase):

    def rmttest_positive_01(self):
        "Requirement Tag History - no tag given"
        config, req = create_parameters()

        rt = ReqHistory(config)
        name, value = rt.rewrite("History-test", req)
        self.assertEqual("History", name)
        self.assertIsNone(value)

    def rmttest_positive_02(self):
        "Requirement Tag History - History set"
        config, req = create_parameters()
        req = {"History": "something"}

        rt = ReqHistory(config)
        name, value = rt.rewrite("History-test", req)
        self.assertEqual("History", name)
        self.assertEqual("something", value)
