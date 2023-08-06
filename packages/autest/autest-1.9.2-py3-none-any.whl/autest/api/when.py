
import autest.glb as glb
import hosts.output as host


def AddWhenFunction(func, name=None, generator=False):
    if not glb.running_main:
        return
    if name is None:
        name = func.__name__

    def wrapper(self, *lst, **kw):
        if lst != () or kw != {}:
            # we have arguments, bind them to call with lambda
            return func(*lst, **kw) if generator else lambda: func(*lst, **kw)
        return func

    wrapper.when_wrapper = True
    method = wrapper
    setattr(glb.When, name, method)
    host.WriteVerbose("api", 'Added extension function "{0}"'.format(name))
