# coding: utf-8

"""
    Demisto API

    This is the public REST API to integrate with the demisto server. HTTP request can be sent using any HTTP-client.  For an example dedicated client take a look at: https://github.com/demisto/demisto-py.  Requests must include API-key that can be generated in the Demisto web client under 'Settings' -> 'Integrations' -> 'API keys'   Optimistic Locking and Versioning\\:  When using Demisto REST API, you will need to make sure to work on the latest version of the item (incident, entry, etc.), otherwise, you will get a DB version error (which not allow you to override a newer item). In addition, you can pass 'version\\: -1' to force data override (make sure that other users data might be lost).  Assume that Alice and Bob both read the same data from Demisto server, then they both changed the data, and then both tried to write the new versions back to the server. Whose changes should be saved? Alice’s? Bob’s? To solve this, each data item in Demisto has a numeric incremental version. If Alice saved an item with version 4 and Bob trying to save the same item with version 3, Demisto will rollback Bob request and returns a DB version conflict error. Bob will need to get the latest item and work on it so Alice work will not get lost.  Example request using 'curl'\\:  ``` curl 'https://hostname:443/incidents/search' -H 'content-type: application/json' -H 'accept: application/json' -H 'Authorization: <API Key goes here>' --data-binary '{\"filter\":{\"query\":\"-status:closed -category:job\",\"period\":{\"by\":\"day\",\"fromValue\":7}}}' --compressed ```  # noqa: E501

    OpenAPI spec version: 2.0.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six

from demisto_client.demisto_api.models.report_automation import ReportAutomation  # noqa: F401,E501
from demisto_client.demisto_api.models.report_query import ReportQuery  # noqa: F401,E501


class Section(object):
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
        'automation': 'ReportAutomation',
        'data': 'object',
        'description': 'str',
        'display_type': 'str',
        'empty_notification': 'str',
        'from_date': 'str',
        'layout': 'object',
        'query': 'ReportQuery',
        'title': 'str',
        'title_style': 'dict(str, object)',
        'to_date': 'str',
        'type': 'str'
    }

    attribute_map = {
        'automation': 'automation',
        'data': 'data',
        'description': 'description',
        'display_type': 'displayType',
        'empty_notification': 'emptyNotification',
        'from_date': 'fromDate',
        'layout': 'layout',
        'query': 'query',
        'title': 'title',
        'title_style': 'titleStyle',
        'to_date': 'toDate',
        'type': 'type'
    }

    def __init__(self, automation=None, data=None, description=None, display_type=None, empty_notification=None, from_date=None, layout=None, query=None, title=None, title_style=None, to_date=None, type=None):  # noqa: E501
        """Section - a model defined in Swagger"""  # noqa: E501

        self._automation = None
        self._data = None
        self._description = None
        self._display_type = None
        self._empty_notification = None
        self._from_date = None
        self._layout = None
        self._query = None
        self._title = None
        self._title_style = None
        self._to_date = None
        self._type = None
        self.discriminator = None

        if automation is not None:
            self.automation = automation
        if data is not None:
            self.data = data
        if description is not None:
            self.description = description
        if display_type is not None:
            self.display_type = display_type
        if empty_notification is not None:
            self.empty_notification = empty_notification
        if from_date is not None:
            self.from_date = from_date
        if layout is not None:
            self.layout = layout
        if query is not None:
            self.query = query
        if title is not None:
            self.title = title
        if title_style is not None:
            self.title_style = title_style
        if to_date is not None:
            self.to_date = to_date
        if type is not None:
            self.type = type

    @property
    def automation(self):
        """Gets the automation of this Section.  # noqa: E501


        :return: The automation of this Section.  # noqa: E501
        :rtype: ReportAutomation
        """
        return self._automation

    @automation.setter
    def automation(self, automation):
        """Sets the automation of this Section.


        :param automation: The automation of this Section.  # noqa: E501
        :type: ReportAutomation
        """

        self._automation = automation

    @property
    def data(self):
        """Gets the data of this Section.  # noqa: E501


        :return: The data of this Section.  # noqa: E501
        :rtype: object
        """
        return self._data

    @data.setter
    def data(self, data):
        """Sets the data of this Section.


        :param data: The data of this Section.  # noqa: E501
        :type: object
        """

        self._data = data

    @property
    def description(self):
        """Gets the description of this Section.  # noqa: E501


        :return: The description of this Section.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this Section.


        :param description: The description of this Section.  # noqa: E501
        :type: str
        """

        self._description = description

    @property
    def display_type(self):
        """Gets the display_type of this Section.  # noqa: E501


        :return: The display_type of this Section.  # noqa: E501
        :rtype: str
        """
        return self._display_type

    @display_type.setter
    def display_type(self, display_type):
        """Sets the display_type of this Section.


        :param display_type: The display_type of this Section.  # noqa: E501
        :type: str
        """

        self._display_type = display_type

    @property
    def empty_notification(self):
        """Gets the empty_notification of this Section.  # noqa: E501


        :return: The empty_notification of this Section.  # noqa: E501
        :rtype: str
        """
        return self._empty_notification

    @empty_notification.setter
    def empty_notification(self, empty_notification):
        """Sets the empty_notification of this Section.


        :param empty_notification: The empty_notification of this Section.  # noqa: E501
        :type: str
        """

        self._empty_notification = empty_notification

    @property
    def from_date(self):
        """Gets the from_date of this Section.  # noqa: E501


        :return: The from_date of this Section.  # noqa: E501
        :rtype: str
        """
        return self._from_date

    @from_date.setter
    def from_date(self, from_date):
        """Sets the from_date of this Section.


        :param from_date: The from_date of this Section.  # noqa: E501
        :type: str
        """

        self._from_date = from_date

    @property
    def layout(self):
        """Gets the layout of this Section.  # noqa: E501


        :return: The layout of this Section.  # noqa: E501
        :rtype: object
        """
        return self._layout

    @layout.setter
    def layout(self, layout):
        """Sets the layout of this Section.


        :param layout: The layout of this Section.  # noqa: E501
        :type: object
        """

        self._layout = layout

    @property
    def query(self):
        """Gets the query of this Section.  # noqa: E501


        :return: The query of this Section.  # noqa: E501
        :rtype: ReportQuery
        """
        return self._query

    @query.setter
    def query(self, query):
        """Sets the query of this Section.


        :param query: The query of this Section.  # noqa: E501
        :type: ReportQuery
        """

        self._query = query

    @property
    def title(self):
        """Gets the title of this Section.  # noqa: E501


        :return: The title of this Section.  # noqa: E501
        :rtype: str
        """
        return self._title

    @title.setter
    def title(self, title):
        """Sets the title of this Section.


        :param title: The title of this Section.  # noqa: E501
        :type: str
        """

        self._title = title

    @property
    def title_style(self):
        """Gets the title_style of this Section.  # noqa: E501


        :return: The title_style of this Section.  # noqa: E501
        :rtype: dict(str, object)
        """
        return self._title_style

    @title_style.setter
    def title_style(self, title_style):
        """Sets the title_style of this Section.


        :param title_style: The title_style of this Section.  # noqa: E501
        :type: dict(str, object)
        """

        self._title_style = title_style

    @property
    def to_date(self):
        """Gets the to_date of this Section.  # noqa: E501


        :return: The to_date of this Section.  # noqa: E501
        :rtype: str
        """
        return self._to_date

    @to_date.setter
    def to_date(self, to_date):
        """Sets the to_date of this Section.


        :param to_date: The to_date of this Section.  # noqa: E501
        :type: str
        """

        self._to_date = to_date

    @property
    def type(self):
        """Gets the type of this Section.  # noqa: E501


        :return: The type of this Section.  # noqa: E501
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this Section.


        :param type: The type of this Section.  # noqa: E501
        :type: str
        """

        self._type = type

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
        if issubclass(Section, dict):
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
        if not isinstance(other, Section):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
