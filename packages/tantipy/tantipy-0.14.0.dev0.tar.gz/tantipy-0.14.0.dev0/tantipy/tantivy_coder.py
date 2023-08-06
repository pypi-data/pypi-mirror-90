from typing import (
    Optional,
    Tuple,
    Union,
)

from izihawa_types.var import (
    process_varint,
    process_varstr,
    varint,
    varstr,
)


class TantivyDocument(dict):
    def __getattr__(self, item):
        return self.get(item)

    def __setattr__(self, item, value):
        self[item] = value


class TantivyCoder:
    def __init__(self, schema_config: dict):
        self.schema_config = schema_config.copy()
        if 'multi_fields' in self.schema_config:
            self.schema_config['multi_fields'] = set(self.schema_config['multi_fields'])

    def decode_field(self, reader: bytes) -> Tuple[int, Union[Optional[bytes], int], bytes]:
        field_id = int.from_bytes(reader[:4], 'little', signed=False)
        reader = reader[4:]
        type_ = int.from_bytes(reader[:1], 'little', signed=False)
        reader = reader[1:]
        if type_ == 0:
            value, length = process_varstr(reader, inverted=True)
            value = value.decode()
            reader = reader[length:]
        elif type_ == 1:
            value = int.from_bytes(reader[:8], 'little', signed=False)
            reader = reader[8:]
        elif type_ == 2:
            value = int.from_bytes(reader[:8], 'little', signed=True)
            reader = reader[8:]
        else:
            return field_id, None, reader
        return field_id, value, reader

    def encode_field(self, field_id: int, type_: str, values) -> bytes:
        # ToDo: Unknown types
        buf = bytes()
        for value in values:
            buf += int.to_bytes(field_id, 4, 'little', signed=False)
            if type_ == 'text':
                buf += int.to_bytes(0, 1, 'little', signed=False)
                buf += varstr(value.encode(), inverted=True)
            elif type_ == 'u64':
                buf += int.to_bytes(1, 1, 'little', signed=False)
                buf += int.to_bytes(value, 8, 'little', signed=False)
            elif type_ == 'i64':
                buf += int.to_bytes(2, 1, 'little', signed=False)
                buf += int.to_bytes(value, 8, 'little', signed=True)
        return buf

    def decode_document(self, document: bytes) -> TantivyDocument:
        num_field_values, length = process_varint(document, inverted=True)
        reader = document[length:]
        document = TantivyDocument()
        for _ in range(num_field_values):
            field_id, value, reader = self.decode_field(reader)
            name = self.schema_config['schema'][field_id]['name']
            if name in self.schema_config['multi_fields']:
                if name not in document:
                    document[name] = []
                document[name].append(value)
            elif name not in document:
                document[name] = value
        return document

    def encode_document(self, document: TantivyDocument) -> bytes:
        encoded = bytes()
        count = 0
        for (i, field) in enumerate(self.schema_config['schema']):
            if hasattr(document, field['name']) and getattr(document, field['name']) is not None:
                values = getattr(document, field['name'])
                if field['name'] not in self.schema_config['multi_fields']:
                    values = [values]
                count += len(values)
                encoded += self.encode_field(i, field['type'], values)
        encoded = varint(count, inverted=True) + encoded
        return encoded
