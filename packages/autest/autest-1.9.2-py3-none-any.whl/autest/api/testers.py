
import hosts.output as host
import autest.glb as glb
import autest.testers
from autest.testers import Tester


def AddTester(item, name=None):
    if not glb.running_main:
        return
    # helper function

    def wrapper(self, *lst, **kw):
        self._add_item(item(*lst, **kw))

    # check to make sure this is a SetupItem type
    if not issubclass(item, Tester):
        host.WriteError(
            "Object must be subclass of autest.testers.Tester",
            stack=host.getCurrentStack(1)
        )

    # get name of task if user did not provide a value
    if name is None:
        name = item.__name__

    host.WriteVerbose(
        "setupext",
        "Adding Tester extension named: {0}".format(name)
    )
    setattr(autest.testers, name, item)
