## Verry basic question answering workflow for [Memos](usememos.com)


### Quickstart
QA:
```bash
export OPENAI_API_KEY="sk-1235611234456123456"
export MEMO_URL="https://[[DOMAIN_NAME_OR_IP]]/api/memo?openId=[[OPENIDKEY]]"
python qa.py "how long did the meeting with Julie lasted ?" --ask-gpt'
```
Memos Retrieval:
```bash
export MEMO_URL="https://[[DOMAIN_NAME_OR_IP]]/api/memo?openId=[[OPENIDKEY]]"
python qa.py "Where does Tom live ?"'
```

### Setup

```bash
# activate your environement if necessary
# source venv/bin/activate
# conda activate myenv
# install the dependencies
pip install -r requirements.txt 
# download the embedding model (420 MB)
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer(model)" 
```

- Retrive the OpenAPI endpoint with the key

    eg: `https://demo.usememos.com/api/v1/memo?openId=81944554-2f01-46a0-aced-0459b747c67b`

- export the key and the openapi key (optional)
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