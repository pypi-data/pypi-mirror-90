

import autest.glb as glb
import hosts.output as host
from autest.core.conditions import ConditionFactory


def ExtendCondition(func, name=None):
    if not glb.running_main:
        return

    if name is None:
        name = func.__name__

    if hasattr(ConditionFactory, name):
        host.WriteWarningf("Condition already has a '{name}' test! Overidding with new function", name=name)

    setattr(ConditionFactory, name, func)
    host.WriteVerbose("api",
                      'Added Condition extension function "{0}"'.format(name))
