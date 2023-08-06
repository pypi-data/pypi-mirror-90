# MIT LICENSE
#
# Copyright 1997 - 2020 by IXIA Keysight
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE. 
from uhd_restpy.base import Base
from uhd_restpy.files import Files


class Ospfv3PseudoRouter(Base):
    """Simulated Router Information
    The Ospfv3PseudoRouter class encapsulates a list of ospfv3PseudoRouter resources that are managed by the system.
    A list of resources can be retrieved from the server using the Ospfv3PseudoRouter.find() method.
    """

    __slots__ = ()
    _SDM_NAME = 'ospfv3PseudoRouter'
    _SDM_ATT_MAP = {
        'Active': 'active',
        'BBit': 'bBit',
        'Count': 'count',
        'DescriptiveName': 'descriptiveName',
        'EBit': 'eBit',
        'Name': 'name',
    }

    def __init__(self, parent):
        super(Ospfv3PseudoRouter, self).__init__(parent)

    @property
    def ExternalRoutes(self):
        """
        Returns
        -------
        - obj(uhd_restpy.testplatform.sessions.ixnetwork.topology.externalroutes_338df8b465168f0a019fa20cfb79a952.ExternalRoutes): An instance of the ExternalRoutes class

        Raises
        ------
        - ServerError: The server has encountered an uncategorized error condition
        """
        from uhd_restpy.testplatform.sessions.ixnetwork.topology.externalroutes_338df8b465168f0a019fa20cfb79a952 import ExternalRoutes
        return ExternalRoutes(self)

    @property
    def InterAreaPrefix(self):
        """
        Returns
        -------
        - obj(uhd_restpy.testplatform.sessions.ixnetwork.topology.interareaprefix_f7d367b5d9c390d2708ab13bd5753060.InterAreaPrefix): An instance of the InterAreaPrefix class

        Raises
        ------
        - ServerError: The server has encountered an uncategorized error condition
        """
        from uhd_restpy.testplatform.sessions.ixnetwork.topology.interareaprefix_f7d367b5d9c390d2708ab13bd5753060 import InterAreaPrefix
        return InterAreaPrefix(self)

    @property
    def InterAreaRouter(self):
        """
        Returns
        -------
        - obj(uhd_restpy.testplatform.sessions.ixnetwork.topology.interarearouter_e3708b9636f21a071f8de5213e1653fb.InterAreaRouter): An instance of the InterAreaRouter class

        Raises
        ------
        - ServerError: The server has encountered an uncategorized error condition
        """
        from uhd_restpy.testplatform.sessions.ixnetwork.topology.interarearouter_e3708b9636f21a071f8de5213e1653fb import InterAreaRouter
        return InterAreaRouter(self)

    @property
    def IntraAreaPrefix(self):
        """
        Returns
        -------
        - obj(uhd_restpy.testplatform.sessions.ixnetwork.topology.intraareaprefix_56180291988230b4b517c7fb315aca70.IntraAreaPrefix): An instance of the IntraAreaPrefix class

        Raises
        ------
        - ServerError: The server has encountered an uncategorized error condition
        """
        from uhd_restpy.testplatform.sessions.ixnetwork.topology.intraareaprefix_56180291988230b4b517c7fb315aca70 import IntraAreaPrefix
        return IntraAreaPrefix(self)

    @property
    def LinkLsaRoutes(self):
        """
        Returns
        -------
        - obj(uhd_restpy.testplatform.sessions.ixnetwork.topology.linklsaroutes_90d38ef22c8cb83b2fd6699330dbb5c0.LinkLsaRoutes): An instance of the LinkLsaRoutes class

        Raises
        ------
        - ServerError: The server has encountered an uncategorized error condition
        """
        from uhd_restpy.testplatform.sessions.ixnetwork.topology.linklsaroutes_90d38ef22c8cb83b2fd6699330dbb5c0 import LinkLsaRoutes
        return LinkLsaRoutes(self)

    @property
    def NssaRoutes(self):
        """
        Returns
        -------
        - obj(uhd_restpy.testplatform.sessions.ixnetwork.topology.nssaroutes_90df7db8cb9457fac64f529f67deaa31.NssaRoutes): An instance of the NssaRoutes class

        Raises
        ------
        - ServerError: The server has encountered an uncategorized error condition
        """
        from uhd_restpy.testplatform.sessions.ixnetwork.topology.nssaroutes_90df7db8cb9457fac64f529f67deaa31 import NssaRoutes
        return NssaRoutes(self)

    @property
    def Active(self):
        """
        Returns
        -------
        - obj(uhd_restpy.multivalue.Multivalue): Activate/Deactivate Configuration
        """
        from uhd_restpy.multivalue import Multivalue
        return Multivalue(self, self._get_attribute(self._SDM_ATT_MAP['Active']))

    @property
    def BBit(self):
        """
        Returns
        -------
        - obj(uhd_restpy.multivalue.Multivalue): Router-LSA B-Bit
        """
        from uhd_restpy.multivalue import Multivalue
        return Multivalue(self, self._get_attribute(self._SDM_ATT_MAP['BBit']))

    @property
    def Count(self):
        """
        Returns
        -------
        - number: Number of elements inside associated multiplier-scaled container object, e.g. number of devices inside a Device Group.
        """
        return self._get_attribute(self._SDM_ATT_MAP['Count'])

    @property
    def DescriptiveName(self):
        """
        Returns
        -------
        - str: Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but may offers more context
        """
        return self._get_attribute(self._SDM_ATT_MAP['DescriptiveName'])

    @property
    def EBit(self):
        """
        Returns
        -------
        - obj(uhd_restpy.multivalue.Multivalue): Router-LSA E-Bit
        """
        from uhd_restpy.multivalue import Multivalue
        return Multivalue(self, self._get_attribute(self._SDM_ATT_MAP['EBit']))

    @property
    def Name(self):
        """
        Returns
        -------
        - str: Name of NGPF element, guaranteed to be unique in Scenario
        """
        return self._get_attribute(self._SDM_ATT_MAP['Name'])
    @Name.setter
    def Name(self, value):
        self._set_attribute(self._SDM_ATT_MAP['Name'], value)

    def update(self, Name=None):
        """Updates ospfv3PseudoRouter resource on the server.

        This method has some named parameters with a type: obj (Multivalue).
        The Multivalue class has documentation that details the possible values for those named parameters.

        Args
        ----
        - Name (str): Name of NGPF element, guaranteed to be unique in Scenario

        Raises
        ------
        - ServerError: The server has encountered an uncategorized error condition
        """
        return self._update(self._map_locals(self._SDM_ATT_MAP, locals()))

    def find(self, Count=None, DescriptiveName=None, Name=None):
        """Finds and retrieves ospfv3PseudoRouter resources from the server.

        All named parameters are evaluated on the server using regex. The named parameters can be used to selectively retrieve ospfv3PseudoRouter resources from the server.
        To retrieve an exact match ensure the parameter value starts with ^ and ends with $
        By default the find method takes no parameters and will retrieve all ospfv3PseudoRouter resources from the server.

        Args
        ----
        - Count (number): Number of elements inside associated multiplier-scaled container object, e.g. number of devices inside a Device Group.
        - DescriptiveName (str): Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but may offers more context
        - Name (str): Name of NGPF element, guaranteed to be unique in Scenario

        Returns
        -------
        - self: This instance with matching ospfv3PseudoRouter resources retrieved from the server available through an iterator or index

        Raises
        ------
        - ServerError: The server has encountered an uncategorized error condition
        """
        return self._select(self._map_locals(self._SDM_ATT_MAP, locals()))

    def read(self, href):
        """Retrieves a single instance of ospfv3PseudoRouter data from the server.

        Args
        ----
        - href (str): An href to the instance to be retrieved

        Returns
        -------
        - self: This instance with the ospfv3PseudoRouter resources from the server available through an iterator or index

        Raises
        ------
        - NotFoundError: The requested resource does not exist on the server
        - ServerError: The server has encountered an uncategorized error condition
        """
        return self._read(href)

    def get_device_ids(self, PortNames=None, Active=None, BBit=None, EBit=None):
        """Base class infrastructure that gets a list of ospfv3PseudoRouter device ids encapsulated by this object.

        Use the optional regex parameters in the method to refine the list of device ids encapsulated by this object.

        Args
        ----
        - PortNames (str): optional regex of port names
        - Active (str): optional regex of active
        - BBit (str): optional regex of bBit
        - EBit (str): optional regex of eBit

        Returns
        -------
        - list(int): A list of device ids that meets the regex criteria provided in the method parameters

        Raises
        ------
        - ServerError: The server has encountered an uncategorized error condition
        """
        return self._get_ngpf_device_ids(locals())

    def Start(self):
        """Executes the start operation on the server.

        Start CPF control plane (equals to promote to negotiated state).

        Raises
        ------
        - NotFoundError: The requested resource does not exist on the server
        - ServerError: The server has encountered an uncategorized error condition
        """
        payload = { "Arg1": self }
        return self._execute('start', payload=payload, response_object=None)

    def StartSimulatedRouter(self, *args, **kwargs):
        """Executes the startSimulatedRouter operation on the server.

        Start Pseudo Router

        The IxNetwork model allows for multiple method Signatures with the same name while python does not.

        startSimulatedRouter(SessionIndices=list)
        -----------------------------------------
        - SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

        startSimulatedRouter(SessionIndices=string)
        -------------------------------------------
        - SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

        startSimulatedRouter(Arg2=list)list
        -----------------------------------
        - Arg2 (list(number)): List of indices into the network info. An empty list indicates all instances in the node specific data.
        - Returns list(str): ID to associate each async action invocation

        Raises
        ------
        - NotFoundError: The requested resource does not exist on the server
        - ServerError: The server has encountered an uncategorized error condition
        """
        payload = { "Arg1": self }
        for i in range(len(args)): payload['Arg%s' % (i + 2)] = args[i]
        for item in kwargs.items(): payload[item[0]] = item[1]
        return self._execute('startSimulatedRouter', payload=payload, response_object=None)

    def Stop(self):
        """Executes the stop operation on the server.

        Stop CPF control plane (equals to demote to PreValidated-DoDDone state).

        Raises
        ------
        - NotFoundError: The requested resource does not exist on the server
        - ServerError: The server has encountered an uncategorized error condition
        """
        payload = { "Arg1": self }
        return self._execute('stop', payload=payload, response_object=None)

    def StopSimulatedRouter(self, *args, **kwargs):
        """Executes the stopSimulatedRouter operation on the server.

        Stop Pseudo Router

        The IxNetwork model allows for multiple method Signatures with the same name while python does not.

        stopSimulatedRouter(SessionIndices=list)
        ----------------------------------------
        - SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

        stopSimulatedRouter(SessionIndices=string)
        ------------------------------------------
        - SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

        stopSimulatedRouter(Arg2=list)list
        ----------------------------------
        - Arg2 (list(number)): List of indices into the network info. An empty list indicates all instances in the network info.
        - Returns list(str): ID to associate each async action invocation

        Raises
        ------
        - NotFoundError: The requested resource does not exist on the server
        - ServerError: The server has encountered an uncategorized error condition
        """
        payload = { "Arg1": self }
        for i in range(len(args)): payload['Arg%s' % (i + 2)] = args[i]
        for item in kwargs.items(): payload[item[0]] = item[1]
        return self._execute('stopSimulatedRouter', payload=payload, response_object=None)
