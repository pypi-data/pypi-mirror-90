from functools import wraps

from concurrentevents.enums import Priority


def catch(event, priority=Priority.MEDIUM):
    """
    This is a decorator for adding member variables to a function
    that should be a handler of a specific event

    .. highlight:: python
    .. code-block:: python

        class ExampleHandler(EventHandler):

            @Catch("Start")
            def foo():
                bar()

            @Catch("Exit", priority=5)
            def bar():
                pass

    :param str event: A string key
    :param class:`concurrentevents.Priority` int priority: Int or Priority used to sort handlers for ordering

    :raises TypeError: If any unaccepted values are passed in for either argument
    """
    if not isinstance(event, str):
        raise TypeError(f"Catch() event argument must be an event or string, not {event}")

    if not isinstance(priority, (int, Priority)):
        raise TypeError(f"Catch() priority argument must be an int or `Priority`, not {priority}")

    def decorator(func):
        func.event = event
        func.priority = int(priority)

        return wraps(func)(lambda *args, **kwargs: func(*args, **kwargs))

    return decorator
