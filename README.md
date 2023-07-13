## Verry basic question answering workflow for [Memos](usememos.com)


### Quickstart
QA:
```bash
Usage: q.py [OPTIONS] QUESTION

Options:
  --memo-url TEXT    url with the OpenID key to acces your Memos instance 
                     [required]
  --openai-key TEXT  OpenAI API Key (optional)
  --openai BOOLEAN   whether to use OpenAI API
  --index-file TEXT  index filename
  --help             Show this message and exit.
```
### Setup

```bash
# activate your environement if necessary
# source venv/bin/activate
# conda activate myenv
# install the dependencies
pip install -r requirements.txt 
# download the embedding model (420 MB)
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-mpnet-base-v2')" 
# download the question answering model (~450 MB)
python -c "from transformers import pipeline self.nlp = pipeline('question-answering', model='deepset/roberta-base-squad2', tokenizer='deepset/roberta-base-squad2')" 
```

- Retrive the OpenAPI endpoint with the key

    eg: `https://demo.usememos.com/api/v1/memo?openId=81944554-2f01-46a0-aced-0459b747c67b`

- run the `qa.py` script

### dependencies
```
- faiss-cpu or faiss-gpu
- numpy
- requests
- sentence_transformers
- openai (optional)
```

### Api
A non exhaustive python api wrapper was made in `api.py`