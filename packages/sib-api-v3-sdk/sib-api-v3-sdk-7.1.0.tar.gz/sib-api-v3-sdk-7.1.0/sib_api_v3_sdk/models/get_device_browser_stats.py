# coding: utf-8

"""
    SendinBlue API

    SendinBlue provide a RESTFul API that can be used with any languages. With this API, you will be able to :   - Manage your campaigns and get the statistics   - Manage your contacts   - Send transactional Emails and SMS   - and much more...  You can download our wrappers at https://github.com/orgs/sendinblue  **Possible responses**   | Code | Message |   | :-------------: | ------------- |   | 200  | OK. Successful Request  |   | 201  | OK. Successful Creation |   | 202  | OK. Request accepted |   | 204  | OK. Successful Update/Deletion  |   | 400  | Error. Bad Request  |   | 401  | Error. Authentication Needed  |   | 402  | Error. Not enough credit, plan upgrade needed  |   | 403  | Error. Permission denied  |   | 404  | Error. Object does not exist |   | 405  | Error. Method not allowed  |   | 406  | Error. Not Acceptable  |   # noqa: E501

    OpenAPI spec version: 3.0.0
    Contact: contact@sendinblue.com
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six


class GetDeviceBrowserStats(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'clickers': 'int',
        'unique_clicks': 'int',
        'viewed': 'int',
        'unique_views': 'int'
    }

    attribute_map = {
        'clickers': 'clickers',
        'unique_clicks': 'uniqueClicks',
        'viewed': 'viewed',
        'unique_views': 'uniqueViews'
    }

    def __init__(self, clickers=None, unique_clicks=None, viewed=None, unique_views=None):  # noqa: E501
        """GetDeviceBrowserStats - a model defined in Swagger"""  # noqa: E501

        self._clickers = None
        self._unique_clicks = None
        self._viewed = None
        self._unique_views = None
        self.discriminator = None

        self.clickers = clickers
        self.unique_clicks = unique_clicks
        self.viewed = viewed
        self.unique_views = unique_views

    @property
    def clickers(self):
        """Gets the clickers of this GetDeviceBrowserStats.  # noqa: E501

        Number of total clicks for the campaign using the particular browser  # noqa: E501

        :return: The clickers of this GetDeviceBrowserStats.  # noqa: E501
        :rtype: int
        """
        return self._clickers

    @clickers.setter
    def clickers(self, clickers):
        """Sets the clickers of this GetDeviceBrowserStats.

        Number of total clicks for the campaign using the particular browser  # noqa: E501

        :param clickers: The clickers of this GetDeviceBrowserStats.  # noqa: E501
        :type: int
        """
        if clickers is None:
            raise ValueError("Invalid value for `clickers`, must not be `None`")  # noqa: E501

        self._clickers = clickers

    @property
    def unique_clicks(self):
        """Gets the unique_clicks of this GetDeviceBrowserStats.  # noqa: E501

        Number of unique clicks for the campaign using the particular browser  # noqa: E501

        :return: The unique_clicks of this GetDeviceBrowserStats.  # noqa: E501
        :rtype: int
        """
        return self._unique_clicks

    @unique_clicks.setter
    def unique_clicks(self, unique_clicks):
        """Sets the unique_clicks of this GetDeviceBrowserStats.

        Number of unique clicks for the campaign using the particular browser  # noqa: E501

        :param unique_clicks: The unique_clicks of this GetDeviceBrowserStats.  # noqa: E501
        :type: int
        """
        if unique_clicks is None:
            raise ValueError("Invalid value for `unique_clicks`, must not be `None`")  # noqa: E501

        self._unique_clicks = unique_clicks

    @property
    def viewed(self):
        """Gets the viewed of this GetDeviceBrowserStats.  # noqa: E501

        Number of openings for the campaign using the particular browser  # noqa: E501

        :return: The viewed of this GetDeviceBrowserStats.  # noqa: E501
        :rtype: int
        """
        return self._viewed

    @viewed.setter
    def viewed(self, viewed):
        """Sets the viewed of this GetDeviceBrowserStats.

        Number of openings for the campaign using the particular browser  # noqa: E501

        :param viewed: The viewed of this GetDeviceBrowserStats.  # noqa: E501
        :type: int
        """
        if viewed is None:
            raise ValueError("Invalid value for `viewed`, must not be `None`")  # noqa: E501

        self._viewed = viewed

    @property
    def unique_views(self):
        """Gets the unique_views of this GetDeviceBrowserStats.  # noqa: E501

        Number of unique openings for the campaign using the particular browser  # noqa: E501

        :return: The unique_views of this GetDeviceBrowserStats.  # noqa: E501
        :rtype: int
        """
        return self._unique_views

    @unique_views.setter
    def unique_views(self, unique_views):
        """Sets the unique_views of this GetDeviceBrowserStats.

        Number of unique openings for the campaign using the particular browser  # noqa: E501

        :param unique_views: The unique_views of this GetDeviceBrowserStats.  # noqa: E501
        :type: int
        """
        if unique_views is None:
            raise ValueError("Invalid value for `unique_views`, must not be `None`")  # noqa: E501

        self._unique_views = unique_views

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value
        if issubclass(GetDeviceBrowserStats, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, GetDeviceBrowserStats):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
