from abc import abstractmethod

import config

import transitions


class Worker(config.THREAD_PARENT):

    class States:
        """Describes states of worker
        """

    class Triggers:
        """
        Describes triggers of worker
        """

    @abstractmethod
    def transitions(self):
        """
        Has to add transitions to state machine of worker
        :return:
        """

    @abstractmethod
    def getinitial(self):
        """
        Get initial state of state machine
        :return: str
        """

    def __init__(self, api, *args, **kwargs):
        """

        :param api: PrivateAPI or PublicAPI instance
        :param storage: Storage-based instance
        :param args: ...
        :param kwargs: ...
        :return:
        """
        config.THREAD_PARENT.__init__(self, *args, **kwargs)
        self.api = api
        self.machine = transitions.Machine(
            model=self,
            states=self.States.__dict__.keys(),
            initial=self.getinitial()
        )
        self.transitions()
        self._alive = True
        self.satelite = None

    @property
    def alive(self):
        return self._alive

    @alive.setter
    def alive(self, value):
        if isinstance(value, bool):
            self._alive = value

    @abstractmethod
    def jobcycle(self):
        """
        This method has to be redefined for worker manualy - it implements the strategy
        of trading ...
        :return:
        """

    def run(self):
        while self.alive:
            self.jobcycle()


def compose2workers(worker1, worker2):
    """
    Composes 2 workers
    :param worker1:
    :param worker2:
    :return: NoneType
    """
    worker1.satelite = worker2
    worker2.satelite = worker1
