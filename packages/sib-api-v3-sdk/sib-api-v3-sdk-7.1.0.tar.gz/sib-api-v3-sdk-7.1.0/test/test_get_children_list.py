# coding: utf-8

"""
    SendinBlue API

    SendinBlue provide a RESTFul API that can be used with any languages. With this API, you will be able to :   - Manage your campaigns and get the statistics   - Manage your contacts   - Send transactional Emails and SMS   - and much more...  You can download our wrappers at https://github.com/orgs/sendinblue  **Possible responses**   | Code | Message |   | :-------------: | ------------- |   | 200  | OK. Successful Request  |   | 201  | OK. Successful Creation |   | 202  | OK. Request accepted |   | 204  | OK. Successful Update/Deletion  |   | 400  | Error. Bad Request  |   | 401  | Error. Authentication Needed  |   | 402  | Error. Not enough credit, plan upgrade needed  |   | 403  | Error. Permission denied  |   | 404  | Error. Object does not exist |   | 405  | Error. Method not allowed  |   | 406  | Error. Not Acceptable  |   # noqa: E501

    OpenAPI spec version: 3.0.0
    Contact: contact@sendinblue.com
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from __future__ import absolute_import

import unittest

import sib_api_v3_sdk
from sib_api_v3_sdk.models.get_children_list import GetChildrenList  # noqa: E501
from sib_api_v3_sdk.rest import ApiException


class TestGetChildrenList(unittest.TestCase):
    """GetChildrenList unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testGetChildrenList(self):
        """Test GetChildrenList"""
        # FIXME: construct object with mandatory attributes with example values
        # model = sib_api_v3_sdk.models.get_children_list.GetChildrenList()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
