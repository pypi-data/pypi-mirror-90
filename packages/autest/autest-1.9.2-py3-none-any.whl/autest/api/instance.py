
import types

import autest.glb as glb
import hosts.output as host


def AddMethodToInstance(obj, method, name=None):
    '''Add method to provided object instance with optional name'''
    if not glb.running_main:
        return
    if name is None:
        name = method.__name__
    setattr(obj, name, types.MethodType(method, obj))
    host.WriteVerbose("api",
                      'Added method "{0}" to instance {1}'.format(name, obj))
