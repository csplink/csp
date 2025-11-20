from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SioCoderDumpRequest(_message.Message):
    __slots__ = ()
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    DIFF_FIELD_NUMBER: _ClassVar[int]
    content: _struct_pb2.Struct
    path: str
    diff: bool
    def __init__(self, content: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., path: _Optional[str] = ..., diff: _Optional[bool] = ...) -> None: ...

class SioCoderDumpProgress(_message.Message):
    __slots__ = ()
    COUNT_FIELD_NUMBER: _ClassVar[int]
    INDEX_FIELD_NUMBER: _ClassVar[int]
    FILE_FIELD_NUMBER: _ClassVar[int]
    count: int
    index: int
    file: str
    def __init__(self, count: _Optional[int] = ..., index: _Optional[int] = ..., file: _Optional[str] = ...) -> None: ...

class SioCoderDumpResponseFile(_message.Message):
    __slots__ = ()
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    DIFF_FIELD_NUMBER: _ClassVar[int]
    content: str
    diff: str
    def __init__(self, content: _Optional[str] = ..., diff: _Optional[str] = ...) -> None: ...

class SioCoderDumpResponse(_message.Message):
    __slots__ = ()
    class FilesEntry(_message.Message):
        __slots__ = ()
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: SioCoderDumpResponseFile
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[SioCoderDumpResponseFile, _Mapping]] = ...) -> None: ...
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    FILES_FIELD_NUMBER: _ClassVar[int]
    success: bool
    error: str
    files: _containers.MessageMap[str, SioCoderDumpResponseFile]
    def __init__(self, success: _Optional[bool] = ..., error: _Optional[str] = ..., files: _Optional[_Mapping[str, SioCoderDumpResponseFile]] = ...) -> None: ...
