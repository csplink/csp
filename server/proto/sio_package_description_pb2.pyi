from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SioPackageDescriptionRequest(_message.Message):
    __slots__ = ()
    TYPE_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    type: str
    name: str
    version: str
    def __init__(self, type: _Optional[str] = ..., name: _Optional[str] = ..., version: _Optional[str] = ...) -> None: ...

class SioPackageDescriptionResponse(_message.Message):
    __slots__ = ()
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    success: bool
    error: str
    description: Description
    def __init__(self, success: _Optional[bool] = ..., error: _Optional[str] = ..., description: _Optional[_Union[Description, _Mapping]] = ...) -> None: ...

class Website(_message.Message):
    __slots__ = ()
    BLOG_FIELD_NUMBER: _ClassVar[int]
    GITHUB_FIELD_NUMBER: _ClassVar[int]
    blog: str
    github: str
    def __init__(self, blog: _Optional[str] = ..., github: _Optional[str] = ...) -> None: ...

class Author(_message.Message):
    __slots__ = ()
    NAME_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    WEBSITE_FIELD_NUMBER: _ClassVar[int]
    name: str
    email: str
    website: Website
    def __init__(self, name: _Optional[str] = ..., email: _Optional[str] = ..., website: _Optional[_Union[Website, _Mapping]] = ...) -> None: ...

class Description(_message.Message):
    __slots__ = ()
    class VendorUrlEntry(_message.Message):
        __slots__ = ()
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    class DescriptionEntry(_message.Message):
        __slots__ = ()
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    class UrlEntry(_message.Message):
        __slots__ = ()
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    NAME_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    LICENSE_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    VENDOR_FIELD_NUMBER: _ClassVar[int]
    VENDORURL_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    URL_FIELD_NUMBER: _ClassVar[int]
    SUPPORT_FIELD_NUMBER: _ClassVar[int]
    AUTHOR_FIELD_NUMBER: _ClassVar[int]
    name: str
    version: str
    license: str
    type: str
    vendor: str
    vendorUrl: _containers.ScalarMap[str, str]
    description: _containers.ScalarMap[str, str]
    url: _containers.ScalarMap[str, str]
    support: str
    author: Author
    def __init__(self, name: _Optional[str] = ..., version: _Optional[str] = ..., license: _Optional[str] = ..., type: _Optional[str] = ..., vendor: _Optional[str] = ..., vendorUrl: _Optional[_Mapping[str, str]] = ..., description: _Optional[_Mapping[str, str]] = ..., url: _Optional[_Mapping[str, str]] = ..., support: _Optional[str] = ..., author: _Optional[_Union[Author, _Mapping]] = ...) -> None: ...
