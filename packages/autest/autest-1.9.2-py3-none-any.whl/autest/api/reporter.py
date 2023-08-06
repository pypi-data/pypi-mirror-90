
import autest.glb as glb
import hosts.output as host


def RegisterReporter(func, name=None):

    if not glb.running_main:
        return
    if name is None:
        name = func.__name__
    glb.reporters[name] = func
    host.WriteVerbose("api", 'Registered reporter "{0}"'.format(name))
