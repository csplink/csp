from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class SioCoderGenerateRequest(_message.Message):
    __slots__ = ()
    PATH_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_FIELD_NUMBER: _ClassVar[int]
    FILES_FIELD_NUMBER: _ClassVar[int]
    path: str
    output: str
    files: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, path: _Optional[str] = ..., output: _Optional[str] = ..., files: _Optional[_Iterable[str]] = ...) -> None: ...

class SioCoderGenerateProgress(_message.Message):
    __slots__ = ()
    COUNT_FIELD_NUMBER: _ClassVar[int]
    INDEX_FIELD_NUMBER: _ClassVar[int]
    FILE_FIELD_NUMBER: _ClassVar[int]
    WRITE_FIELD_NUMBER: _ClassVar[int]
    count: int
    index: int
    file: str
    write: bool
    def __init__(self, count: _Optional[int] = ..., index: _Optional[int] = ..., file: _Optional[str] = ..., write: _Optional[bool] = ...) -> None: ...

class SioCoderGenerateResponse(_message.Message):
    __slots__ = ()
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    success: bool
    error: str
    def __init__(self, success: _Optional[bool] = ..., error: _Optional[str] = ...) -> None: ...
