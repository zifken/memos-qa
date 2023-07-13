import faiss
import numpy as np
import requests
import sys
import os
from pathlib import Path

BASE_URL = os.getenv('MEMO_URL').split('/memo?')[0]
OPENID = os.getenv('MEMO_URL').split('/memo')[1]

INDEX_FILE = "./memos.index"


OPENAI_API_KEY =  os.getenv('OPENAI_API_KEY')

def generate_embeddings(texts, model='all-mpnet-base-v2',show_progress_bar=True):
    if model == 'text-embedding-ada-002':
        import openai
        openai.api_key = OPENAI_API_KEY
        response = openai.Embed(texts=texts)
        embedding = np.array(response['embeddings'])
        dim = 1536
        return embeddings, dim
    else:
        from sentence_transformers import SentenceTransformer
        model = SentenceTransformer(model)
        dim = model.get_sentence_embedding_dimension()
        embeddings = model.encode(texts, show_progress_bar=show_progress_bar)
        return embeddings, dim

def create_index(d):
    # d => dimension of embeddings
    index = faiss.IndexIDMap(faiss.IndexFlatIP(d))
    return index



def add_embeddings(memoIds, embeddings, index):
    ids = np.array(memoIds)
    index.add_with_ids(embeddings, ids)
    return index

def id_to_txt(_id):
    resp = requests.get(f"{BASE_URL}/memo/{_id}{OPENID}")
    try:
        return resp.json()['content']
    except:
        return resp.json()['data']['content']

def find_similar_texts(input_text, index, model='all-mpnet-base-v2', k=3):
    query_vector = generate_embeddings([input_text], model='all-mpnet-base-v2')[0]
    _, I = index.search(query_vector, k)
    res = [id_to_txt(_id) for _id in I.tolist()[0]]
    return res

def get_all_memos(memo_find=None):
    query_list = []
    if memo_find and memo_find.get("offset"):
        query_list.append(f"offset={memo_find['offset']}")
    if memo_find and memo_find.get("limit"):
        query_list.append(f"limit={memo_find['limit']}")
    query_string = "&".join(query_list)
    url = f"{BASE_URL}/memo{OPENID}&{query_string}" if query_string else f"{BASE_URL}/memo{OPENID}"
    resp = requests.get(url)
    return resp


def ask_gpt(context, question):
    import openai
    openai.api_key = OPENAI_API_KEY
    prompt=f"Given this context and only this context:\n{context}\nAnswer this Question: {question}"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=100, n=1, stop=None, temperature=0.5  
    )
    generated_text = response.choices[0].message.content
    return generated_text


if __name__=='__main__':
    if len(sys.argv) < 1 or (len(sys.argv)==1 and sys.argv[1]=='--ask-gpt'):
        print('usage: to find the most relevent memo and ask chatgpt (3.5-turbo)\
              export OPENAI_API_KEY="sk-1235611234456123456";\
              export MEMO_URL="https://[[DOMAIN_NAME_OR_IP]]/api/memo?openId=12345-12345";\
              python qa.py "how long did the meeting with Julie lasted ?" --ask-gpt')
        print('usage: to find and print the most relevent memo \
              export MEMO_URL="https://[[DOMAIN_NAME_OR_IP]]/api/memo?openId=12345-12345";\
              python qa.py "how long did the meeting with Julie lasted ?"')
        print('IMPORTANT : The embeddings is computed for all the memos in the DB \
              this will create the memos.index file \
              it can take several minutes depending on your hardware and the number of memos \
              so once its done don\'t rename move or delete the memos.index file \
              or change the variable INDEX_FILE to point to the right location')
        sys.exit()
    

    if not  Path(INDEX_FILE).is_file():
        print('starting embedding')

        memos = [(i['id'], i['content']) for i in get_all_memos({'limit':200, 'offset':-1}).json()['data']]
        memos_txt = [m[1] for m in memos]
        memos_ids = [m[0] for m in memos]
        embeddings, dim = generate_embeddings(memos_txt)
        index = add_embeddings(memos_ids, embeddings, create_index(dim))
        faiss.write_index(index, INDEX_FILE)
    else: 
        print('skipping embedding')


    index = faiss.read_index(INDEX_FILE)
    q=sys.argv[1]
    res = find_similar_texts(q, index, model='all-mpnet-base-v2', k=3)
    if '--ask-gpt' in sys.argv:
        i = input(f"!!This memo will be sent to openai!!:\n{res[0]}\n!!Please confirm with [y]!!\n")
        if i == 'y':
            gpt_res = ask_gpt(res[0], q)
            print(gpt_res)
    else:
        for r in res:
            print(r)
