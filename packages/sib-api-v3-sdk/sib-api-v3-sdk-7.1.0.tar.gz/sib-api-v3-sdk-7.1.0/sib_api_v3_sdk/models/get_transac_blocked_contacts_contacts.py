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


class GetTransacBlockedContactsContacts(object):
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
        'email': 'str',
        'sender_email': 'str',
        'reason': 'GetTransacBlockedContactsReason',
        'blocked_at': 'datetime'
    }

    attribute_map = {
        'email': 'email',
        'sender_email': 'senderEmail',
        'reason': 'reason',
        'blocked_at': 'blockedAt'
    }

    def __init__(self, email=None, sender_email=None, reason=None, blocked_at=None):  # noqa: E501
        """GetTransacBlockedContactsContacts - a model defined in Swagger"""  # noqa: E501

        self._email = None
        self._sender_email = None
        self._reason = None
        self._blocked_at = None
        self.discriminator = None

        self.email = email
        self.sender_email = sender_email
        self.reason = reason
        self.blocked_at = blocked_at

    @property
    def email(self):
        """Gets the email of this GetTransacBlockedContactsContacts.  # noqa: E501

        Email address of the blocked or unsubscribed contact  # noqa: E501

        :return: The email of this GetTransacBlockedContactsContacts.  # noqa: E501
        :rtype: str
        """
        return self._email

    @email.setter
    def email(self, email):
        """Sets the email of this GetTransacBlockedContactsContacts.

        Email address of the blocked or unsubscribed contact  # noqa: E501

        :param email: The email of this GetTransacBlockedContactsContacts.  # noqa: E501
        :type: str
        """
        if email is None:
            raise ValueError("Invalid value for `email`, must not be `None`")  # noqa: E501

        self._email = email

    @property
    def sender_email(self):
        """Gets the sender_email of this GetTransacBlockedContactsContacts.  # noqa: E501

        Sender email address of the blocked or unsubscribed contact  # noqa: E501

        :return: The sender_email of this GetTransacBlockedContactsContacts.  # noqa: E501
        :rtype: str
        """
        return self._sender_email

    @sender_email.setter
    def sender_email(self, sender_email):
        """Sets the sender_email of this GetTransacBlockedContactsContacts.

        Sender email address of the blocked or unsubscribed contact  # noqa: E501

        :param sender_email: The sender_email of this GetTransacBlockedContactsContacts.  # noqa: E501
        :type: str
        """
        if sender_email is None:
            raise ValueError("Invalid value for `sender_email`, must not be `None`")  # noqa: E501

        self._sender_email = sender_email

    @property
    def reason(self):
        """Gets the reason of this GetTransacBlockedContactsContacts.  # noqa: E501


        :return: The reason of this GetTransacBlockedContactsContacts.  # noqa: E501
        :rtype: GetTransacBlockedContactsReason
        """
        return self._reason

    @reason.setter
    def reason(self, reason):
        """Sets the reason of this GetTransacBlockedContactsContacts.


        :param reason: The reason of this GetTransacBlockedContactsContacts.  # noqa: E501
        :type: GetTransacBlockedContactsReason
        """
        if reason is None:
            raise ValueError("Invalid value for `reason`, must not be `None`")  # noqa: E501

        self._reason = reason

    @property
    def blocked_at(self):
        """Gets the blocked_at of this GetTransacBlockedContactsContacts.  # noqa: E501

        Date when the contact was blocked or unsubscribed on  # noqa: E501

        :return: The blocked_at of this GetTransacBlockedContactsContacts.  # noqa: E501
        :rtype: datetime
        """
        return self._blocked_at

    @blocked_at.setter
    def blocked_at(self, blocked_at):
        """Sets the blocked_at of this GetTransacBlockedContactsContacts.

        Date when the contact was blocked or unsubscribed on  # noqa: E501

        :param blocked_at: The blocked_at of this GetTransacBlockedContactsContacts.  # noqa: E501
        :type: datetime
        """
        if blocked_at is None:
            raise ValueError("Invalid value for `blocked_at`, must not be `None`")  # noqa: E501

        self._blocked_at = blocked_at

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
        if issubclass(GetTransacBlockedContactsContacts, dict):
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
        if not isinstance(other, GetTransacBlockedContactsContacts):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
