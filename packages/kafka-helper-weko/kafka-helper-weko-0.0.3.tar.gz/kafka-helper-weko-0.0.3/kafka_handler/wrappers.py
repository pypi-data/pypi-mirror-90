from abc import abstractmethod


class KafkaTask:
    """
    Base class for handler kafka message
    """
    __is_kafka__ = True
    __action__ = None  # Set action name for triggering handler

    def __init__(self, logger):
        assert self.__action__, 'Action name missed'
        self.logger = logger
        self.logger.info(f"{self.__class__.__name__} {self.__action__} action class inited")

    def __call__(self, data):
        self.set_up(**data)
        self.complete()
        self.finish()

    @abstractmethod
    def complete(self):
        """
        Main code of handler function
        :return: None
        """
        raise NotImplemented('complete method should be implemented')

    def finish(self):  # Called on task success finish
        self.logger.info(f'Task {self.__action__} finished')

    @abstractmethod
    def set_up(self, **kwargs):
        """
        Set up instance fields before start handling
        :return: None
        """
        raise NotImplemented('set_up method should be implemented')


def task(action, name=None):
    """
    Wraps function for kafka-handler detector
    :param action: Action for triggering function
    :param name: TODO
    """
    def wrapping(func):
        func.__is_kafka__ = True
        func.__action__ = action
        func.__name__ = name if name else func.__name__
        return func
    return wrapping
