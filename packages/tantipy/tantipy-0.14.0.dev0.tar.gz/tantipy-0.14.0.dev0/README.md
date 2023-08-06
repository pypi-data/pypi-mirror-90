# Tantipy

Tantipy is a pure python tool for reading Tantivy `.store` files.

## Example

```python
import json
import os

from tantipy import TantivyReader


index_path = '...'
with open(os.path.join(index_path, 'meta.json')) as schema_file:
    schema = json.load(schema_file)['schema']

with open(os.path.join(index_path, '687e95d2e6f54a3cb1008e69ebbebdd9.store')) as store_file:
    content = store_file.read()
    tantivy_reader = TantivyReader(content, schema)
    for document in tantivy_reader.documents():
        print(document)
```