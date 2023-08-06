# dada-client

A lightweight API client for `dada-lake`.

```python
from dada_client import DadaClient 

dada = DadaClient(url='https://dada.lake', api_key='dev')
dada.files.search(ext='mp3')
```

