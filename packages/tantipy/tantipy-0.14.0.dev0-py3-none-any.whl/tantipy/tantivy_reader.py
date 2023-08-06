from typing import (
    Iterable,
    Tuple,
)

import brotli
from izihawa_types.var import (
    process_varint,
    process_varstr,
)

from .tantivy_coder import TantivyCoder


def auto_process_varint(data):
    var, length = process_varint(data, inverted=True)
    return var, data[length:]


def read_footer(data: bytes) -> Tuple[bytes, bytes]:
    footer_len = int.from_bytes(data[-4:], 'little', signed=False)
    data = data[:-4]
    body, footer = data[:-footer_len], data[-footer_len:]
    return body, footer


def read_store(body: bytes) -> Tuple[bytes, bytes]:
    offset = int.from_bytes(body[-8:], 'little', signed=False)
    return body[:offset], body[offset:-8]


def parse_footer(footer: bytes) -> Tuple[int, int, bytes]:
    footer_length, footer = auto_process_varint(footer)
    version = int.from_bytes(footer[:4], 'little', signed=False)
    crc = int.from_bytes(footer[4:8], 'little', signed=False)
    compression, _ = process_varstr(footer[8:], inverted=True)
    return version, crc, compression


def read_layers(skip_index):
    layers = []
    skip_index_length, skip_index = auto_process_varint(skip_index)
    start_offset = 0
    for i in range(skip_index_length):
        end_offset, skip_index = auto_process_varint(skip_index)
        layers.append((start_offset, end_offset))
        start_offset = end_offset
    return layers, skip_index


def parse_blocks(last_layer):
    checkpoints = []
    while last_layer:
        length, last_layer = auto_process_varint(last_layer)
        if length == 0:
            continue
        doc_id, last_layer = auto_process_varint(last_layer)
        start_offset, last_layer = auto_process_varint(last_layer)
        for i in range(length):
            num_docs, last_layer = auto_process_varint(last_layer)
            block_num_bytes, last_layer = auto_process_varint(last_layer)
            checkpoints.append({
                'start_doc': doc_id,
                'end_doc': doc_id + num_docs,
                'start_offset': start_offset,
                'end_offset': start_offset + block_num_bytes,
            })
            doc_id += num_docs
            start_offset += block_num_bytes
    return checkpoints


class TantivyReader:
    def __init__(self, store: bytes, coder: TantivyCoder):
        self.store = store
        self.coder = coder

    def documents(self) -> Iterable[dict]:
        """
        Iterates over all document inside `.store`

        Returns:
            Document generator
        """
        body, footer = read_footer(self.store)
        store, skip_index = read_store(body)
        layers, skip_index = read_layers(skip_index)

        checkpoints = parse_blocks(skip_index[layers[-1][0]:layers[-1][1]])

        for checkpoint in checkpoints:
            decompressed = brotli.decompress(store[checkpoint['start_offset']:checkpoint['end_offset']])
            while decompressed:
                doc_length, decompressed = auto_process_varint(decompressed)
                document = self.coder.decode_document(decompressed)
                yield document
                decompressed = decompressed[doc_length:]
