

from autest.core.testrun import TestRun
import autest.api
from autest.common.constructor import call_base, smart_init
from autest.core.testentity import TestEntity
from autest.core.testerset import TesterSet
import autest.testers as testers
import autest.core.process as process

# deal with subprocess throwing different exceptions on different systems
try:
    WindowsError
except NameError:
    WindowsError = None


@smart_init
class Process(process.Process, TestEntity):
    @call_base(TestEntity=(), Process=("runable", "name", "cmdstr"))
    def __init__(self, runable, name, cmdstr=None):
        self.__streams = object()
        self.__is_running = False
        # setup testables
        # ReturnCode
        self._Register(
            "Process.{0}.ReturnCode".format(self.Name),
            TesterSet(
                testers.Equal,
                "ReturnCode",
                self.FinishedEvent,
                converter=lambda x: int(x) if x is not None else None),
            "ReturnCode")
        # TimeOut
        self._Register(
            "Process.{0}.TimeOut".format(self.Name),
            TesterSet(
                testers.LessThan,
                "TotalRunTime",
                self.RunningEvent,
                converter=float,
                kill_on_failure=True,
                description_group="Time-Out",
                description="Process finishes within expected time"),
            "TimeOut")

        timeout = self.Variables.Autest.Process.TimeOut

        if timeout is not None:
            self.TimeOut = timeout

        # Time
        self._Register(
            "Process.{0}.Time".format(self.Name),
            TesterSet(
                testers.LessThan,
                "TotalTime",
                self.FinishedEvent,
                converter=float,
                kill_on_failure=True),
            "Time")

    def _isRunning(self, value=None):
        if value is not None:
            self.__is_running = value
        return self.__is_running

    # these are to help with discription

    def _isRunningBefore(self):
        return self._isRunning()

    def _isRunningAfter(self):
        return self._isRunning()


# some forwarding functions...
# for backward compatibility
def Command(self, cmdstr):
    self.Processes.Default.Command = cmdstr


def RawCommand(self, cmdstr):
    self.Processes.Default.RawCommand = cmdstr


def ReturnCode(self, val):
    self.Processes.Default.ReturnCode = val


def Time(self, val):
    self.Processes.Default.Time = val


# def TimeOut(self, val):
    #self.Processes.Default.TimeOut = val


# for backward compatibility


class Streams(TestEntity):
    def __init__(self, testrun):
        super(Streams, self).__init__(testrun)

    @property
    def stdout(self):
        return self._Runable.Processes.Default.Streams.stdout

    @stdout.setter
    def stdout(self, val):
        self._Runable.Processes.Default.Streams.stdout = val

    @property
    def stderr(self):
        return self._Runable.Processes.Default.Streams.stderr

    @stderr.setter
    def stderr(self, val):
        self._Runable.Processes.Default.Streams.stderr = val

    @property
    def All(self):
        return self._Runable.Processes.Default.Streams.All

    @All.setter
    def All(self, val):
        self._Runable.Processes.Default.Streams.All = val

    @property
    def Warning(self):
        return self._Runable.Processes.Default.Streams.Warning

    @Warning.setter
    def Warning(self, val):
        self._Runable.Processes.Default.Streams.Warning = val

    @property
    def Error(self):
        return self._Runable.Processes.Default.Streams.Error

    @Error.setter
    def Error(self, val):
        self._Runable.Processes.Default.Streams.Error = val

    @property
    def Debug(self):
        return self._Runable.Processes.Default.Streams.Debug

    @Debug.setter
    def Debug(self, val):
        self._Runable.Processes.Default.Streams.Debug = val

    @property
    def Verbose(self):
        return self._Runable.Processes.Default.Streams.Verbose

    @Verbose.setter
    def Verbose(self, val):
        self._Runable.Processes.Default.Streams.Verbose = val


autest.api.AddTestEntityMember(Streams, classes=[TestRun])
autest.api.ExtendTestRun(Command, setproperty=True)
autest.api.ExtendTestRun(RawCommand, setproperty=True)
autest.api.ExtendTestRun(ReturnCode, setproperty=True)
autest.api.ExtendTestRun(Time, setproperty=True)
#autest.api.ExtendTestRun(TimeOut, setproperty=True)
