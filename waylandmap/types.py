from typing import Type, Callable


LogInput = tuple[float, int, int, int]
LogOutput = tuple[tuple[int, int], int] | None
FilterOutput = tuple[tuple[int, int], int] | None
RetryCatch = tuple[Type[Exception], ...]
RetryWrapped = Callable[..., None]
RetryWrapper = Callable[[Type[Callable]], Type[RetryWrapped]]
