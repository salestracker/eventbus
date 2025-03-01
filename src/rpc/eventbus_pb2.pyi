from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import (
    ClassVar as _ClassVar,
    Iterable as _Iterable,
    Mapping as _Mapping,
    Optional as _Optional,
    Union as _Union,
)

DESCRIPTOR: _descriptor.FileDescriptor

class SingleValue(_message.Message):
    __slots__ = (
        "string_val",
        "int32_val",
        "int64_val",
        "uint32_val",
        "uint64_val",
        "sint32_val",
        "sint64_val",
        "bool_val",
        "byte_val",
        "fixed32_val",
        "fixed64_val",
        "double_val",
        "float_val",
    )
    STRING_VAL_FIELD_NUMBER: _ClassVar[int]
    INT32_VAL_FIELD_NUMBER: _ClassVar[int]
    INT64_VAL_FIELD_NUMBER: _ClassVar[int]
    UINT32_VAL_FIELD_NUMBER: _ClassVar[int]
    UINT64_VAL_FIELD_NUMBER: _ClassVar[int]
    SINT32_VAL_FIELD_NUMBER: _ClassVar[int]
    SINT64_VAL_FIELD_NUMBER: _ClassVar[int]
    BOOL_VAL_FIELD_NUMBER: _ClassVar[int]
    BYTE_VAL_FIELD_NUMBER: _ClassVar[int]
    FIXED32_VAL_FIELD_NUMBER: _ClassVar[int]
    FIXED64_VAL_FIELD_NUMBER: _ClassVar[int]
    DOUBLE_VAL_FIELD_NUMBER: _ClassVar[int]
    FLOAT_VAL_FIELD_NUMBER: _ClassVar[int]
    string_val: str
    int32_val: int
    int64_val: int
    uint32_val: int
    uint64_val: int
    sint32_val: int
    sint64_val: int
    bool_val: bool
    byte_val: bytes
    fixed32_val: int
    fixed64_val: int
    double_val: float
    float_val: float
    def __init__(
        self,
        string_val: _Optional[str] = ...,
        int32_val: _Optional[int] = ...,
        int64_val: _Optional[int] = ...,
        uint32_val: _Optional[int] = ...,
        uint64_val: _Optional[int] = ...,
        sint32_val: _Optional[int] = ...,
        sint64_val: _Optional[int] = ...,
        bool_val: bool = ...,
        byte_val: _Optional[bytes] = ...,
        fixed32_val: _Optional[int] = ...,
        fixed64_val: _Optional[int] = ...,
        double_val: _Optional[float] = ...,
        float_val: _Optional[float] = ...,
    ) -> None: ...

class ListValue(_message.Message):
    __slots__ = (
        "string_list",
        "int32_list",
        "int64_list",
        "uint32_list",
        "uint64_list",
        "sint32_list",
        "sint64_list",
        "bool_list",
        "byte_list",
        "fixed32_list",
        "fixed64_list",
        "double_list",
        "float_list",
    )
    STRING_LIST_FIELD_NUMBER: _ClassVar[int]
    INT32_LIST_FIELD_NUMBER: _ClassVar[int]
    INT64_LIST_FIELD_NUMBER: _ClassVar[int]
    UINT32_LIST_FIELD_NUMBER: _ClassVar[int]
    UINT64_LIST_FIELD_NUMBER: _ClassVar[int]
    SINT32_LIST_FIELD_NUMBER: _ClassVar[int]
    SINT64_LIST_FIELD_NUMBER: _ClassVar[int]
    BOOL_LIST_FIELD_NUMBER: _ClassVar[int]
    BYTE_LIST_FIELD_NUMBER: _ClassVar[int]
    FIXED32_LIST_FIELD_NUMBER: _ClassVar[int]
    FIXED64_LIST_FIELD_NUMBER: _ClassVar[int]
    DOUBLE_LIST_FIELD_NUMBER: _ClassVar[int]
    FLOAT_LIST_FIELD_NUMBER: _ClassVar[int]
    string_list: _containers.RepeatedScalarFieldContainer[str]
    int32_list: _containers.RepeatedScalarFieldContainer[int]
    int64_list: _containers.RepeatedScalarFieldContainer[int]
    uint32_list: _containers.RepeatedScalarFieldContainer[int]
    uint64_list: _containers.RepeatedScalarFieldContainer[int]
    sint32_list: _containers.RepeatedScalarFieldContainer[int]
    sint64_list: _containers.RepeatedScalarFieldContainer[int]
    bool_list: _containers.RepeatedScalarFieldContainer[bool]
    byte_list: _containers.RepeatedScalarFieldContainer[bytes]
    fixed32_list: _containers.RepeatedScalarFieldContainer[int]
    fixed64_list: _containers.RepeatedScalarFieldContainer[int]
    double_list: _containers.RepeatedScalarFieldContainer[float]
    float_list: _containers.RepeatedScalarFieldContainer[float]
    def __init__(
        self,
        string_list: _Optional[_Iterable[str]] = ...,
        int32_list: _Optional[_Iterable[int]] = ...,
        int64_list: _Optional[_Iterable[int]] = ...,
        uint32_list: _Optional[_Iterable[int]] = ...,
        uint64_list: _Optional[_Iterable[int]] = ...,
        sint32_list: _Optional[_Iterable[int]] = ...,
        sint64_list: _Optional[_Iterable[int]] = ...,
        bool_list: _Optional[_Iterable[bool]] = ...,
        byte_list: _Optional[_Iterable[bytes]] = ...,
        fixed32_list: _Optional[_Iterable[int]] = ...,
        fixed64_list: _Optional[_Iterable[int]] = ...,
        double_list: _Optional[_Iterable[float]] = ...,
        float_list: _Optional[_Iterable[float]] = ...,
    ) -> None: ...

class PayloadValue(_message.Message):
    __slots__ = ("single_datatype", "list_datatype")
    SINGLE_DATATYPE_FIELD_NUMBER: _ClassVar[int]
    LIST_DATATYPE_FIELD_NUMBER: _ClassVar[int]
    single_datatype: SingleValue
    list_datatype: ListValue
    def __init__(
        self,
        single_datatype: _Optional[_Union[SingleValue, _Mapping]] = ...,
        list_datatype: _Optional[_Union[ListValue, _Mapping]] = ...,
    ) -> None: ...

class Event(_message.Message):
    __slots__ = ("event_name", "payload", "correlation_id", "ttl")
    class PayloadEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: PayloadValue
        def __init__(
            self,
            key: _Optional[str] = ...,
            value: _Optional[_Union[PayloadValue, _Mapping]] = ...,
        ) -> None: ...

    EVENT_NAME_FIELD_NUMBER: _ClassVar[int]
    PAYLOAD_FIELD_NUMBER: _ClassVar[int]
    CORRELATION_ID_FIELD_NUMBER: _ClassVar[int]
    TTL_FIELD_NUMBER: _ClassVar[int]
    event_name: str
    payload: _containers.MessageMap[str, PayloadValue]
    correlation_id: str
    ttl: int
    def __init__(
        self,
        event_name: _Optional[str] = ...,
        payload: _Optional[_Mapping[str, PayloadValue]] = ...,
        correlation_id: _Optional[str] = ...,
        ttl: _Optional[int] = ...,
    ) -> None: ...

class EventRequest(_message.Message):
    __slots__ = ("event",)
    EVENT_FIELD_NUMBER: _ClassVar[int]
    event: Event
    def __init__(self, event: _Optional[_Union[Event, _Mapping]] = ...) -> None: ...

class ResponseType(_message.Message):
    __slots__ = ("success", "failure")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    FAILURE_FIELD_NUMBER: _ClassVar[int]
    success: bool
    failure: bool
    def __init__(self, success: bool = ..., failure: bool = ...) -> None: ...

class EventResponse(_message.Message):
    __slots__ = ("response", "error_message")
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    response: ResponseType
    error_message: str
    def __init__(
        self,
        response: _Optional[_Union[ResponseType, _Mapping]] = ...,
        error_message: _Optional[str] = ...,
    ) -> None: ...

class SubscribeEventStream(_message.Message):
    __slots__ = ("event_name", "subscriber_id")
    EVENT_NAME_FIELD_NUMBER: _ClassVar[int]
    SUBSCRIBER_ID_FIELD_NUMBER: _ClassVar[int]
    event_name: str
    subscriber_id: str
    def __init__(
        self, event_name: _Optional[str] = ..., subscriber_id: _Optional[str] = ...
    ) -> None: ...

class SubscriberResponse(_message.Message):
    __slots__ = ("event", "subscriber_id")
    EVENT_FIELD_NUMBER: _ClassVar[int]
    SUBSCRIBER_ID_FIELD_NUMBER: _ClassVar[int]
    event: Event
    subscriber_id: str
    def __init__(
        self,
        event: _Optional[_Union[Event, _Mapping]] = ...,
        subscriber_id: _Optional[str] = ...,
    ) -> None: ...

class SubscriberStreamResponse(_message.Message):
    __slots__ = ("response", "error_message")
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    response: SubscriberResponse
    error_message: str
    def __init__(
        self,
        response: _Optional[_Union[SubscriberResponse, _Mapping]] = ...,
        error_message: _Optional[str] = ...,
    ) -> None: ...
