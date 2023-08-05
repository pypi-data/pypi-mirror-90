# coding: utf-8

"""
    Aliro Quantum App

    This is an api for the Aliro Quantum App  # noqa: E501

    The version of the OpenAPI document: 1.0.0
    Contact: nick@aliroquantum.com
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from aliro_quantum.configuration import Configuration


class ControlFlowGraphCircuit(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {
        'circuit': 'str',
        'language': 'str'
    }

    attribute_map = {
        'circuit': 'circuit',
        'language': 'language'
    }

    def __init__(self, circuit=None, language=None, local_vars_configuration=None):  # noqa: E501
        """ControlFlowGraphCircuit - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._circuit = None
        self._language = None
        self.discriminator = None

        if circuit is not None:
            self.circuit = circuit
        if language is not None:
            self.language = language

    @property
    def circuit(self):
        """Gets the circuit of this ControlFlowGraphCircuit.  # noqa: E501


        :return: The circuit of this ControlFlowGraphCircuit.  # noqa: E501
        :rtype: str
        """
        return self._circuit

    @circuit.setter
    def circuit(self, circuit):
        """Sets the circuit of this ControlFlowGraphCircuit.


        :param circuit: The circuit of this ControlFlowGraphCircuit.  # noqa: E501
        :type: str
        """

        self._circuit = circuit

    @property
    def language(self):
        """Gets the language of this ControlFlowGraphCircuit.  # noqa: E501


        :return: The language of this ControlFlowGraphCircuit.  # noqa: E501
        :rtype: str
        """
        return self._language

    @language.setter
    def language(self, language):
        """Sets the language of this ControlFlowGraphCircuit.


        :param language: The language of this ControlFlowGraphCircuit.  # noqa: E501
        :type: str
        """

        self._language = language

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
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

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, ControlFlowGraphCircuit):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ControlFlowGraphCircuit):
            return True

        return self.to_dict() != other.to_dict()
