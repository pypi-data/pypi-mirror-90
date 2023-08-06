

class Lag(object):
    """Generated from OpenAPI schema object #/components/schemas/Lag

    A container for LAG settings  

    Args
    ----
    - name (str): Unique system wide name of an object that is also the primary key for objects found in arrays
    - port_names (list[str]): A list of unique names of port objects that will be part of the same lag
     The value of the port_names property is the count for any child property in this hierarchy that is a container for a device pattern
    - protocol (Protocol): Static lag or LACP protocol settings
    - ethernet (Ethernet): Emulated ethernet protocol
     A top level in the emulated device stack
     Per port ethernet and vlan settings
    """
    def __init__(self, name=None, port_names=[], protocol=None, ethernet=None):
        from abstract_open_traffic_generator.lag import Protocol
        from abstract_open_traffic_generator.device import Ethernet
        if isinstance(name, (str)) is True:
            import re
            assert(bool(re.match(r'^[\sa-zA-Z0-9-_()><\[\]]+$', name)) is True)
            self.name = name
        else:
            raise TypeError('name must be an instance of (str)')
        if isinstance(port_names, (list, type(None))) is True:
            self.port_names = [] if port_names is None else list(port_names)
        else:
            raise TypeError('port_names must be an instance of (list, type(None))')
        if isinstance(protocol, (Protocol)) is True:
            self.protocol = protocol
        else:
            raise TypeError('protocol must be an instance of (Protocol)')
        if isinstance(ethernet, (Ethernet, type(None))) is True:
            self.ethernet = ethernet
        else:
            raise TypeError('ethernet must be an instance of (Ethernet, type(None))')


class Protocol(object):
    """Generated from OpenAPI schema object #/components/schemas/Lag.Protocol

    TBD  

    Args
    ----
    - choice (Union[Lacp, Static]): The type of lag protocol
    """
    _CHOICE_MAP = {
        'Lacp': 'lacp',
        'Static': 'static',
    }
    def __init__(self, choice=None):
        from abstract_open_traffic_generator.lag import Lacp
        from abstract_open_traffic_generator.lag import Static
        if isinstance(choice, (Lacp, Static)) is False:
            raise TypeError('choice must be of type: Lacp, Static')
        self.__setattr__('choice', Protocol._CHOICE_MAP[type(choice).__name__])
        self.__setattr__(Protocol._CHOICE_MAP[type(choice).__name__], choice)


class Static(object):
    """Generated from OpenAPI schema object #/components/schemas/Lag.Static

    TBD  

    Args
    ----
    - lag_id (Pattern): A container for emulated device property patterns
     The static lag id
    """
    def __init__(self, lag_id=None):
        from abstract_open_traffic_generator.device import Pattern
        if isinstance(lag_id, (Pattern, type(None))) is True:
            self.lag_id = lag_id
        else:
            raise TypeError('lag_id must be an instance of (Pattern, type(None))')


class Lacp(object):
    """Generated from OpenAPI schema object #/components/schemas/Lag.Lacp

    TBD  

    Args
    ----
    - actor_key (Pattern): A container for emulated device property patterns
     The actor key
    - actor_port_number (Pattern): A container for emulated device property patterns
     The actor port number
    - actor_port_priority (Pattern): A container for emulated device property patterns
     The actor port priority
    - actor_system_id (Pattern): A container for emulated device property patterns
     The actor system id
    - actor_system_priority (Pattern): A container for emulated device property patterns
     The actor system priority
    """
    def __init__(self, actor_key=None, actor_port_number=None, actor_port_priority=None, actor_system_id=None, actor_system_priority=None):
        from abstract_open_traffic_generator.device import Pattern
        if isinstance(actor_key, (Pattern, type(None))) is True:
            self.actor_key = actor_key
        else:
            raise TypeError('actor_key must be an instance of (Pattern, type(None))')
        if isinstance(actor_port_number, (Pattern, type(None))) is True:
            self.actor_port_number = actor_port_number
        else:
            raise TypeError('actor_port_number must be an instance of (Pattern, type(None))')
        if isinstance(actor_port_priority, (Pattern, type(None))) is True:
            self.actor_port_priority = actor_port_priority
        else:
            raise TypeError('actor_port_priority must be an instance of (Pattern, type(None))')
        if isinstance(actor_system_id, (Pattern, type(None))) is True:
            self.actor_system_id = actor_system_id
        else:
            raise TypeError('actor_system_id must be an instance of (Pattern, type(None))')
        if isinstance(actor_system_priority, (Pattern, type(None))) is True:
            self.actor_system_priority = actor_system_priority
        else:
            raise TypeError('actor_system_priority must be an instance of (Pattern, type(None))')
