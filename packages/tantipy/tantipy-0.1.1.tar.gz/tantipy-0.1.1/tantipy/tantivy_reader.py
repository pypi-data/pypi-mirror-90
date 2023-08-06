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


def read_footer(data: bytes) -> Tuple[bytes, bytes]:
    footer_len = int.from_bytes(data[-4:], 'little', signed=False)
    data = data[:-4]
    body, footer = data[:-footer_len], data[-footer_len:]
    return body, footer


def read_store(body: bytes) -> Tuple[bytes, bytes, int]:
    offset = int.from_bytes(body[-12:-4], 'little', signed=False)
    max_doc = int.from_bytes(body[-4:], 'little', signed=False)
    return body[:offset], body[offset:-12], max_doc


def parse_footer(footer: bytes) -> Tuple[int, int, bytes]:
    footer_length, length = process_varint(footer, inverted=True)
    footer = footer[length:]
    version = int.from_bytes(footer[:4], 'little', signed=False)
    crc = int.from_bytes(footer[4:8], 'little', signed=False)
    compression, _ = process_varstr(footer[8:], inverted=True)
    return version, crc, compression


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
        store, skip_list, max_doc = read_store(body)
        while store:
            block_size = int.from_bytes(store[:4], 'little', signed=False)
            decompressed = brotli.decompress(store[4:block_size + 4])
            while decompressed:
                doc_length, length = process_varint(decompressed, inverted=True)
                decompressed = decompressed[length:]
                document = self.coder.decode_document(decompressed)
                yield document
                decompressed = decompressed[doc_length:]
            store = store[block_size + 4:]
