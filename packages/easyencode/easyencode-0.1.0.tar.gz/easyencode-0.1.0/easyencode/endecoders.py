import json
from datetime import datetime, date
from abc import abstractmethod

ENCODER_KEY = '__meta_name'


class EncoderMeta:

    @classmethod
    def _encoder_meta_name(cls) -> str:
        return f'__{str(cls)}__'


class DictEncodable(EncoderMeta):

    @abstractmethod
    def to_dict(self) -> dict:
        pass

    def _encode(self) -> dict:
        dct = self.to_dict()
        dct[ENCODER_KEY] = self._encoder_meta_name()
        return dct


class DictDecodable(EncoderMeta):

    @classmethod
    def from_dict(cls, dct: dict):
        return cls(**dct)

    @classmethod
    def _decode(cls, dct: dict):
        return cls.from_dict(dct)


class DictRepresentable(DictEncodable, DictDecodable):
    """Class that is both DictDecodable as DictEncodable.

    This class can autogenerate

    :param DictEncodable: [description]
    :type DictEncodable: [type]
    :param DictDecodable: [description]
    :type DictDecodable: [type]
    """
    pass


def _decodable_keymap() -> dict:
    keymap = {}
    for rclass in DictDecodable.__subclasses__():
        rclass: DictDecodable
        keymap[rclass._encoder_meta_name()] = rclass
    return keymap


def dict_decodable_object_hook(obj: dict):
    keymap = _decodable_keymap()
    if ENCODER_KEY in obj:
        key_value = obj.pop(ENCODER_KEY)
        if key_value in keymap:
            obj = keymap[key_value]._decode(obj)
    return obj


class DictDecodableJSONDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(self, object_hook=dict_decodable_object_hook, *args, **kwargs)


class DictEncodableJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, DictEncodable):
            obj: DictEncodable
            return obj._encode()
        elif isinstance(obj, datetime):
            obj: datetime
            return obj.timestamp()
        elif isinstance(obj, date):
            obj: date
            return obj.isoformat()
        else:
            return json.JSONEncoder.default(self, obj)
