from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SioPackageListResponse(_message.Message):
    __slots__ = ()
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    PACKAGES_FIELD_NUMBER: _ClassVar[int]
    success: bool
    error: str
    packages: _struct_pb2.Struct
    def __init__(self, success: _Optional[bool] = ..., error: _Optional[str] = ..., packages: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...
