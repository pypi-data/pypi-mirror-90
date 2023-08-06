from typing import Callable, Union, Awaitable, Any

from eventipy import Event



EventHandler = Callable[[Event], Union[Any, Awaitable[Any]]]
