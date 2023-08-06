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


class CfmBridge(Base):
    """
    The CfmBridge class encapsulates a list of cfmBridge resources that are managed by the user.
    A list of resources can be retrieved from the server using the CfmBridge.find() method.
    The list can be managed by using the CfmBridge.add() and CfmBridge.remove() methods.
    """

    __slots__ = ()
    _SDM_NAME = 'cfmBridge'
    _SDM_ATT_MAP = {
        'Active': 'active',
        'AllowCfmMaidFormatsinY1731': 'allowCfmMaidFormatsinY1731',
        'ConnectedVia': 'connectedVia',
        'Count': 'count',
        'DescriptiveName': 'descriptiveName',
        'EnableOutOfSequenceCcmDetection': 'enableOutOfSequenceCcmDetection',
        'EncapsulationType': 'encapsulationType',
        'Errors': 'errors',
        'EtherType': 'etherType',
        'GarbageCollectionTime': 'garbageCollectionTime',
        'Multiplier': 'multiplier',
        'Name': 'name',
        'NumberOfCustomTLVs': 'numberOfCustomTLVs',
        'NumberOfLinks': 'numberOfLinks',
        'NumberOfMPs': 'numberOfMPs',
        'NumberOfMdLevels': 'numberOfMdLevels',
        'OperationMode': 'operationMode',
        'SessionStatus': 'sessionStatus',
        'StackedLayers': 'stackedLayers',
        'StateCounts': 'stateCounts',
        'Status': 'status',
    }

    def __init__(self, parent):
        super(CfmBridge, self).__init__(parent)

    @property
    def AdvancedLearnedInfoOptions(self):
        """
        Returns
        -------
        - obj(uhd_restpy.testplatform.sessions.ixnetwork.topology.advancedlearnedinfooptions_91489fb21a51a28f7c4d1aa208a1d6a4.AdvancedLearnedInfoOptions): An instance of the AdvancedLearnedInfoOptions class

        Raises
        ------
        - ServerError: The server has encountered an uncategorized error condition
        """
        from uhd_restpy.testplatform.sessions.ixnetwork.topology.advancedlearnedinfooptions_91489fb21a51a28f7c4d1aa208a1d6a4 import AdvancedLearnedInfoOptions
        return AdvancedLearnedInfoOptions(self)._select()

    @property
    def CustomTLV(self):
        """
        Returns
        -------
        - obj(uhd_restpy.testplatform.sessions.ixnetwork.topology.customtlv_8529f592411fc68872b828287df0f7b7.CustomTLV): An instance of the CustomTLV class

        Raises
        ------
        - ServerError: The server has encountered an uncategorized error condition
        """
        from uhd_restpy.testplatform.sessions.ixnetwork.topology.customtlv_8529f592411fc68872b828287df0f7b7 import CustomTLV
        return CustomTLV(self)._select()

    @property
    def LearnedInfo(self):
        """
        Returns
        -------
        - obj(uhd_restpy.testplatform.sessions.ixnetwork.topology.learnedinfo.learnedinfo_ff4d5e5643a63bccb40b6cf64fc58100.LearnedInfo): An instance of the LearnedInfo class

        Raises
        ------
        - ServerError: The server has encountered an uncategorized error condition
        """
        from uhd_restpy.testplatform.sessions.ixnetwork.topology.learnedinfo.learnedinfo_ff4d5e5643a63bccb40b6cf64fc58100 import LearnedInfo
        return LearnedInfo(self)

    @property
    def Link(self):
        """
        Returns
        -------
        - obj(uhd_restpy.testplatform.sessions.ixnetwork.topology.link_3c4eb8730b5826d36118e54600a5188b.Link): An instance of the Link class

        Raises
        ------
        - ServerError: The server has encountered an uncategorized error condition
        """
        from uhd_restpy.testplatform.sessions.ixnetwork.topology.link_3c4eb8730b5826d36118e54600a5188b import Link
        return Link(self)._select()

    @property
    def MdLevels(self):
        """
        Returns
        -------
        - obj(uhd_restpy.testplatform.sessions.ixnetwork.topology.mdlevels_139c757bfb085e85b81902e33a549b1f.MdLevels): An instance of the MdLevels class

        Raises
        ------
        - ServerError: The server has encountered an uncategorized error condition
        """
        from uhd_restpy.testplatform.sessions.ixnetwork.topology.mdlevels_139c757bfb085e85b81902e33a549b1f import MdLevels
        return MdLevels(self)._select()

    @property
    def Mp(self):
        """
        Returns
        -------
        - obj(uhd_restpy.testplatform.sessions.ixnetwork.topology.mp_733c1962f075c06b1219c758cc609898.Mp): An instance of the Mp class

        Raises
        ------
        - ServerError: The server has encountered an uncategorized error condition
        """
        from uhd_restpy.testplatform.sessions.ixnetwork.topology.mp_733c1962f075c06b1219c758cc609898 import Mp
        return Mp(self)._select()

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
    def AllowCfmMaidFormatsinY1731(self):
        """
        Returns
        -------
        - obj(uhd_restpy.multivalue.Multivalue): Allow CFM MAID Formats in Y.1731
        """
        from uhd_restpy.multivalue import Multivalue
        return Multivalue(self, self._get_attribute(self._SDM_ATT_MAP['AllowCfmMaidFormatsinY1731']))

    @property
    def ConnectedVia(self):
        """DEPRECATED 
        Returns
        -------
        - list(str[None | /api/v1/sessions/1/ixnetwork/topology/.../*]): List of layers this layer used to connect to the wire
        """
        return self._get_attribute(self._SDM_ATT_MAP['ConnectedVia'])
    @ConnectedVia.setter
    def ConnectedVia(self, value):
        self._set_attribute(self._SDM_ATT_MAP['ConnectedVia'], value)

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
    def EnableOutOfSequenceCcmDetection(self):
        """
        Returns
        -------
        - obj(uhd_restpy.multivalue.Multivalue): Enable Out of Sequence CCM Detection
        """
        from uhd_restpy.multivalue import Multivalue
        return Multivalue(self, self._get_attribute(self._SDM_ATT_MAP['EnableOutOfSequenceCcmDetection']))

    @property
    def EncapsulationType(self):
        """
        Returns
        -------
        - obj(uhd_restpy.multivalue.Multivalue): Encapsulation
        """
        from uhd_restpy.multivalue import Multivalue
        return Multivalue(self, self._get_attribute(self._SDM_ATT_MAP['EncapsulationType']))

    @property
    def Errors(self):
        """
        Returns
        -------
        - list(dict(arg1:str[None | /api/v1/sessions/1/ixnetwork//.../*],arg2:list[str])): A list of errors that have occurred
        """
        return self._get_attribute(self._SDM_ATT_MAP['Errors'])

    @property
    def EtherType(self):
        """
        Returns
        -------
        - obj(uhd_restpy.multivalue.Multivalue): Ether Type
        """
        from uhd_restpy.multivalue import Multivalue
        return Multivalue(self, self._get_attribute(self._SDM_ATT_MAP['EtherType']))

    @property
    def GarbageCollectionTime(self):
        """
        Returns
        -------
        - obj(uhd_restpy.multivalue.Multivalue): Garbage Collection Time (sec)
        """
        from uhd_restpy.multivalue import Multivalue
        return Multivalue(self, self._get_attribute(self._SDM_ATT_MAP['GarbageCollectionTime']))

    @property
    def Multiplier(self):
        """
        Returns
        -------
        - number: Number of layer instances per parent instance (multiplier)
        """
        return self._get_attribute(self._SDM_ATT_MAP['Multiplier'])
    @Multiplier.setter
    def Multiplier(self, value):
        self._set_attribute(self._SDM_ATT_MAP['Multiplier'], value)

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

    @property
    def NumberOfCustomTLVs(self):
        """
        Returns
        -------
        - number: Number of Custom TLVs
        """
        return self._get_attribute(self._SDM_ATT_MAP['NumberOfCustomTLVs'])
    @NumberOfCustomTLVs.setter
    def NumberOfCustomTLVs(self, value):
        self._set_attribute(self._SDM_ATT_MAP['NumberOfCustomTLVs'], value)

    @property
    def NumberOfLinks(self):
        """
        Returns
        -------
        - number: Number of Links
        """
        return self._get_attribute(self._SDM_ATT_MAP['NumberOfLinks'])
    @NumberOfLinks.setter
    def NumberOfLinks(self, value):
        self._set_attribute(self._SDM_ATT_MAP['NumberOfLinks'], value)

    @property
    def NumberOfMPs(self):
        """
        Returns
        -------
        - number: Number of MPs
        """
        return self._get_attribute(self._SDM_ATT_MAP['NumberOfMPs'])
    @NumberOfMPs.setter
    def NumberOfMPs(self, value):
        self._set_attribute(self._SDM_ATT_MAP['NumberOfMPs'], value)

    @property
    def NumberOfMdLevels(self):
        """
        Returns
        -------
        - number: Number of MD/MEG Levels
        """
        return self._get_attribute(self._SDM_ATT_MAP['NumberOfMdLevels'])
    @NumberOfMdLevels.setter
    def NumberOfMdLevels(self, value):
        self._set_attribute(self._SDM_ATT_MAP['NumberOfMdLevels'], value)

    @property
    def OperationMode(self):
        """
        Returns
        -------
        - obj(uhd_restpy.multivalue.Multivalue): Operation Mode
        """
        from uhd_restpy.multivalue import Multivalue
        return Multivalue(self, self._get_attribute(self._SDM_ATT_MAP['OperationMode']))

    @property
    def SessionStatus(self):
        """
        Returns
        -------
        - list(str[down | notStarted | up]): Current state of protocol session: Not Started - session negotiation not started, the session is not active yet. Down - actively trying to bring up a protocol session, but negotiation is didn't successfully complete (yet). Up - session came up successfully.
        """
        return self._get_attribute(self._SDM_ATT_MAP['SessionStatus'])

    @property
    def StackedLayers(self):
        """
        Returns
        -------
        - list(str[None | /api/v1/sessions/1/ixnetwork/topology/.../*]): List of secondary (many to one) child layer protocols
        """
        return self._get_attribute(self._SDM_ATT_MAP['StackedLayers'])
    @StackedLayers.setter
    def StackedLayers(self, value):
        self._set_attribute(self._SDM_ATT_MAP['StackedLayers'], value)

    @property
    def StateCounts(self):
        """
        Returns
        -------
        - dict(total:number,notStarted:number,down:number,up:number): A list of values that indicates the total number of sessions, the number of sessions not started, the number of sessions down and the number of sessions that are up
        """
        return self._get_attribute(self._SDM_ATT_MAP['StateCounts'])

    @property
    def Status(self):
        """
        Returns
        -------
        - str(configured | error | mixed | notStarted | started | starting | stopping): Running status of associated network element. Once in Started state, protocol sessions will begin to negotiate.
        """
        return self._get_attribute(self._SDM_ATT_MAP['Status'])

    def update(self, ConnectedVia=None, Multiplier=None, Name=None, NumberOfCustomTLVs=None, NumberOfLinks=None, NumberOfMPs=None, NumberOfMdLevels=None, StackedLayers=None):
        """Updates cfmBridge resource on the server.

        This method has some named parameters with a type: obj (Multivalue).
        The Multivalue class has documentation that details the possible values for those named parameters.

        Args
        ----
        - ConnectedVia (list(str[None | /api/v1/sessions/1/ixnetwork/topology/.../*])): List of layers this layer used to connect to the wire
        - Multiplier (number): Number of layer instances per parent instance (multiplier)
        - Name (str): Name of NGPF element, guaranteed to be unique in Scenario
        - NumberOfCustomTLVs (number): Number of Custom TLVs
        - NumberOfLinks (number): Number of Links
        - NumberOfMPs (number): Number of MPs
        - NumberOfMdLevels (number): Number of MD/MEG Levels
        - StackedLayers (list(str[None | /api/v1/sessions/1/ixnetwork/topology/.../*])): List of secondary (many to one) child layer protocols

        Raises
        ------
        - ServerError: The server has encountered an uncategorized error condition
        """
        return self._update(self._map_locals(self._SDM_ATT_MAP, locals()))

    def add(self, ConnectedVia=None, Multiplier=None, Name=None, NumberOfCustomTLVs=None, NumberOfLinks=None, NumberOfMPs=None, NumberOfMdLevels=None, StackedLayers=None):
        """Adds a new cfmBridge resource on the server and adds it to the container.

        Args
        ----
        - ConnectedVia (list(str[None | /api/v1/sessions/1/ixnetwork/topology/.../*])): List of layers this layer used to connect to the wire
        - Multiplier (number): Number of layer instances per parent instance (multiplier)
        - Name (str): Name of NGPF element, guaranteed to be unique in Scenario
        - NumberOfCustomTLVs (number): Number of Custom TLVs
        - NumberOfLinks (number): Number of Links
        - NumberOfMPs (number): Number of MPs
        - NumberOfMdLevels (number): Number of MD/MEG Levels
        - StackedLayers (list(str[None | /api/v1/sessions/1/ixnetwork/topology/.../*])): List of secondary (many to one) child layer protocols

        Returns
        -------
        - self: This instance with all currently retrieved cfmBridge resources using find and the newly added cfmBridge resources available through an iterator or index

        Raises
        ------
        - ServerError: The server has encountered an uncategorized error condition
        """
        return self._create(self._map_locals(self._SDM_ATT_MAP, locals()))

    def remove(self):
        """Deletes all the contained cfmBridge resources in this instance from the server.

        Raises
        ------
        - NotFoundError: The requested resource does not exist on the server
        - ServerError: The server has encountered an uncategorized error condition
        """
        self._delete()

    def find(self, ConnectedVia=None, Count=None, DescriptiveName=None, Errors=None, Multiplier=None, Name=None, NumberOfCustomTLVs=None, NumberOfLinks=None, NumberOfMPs=None, NumberOfMdLevels=None, SessionStatus=None, StackedLayers=None, StateCounts=None, Status=None):
        """Finds and retrieves cfmBridge resources from the server.

        All named parameters are evaluated on the server using regex. The named parameters can be used to selectively retrieve cfmBridge resources from the server.
        To retrieve an exact match ensure the parameter value starts with ^ and ends with $
        By default the find method takes no parameters and will retrieve all cfmBridge resources from the server.

        Args
        ----
        - ConnectedVia (list(str[None | /api/v1/sessions/1/ixnetwork/topology/.../*])): List of layers this layer used to connect to the wire
        - Count (number): Number of elements inside associated multiplier-scaled container object, e.g. number of devices inside a Device Group.
        - DescriptiveName (str): Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but may offers more context
        - Errors (list(dict(arg1:str[None | /api/v1/sessions/1/ixnetwork//.../*],arg2:list[str]))): A list of errors that have occurred
        - Multiplier (number): Number of layer instances per parent instance (multiplier)
        - Name (str): Name of NGPF element, guaranteed to be unique in Scenario
        - NumberOfCustomTLVs (number): Number of Custom TLVs
        - NumberOfLinks (number): Number of Links
        - NumberOfMPs (number): Number of MPs
        - NumberOfMdLevels (number): Number of MD/MEG Levels
        - SessionStatus (list(str[down | notStarted | up])): Current state of protocol session: Not Started - session negotiation not started, the session is not active yet. Down - actively trying to bring up a protocol session, but negotiation is didn't successfully complete (yet). Up - session came up successfully.
        - StackedLayers (list(str[None | /api/v1/sessions/1/ixnetwork/topology/.../*])): List of secondary (many to one) child layer protocols
        - StateCounts (dict(total:number,notStarted:number,down:number,up:number)): A list of values that indicates the total number of sessions, the number of sessions not started, the number of sessions down and the number of sessions that are up
        - Status (str(configured | error | mixed | notStarted | started | starting | stopping)): Running status of associated network element. Once in Started state, protocol sessions will begin to negotiate.

        Returns
        -------
        - self: This instance with matching cfmBridge resources retrieved from the server available through an iterator or index

        Raises
        ------
        - ServerError: The server has encountered an uncategorized error condition
        """
        return self._select(self._map_locals(self._SDM_ATT_MAP, locals()))

    def read(self, href):
        """Retrieves a single instance of cfmBridge data from the server.

        Args
        ----
        - href (str): An href to the instance to be retrieved

        Returns
        -------
        - self: This instance with the cfmBridge resources from the server available through an iterator or index

        Raises
        ------
        - NotFoundError: The requested resource does not exist on the server
        - ServerError: The server has encountered an uncategorized error condition
        """
        return self._read(href)

    def get_device_ids(self, PortNames=None, Active=None, AllowCfmMaidFormatsinY1731=None, EnableOutOfSequenceCcmDetection=None, EncapsulationType=None, EtherType=None, GarbageCollectionTime=None, OperationMode=None):
        """Base class infrastructure that gets a list of cfmBridge device ids encapsulated by this object.

        Use the optional regex parameters in the method to refine the list of device ids encapsulated by this object.

        Args
        ----
        - PortNames (str): optional regex of port names
        - Active (str): optional regex of active
        - AllowCfmMaidFormatsinY1731 (str): optional regex of allowCfmMaidFormatsinY1731
        - EnableOutOfSequenceCcmDetection (str): optional regex of enableOutOfSequenceCcmDetection
        - EncapsulationType (str): optional regex of encapsulationType
        - EtherType (str): optional regex of etherType
        - GarbageCollectionTime (str): optional regex of garbageCollectionTime
        - OperationMode (str): optional regex of operationMode

        Returns
        -------
        - list(int): A list of device ids that meets the regex criteria provided in the method parameters

        Raises
        ------
        - ServerError: The server has encountered an uncategorized error condition
        """
        return self._get_ngpf_device_ids(locals())

    def ClearAllLearnedInfo(self, *args, **kwargs):
        """Executes the clearAllLearnedInfo operation on the server.

        Clear All Learned Info

        The IxNetwork model allows for multiple method Signatures with the same name while python does not.

        clearAllLearnedInfo(SessionIndices=list)
        ----------------------------------------
        - SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

        clearAllLearnedInfo(SessionIndices=string)
        ------------------------------------------
        - SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

        clearAllLearnedInfo(Arg2=list)list
        ----------------------------------
        - Arg2 (list(number)): List of indices into the protocol plugin.An empty list indicates all instances in the plugin.
        - Returns list(str): ID to associate each async action invocation

        Raises
        ------
        - NotFoundError: The requested resource does not exist on the server
        - ServerError: The server has encountered an uncategorized error condition
        """
        payload = { "Arg1": self }
        for i in range(len(args)): payload['Arg%s' % (i + 2)] = args[i]
        for item in kwargs.items(): payload[item[0]] = item[1]
        return self._execute('clearAllLearnedInfo', payload=payload, response_object=None)

    def GetAllLearnedInfo(self, *args, **kwargs):
        """Executes the getAllLearnedInfo operation on the server.

        Get All Learned Info

        The IxNetwork model allows for multiple method Signatures with the same name while python does not.

        getAllLearnedInfo(SessionIndices=list)
        --------------------------------------
        - SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

        getAllLearnedInfo(SessionIndices=string)
        ----------------------------------------
        - SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

        getAllLearnedInfo(Arg2=list)list
        --------------------------------
        - Arg2 (list(number)): List of indices into the protocol plugin.An empty list indicates all instances in the plugin.
        - Returns list(str): Please provide a proper description here

        Raises
        ------
        - NotFoundError: The requested resource does not exist on the server
        - ServerError: The server has encountered an uncategorized error condition
        """
        payload = { "Arg1": self }
        for i in range(len(args)): payload['Arg%s' % (i + 2)] = args[i]
        for item in kwargs.items(): payload[item[0]] = item[1]
        return self._execute('getAllLearnedInfo', payload=payload, response_object=None)

    def GetCfmAISDbLearnedInformation(self, *args, **kwargs):
        """Executes the getCfmAISDbLearnedInformation operation on the server.

        Get Learned AIS Information

        getCfmAISDbLearnedInformation(Arg2=list)list
        --------------------------------------------
        - Arg2 (list(number)): List of indices into the protocol plugin.An empty list indicates all instances in the plugin.
        - Returns list(str): Please provide a proper description here.

        Raises
        ------
        - NotFoundError: The requested resource does not exist on the server
        - ServerError: The server has encountered an uncategorized error condition
        """
        payload = { "Arg1": self.href }
        for i in range(len(args)): payload['Arg%s' % (i + 2)] = args[i]
        for item in kwargs.items(): payload[item[0]] = item[1]
        return self._execute('getCfmAISDbLearnedInformation', payload=payload, response_object=None)

    def GetCfmCcmLearnedInformation(self, *args, **kwargs):
        """Executes the getCfmCcmLearnedInformation operation on the server.

        Get CCM Learned Info

        The IxNetwork model allows for multiple method Signatures with the same name while python does not.

        getCfmCcmLearnedInformation(SessionIndices=list)
        ------------------------------------------------
        - SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

        getCfmCcmLearnedInformation(SessionIndices=string)
        --------------------------------------------------
        - SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

        getCfmCcmLearnedInformation(Arg2=list)list
        ------------------------------------------
        - Arg2 (list(number)): List of indices into the protocol plugin.An empty list indicates all instances in the plugin.
        - Returns list(str): Please provide a proper description here.

        Raises
        ------
        - NotFoundError: The requested resource does not exist on the server
        - ServerError: The server has encountered an uncategorized error condition
        """
        payload = { "Arg1": self }
        for i in range(len(args)): payload['Arg%s' % (i + 2)] = args[i]
        for item in kwargs.items(): payload[item[0]] = item[1]
        return self._execute('getCfmCcmLearnedInformation', payload=payload, response_object=None)

    def GetCfmDMDbLearnedInformation(self, *args, **kwargs):
        """Executes the getCfmDMDbLearnedInformation operation on the server.

        Get Learned DM Information

        getCfmDMDbLearnedInformation(Arg2=list)list
        -------------------------------------------
        - Arg2 (list(number)): List of indices into the protocol plugin.An empty list indicates all instances in the plugin.
        - Returns list(str): Please provide a proper description here.

        Raises
        ------
        - NotFoundError: The requested resource does not exist on the server
        - ServerError: The server has encountered an uncategorized error condition
        """
        payload = { "Arg1": self.href }
        for i in range(len(args)): payload['Arg%s' % (i + 2)] = args[i]
        for item in kwargs.items(): payload[item[0]] = item[1]
        return self._execute('getCfmDMDbLearnedInformation', payload=payload, response_object=None)

    def GetCfmLCKDbLearnedInformation(self, *args, **kwargs):
        """Executes the getCfmLCKDbLearnedInformation operation on the server.

        Get Learned LCK Information

        getCfmLCKDbLearnedInformation(Arg2=list)list
        --------------------------------------------
        - Arg2 (list(number)): List of indices into the protocol plugin.An empty list indicates all instances in the plugin.
        - Returns list(str): Please provide a proper description here.

        Raises
        ------
        - NotFoundError: The requested resource does not exist on the server
        - ServerError: The server has encountered an uncategorized error condition
        """
        payload = { "Arg1": self.href }
        for i in range(len(args)): payload['Arg%s' % (i + 2)] = args[i]
        for item in kwargs.items(): payload[item[0]] = item[1]
        return self._execute('getCfmLCKDbLearnedInformation', payload=payload, response_object=None)

    def GetCfmLinkTraceDbLearnedInformation(self, *args, **kwargs):
        """Executes the getCfmLinkTraceDbLearnedInformation operation on the server.

        Get LinkTrace Learned Info

        The IxNetwork model allows for multiple method Signatures with the same name while python does not.

        getCfmLinkTraceDbLearnedInformation(SessionIndices=list)
        --------------------------------------------------------
        - SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

        getCfmLinkTraceDbLearnedInformation(SessionIndices=string)
        ----------------------------------------------------------
        - SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

        getCfmLinkTraceDbLearnedInformation(Arg2=list)list
        --------------------------------------------------
        - Arg2 (list(number)): List of indices into the protocol plugin.An empty list indicates all instances in the plugin.
        - Returns list(str): Please provide a proper description here.

        Raises
        ------
        - NotFoundError: The requested resource does not exist on the server
        - ServerError: The server has encountered an uncategorized error condition
        """
        payload = { "Arg1": self }
        for i in range(len(args)): payload['Arg%s' % (i + 2)] = args[i]
        for item in kwargs.items(): payload[item[0]] = item[1]
        return self._execute('getCfmLinkTraceDbLearnedInformation', payload=payload, response_object=None)

    def GetCfmLMDbLearnedInformation(self, *args, **kwargs):
        """Executes the getCfmLMDbLearnedInformation operation on the server.

        Get Learned LM Information

        getCfmLMDbLearnedInformation(Arg2=list)list
        -------------------------------------------
        - Arg2 (list(number)): List of indices into the protocol plugin.An empty list indicates all instances in the plugin.
        - Returns list(str): Please provide a proper description here.

        Raises
        ------
        - NotFoundError: The requested resource does not exist on the server
        - ServerError: The server has encountered an uncategorized error condition
        """
        payload = { "Arg1": self.href }
        for i in range(len(args)): payload['Arg%s' % (i + 2)] = args[i]
        for item in kwargs.items(): payload[item[0]] = item[1]
        return self._execute('getCfmLMDbLearnedInformation', payload=payload, response_object=None)

    def GetCfmLoopbackDbLearnedInformation(self, *args, **kwargs):
        """Executes the getCfmLoopbackDbLearnedInformation operation on the server.

        Get LoopBack Learned Info

        The IxNetwork model allows for multiple method Signatures with the same name while python does not.

        getCfmLoopbackDbLearnedInformation(SessionIndices=list)
        -------------------------------------------------------
        - SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

        getCfmLoopbackDbLearnedInformation(SessionIndices=string)
        ---------------------------------------------------------
        - SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

        getCfmLoopbackDbLearnedInformation(Arg2=list)list
        -------------------------------------------------
        - Arg2 (list(number)): List of indices into the protocol plugin.An empty list indicates all instances in the plugin.
        - Returns list(str): Please provide a proper description here.

        Raises
        ------
        - NotFoundError: The requested resource does not exist on the server
        - ServerError: The server has encountered an uncategorized error condition
        """
        payload = { "Arg1": self }
        for i in range(len(args)): payload['Arg%s' % (i + 2)] = args[i]
        for item in kwargs.items(): payload[item[0]] = item[1]
        return self._execute('getCfmLoopbackDbLearnedInformation', payload=payload, response_object=None)

    def GetCfmTSTDbLearnedInformation(self, *args, **kwargs):
        """Executes the getCfmTSTDbLearnedInformation operation on the server.

        Get Learned TST Information

        getCfmTSTDbLearnedInformation(Arg2=list)list
        --------------------------------------------
        - Arg2 (list(number)): List of indices into the protocol plugin.An empty list indicates all instances in the plugin.
        - Returns list(str): Please provide a proper description here.

        Raises
        ------
        - NotFoundError: The requested resource does not exist on the server
        - ServerError: The server has encountered an uncategorized error condition
        """
        payload = { "Arg1": self.href }
        for i in range(len(args)): payload['Arg%s' % (i + 2)] = args[i]
        for item in kwargs.items(): payload[item[0]] = item[1]
        return self._execute('getCfmTSTDbLearnedInformation', payload=payload, response_object=None)

    def GetPeriodicOAMLearnedInformation(self, *args, **kwargs):
        """Executes the getPeriodicOAMLearnedInformation operation on the server.

        Get All Periodic Learned Info

        The IxNetwork model allows for multiple method Signatures with the same name while python does not.

        getPeriodicOAMLearnedInformation(SessionIndices=list)
        -----------------------------------------------------
        - SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

        getPeriodicOAMLearnedInformation(SessionIndices=string)
        -------------------------------------------------------
        - SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

        getPeriodicOAMLearnedInformation(Arg2=list)list
        -----------------------------------------------
        - Arg2 (list(number)): List of indices into the protocol plugin.An empty list indicates all instances in the plugin.
        - Returns list(str): Please provide a proper description here.

        Raises
        ------
        - NotFoundError: The requested resource does not exist on the server
        - ServerError: The server has encountered an uncategorized error condition
        """
        payload = { "Arg1": self }
        for i in range(len(args)): payload['Arg%s' % (i + 2)] = args[i]
        for item in kwargs.items(): payload[item[0]] = item[1]
        return self._execute('getPeriodicOAMLearnedInformation', payload=payload, response_object=None)

    def RestartDown(self, *args, **kwargs):
        """Executes the restartDown operation on the server.

        Stop and start interfaces and sessions that are in Down state.

        The IxNetwork model allows for multiple method Signatures with the same name while python does not.

        restartDown(SessionIndices=list)
        --------------------------------
        - SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

        restartDown(SessionIndices=string)
        ----------------------------------
        - SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

        Raises
        ------
        - NotFoundError: The requested resource does not exist on the server
        - ServerError: The server has encountered an uncategorized error condition
        """
        payload = { "Arg1": self }
        for i in range(len(args)): payload['Arg%s' % (i + 2)] = args[i]
        for item in kwargs.items(): payload[item[0]] = item[1]
        return self._execute('restartDown', payload=payload, response_object=None)

    def Start(self, *args, **kwargs):
        """Executes the start operation on the server.

        Start CFM Bridge

        The IxNetwork model allows for multiple method Signatures with the same name while python does not.

        start(SessionIndices=list)
        --------------------------
        - SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

        start(SessionIndices=string)
        ----------------------------
        - SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

        Raises
        ------
        - NotFoundError: The requested resource does not exist on the server
        - ServerError: The server has encountered an uncategorized error condition
        """
        payload = { "Arg1": self }
        for i in range(len(args)): payload['Arg%s' % (i + 2)] = args[i]
        for item in kwargs.items(): payload[item[0]] = item[1]
        return self._execute('start', payload=payload, response_object=None)

    def Stop(self, *args, **kwargs):
        """Executes the stop operation on the server.

        Stop CFM Bridge

        The IxNetwork model allows for multiple method Signatures with the same name while python does not.

        stop(SessionIndices=list)
        -------------------------
        - SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

        stop(SessionIndices=string)
        ---------------------------
        - SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

        Raises
        ------
        - NotFoundError: The requested resource does not exist on the server
        - ServerError: The server has encountered an uncategorized error condition
        """
        payload = { "Arg1": self }
        for i in range(len(args)): payload['Arg%s' % (i + 2)] = args[i]
        for item in kwargs.items(): payload[item[0]] = item[1]
        return self._execute('stop', payload=payload, response_object=None)
