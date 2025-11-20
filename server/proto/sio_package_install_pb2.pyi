from proto import sio_package_description_pb2 as _sio_package_description_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SioPackageInstallRequest(_message.Message):
    __slots__ = ()
    PATH_FIELD_NUMBER: _ClassVar[int]
    path: str
    def __init__(self, path: _Optional[str] = ...) -> None: ...

class SioPackageInstallProgress(_message.Message):
    __slots__ = ()
    COUNT_FIELD_NUMBER: _ClassVar[int]
    INDEX_FIELD_NUMBER: _ClassVar[int]
    FILE_FIELD_NUMBER: _ClassVar[int]
    count: int
    index: int
    file: str
    def __init__(self, count: _Optional[int] = ..., index: _Optional[int] = ..., file: _Optional[str] = ...) -> None: ...

class SioPackageInstallResponse(_message.Message):
    __slots__ = ()
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    success: bool
    error: str
    description: _sio_package_description_pb2.Description
    def __init__(self, success: _Optional[bool] = ..., error: _Optional[str] = ..., description: _Optional[_Union[_sio_package_description_pb2.Description, _Mapping]] = ...) -> None: ...
