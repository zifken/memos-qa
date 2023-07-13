import os
from pathlib import Path
import click
import faiss
import numpy as np
import requests
from sentence_transformers import SentenceTransformer
from transformers import pipeline
import openai



class Embedding(object):
    def __init__(self, model_name):
        self.model = SentenceTransformer(model_name)
        self.dim = self.model.get_sentence_embedding_dimension()
    def embed(self, memos):
        # TODO: create a preprocess function to truncate the text if > model.max_length 
        # text = self.preprocess(texts) 
        return self.model.encode([m.content for m in memos], show_progress_bar=(len(memos)!=1))

class Qa(object):
    def __init__(self, model_name):
        self.nlp = pipeline('question-answering', model=model_name, tokenizer=model_name)

    def get(self, query):
        res = self.nlp({
            'question': query.question,
            'context': query.context.content
        })
        return res['answer']

class Openaiqa(object):
    def __init__(self, api_key):
        openai.api_key = api_key

    def get(self, query):
        prompt=f"Given this context and only this context:\n{query.context.content}\nAnswer this Question: {query.question}"
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


class Query(object):
    def __init__(self, question, context=None) -> None:
        self.question = question
        self.context = context
        self.answer=None
    def get_context(self, e, E, db):
        self.embedding = E.embed([Memo(-1,self.question)])
        self.context = db.by_id(e.search(self.embedding)[0])
    def get_answer(self, qa):
        self.answer = qa.get(self)


class Memo(object):
    def __init__(self, id_, content) -> None:
        self.id = id_
        self.content = content
        self.embedding = None

    def set_embedding(self, embedding):
        self.embedding = embedding


class Engine(object):
    def __init__(self, index_path, d=None) -> None:
        self.path = index_path
        if Path(index_path).is_file():
            self.index = faiss.read_index(self.path)
            self.ids = [self.index.id_map.at(i) for i in range(self.index.ntotal)]
            self.d = self.index.d
        elif d:
            self.index = faiss.IndexIDMap(faiss.IndexFlatIP(d))
            self.d = self.index.d
            self.ids = []
        else:
            raise Exception('Either an existing index path or a path and the embedding dim must be provided')

    def clean(self, ids_):
        to_del = [i for i in self.ids if i not in ids_]
        if len(to_del) > 0:
            self.index.remove_ids(np.array(to_del))
    
    def save(self):
        faiss.write_index(self.index, self.path)
    
    def isin(self, id_):
        return id_ in self.ids

    def add_embeddings(self, memos):
        embeddings = np.array([m.embedding for m in memos])
        ids = np.array([m.id for m in memos])
        self.index.add_with_ids(embeddings, ids)
        self.ids = [self.index.id_map.at(i) for i in range(self.index.ntotal)]


    def search(self,query_vector, k=1):
        _, I = self.index.search(query_vector, k)
        res = [_id for _id in I.tolist()[0]]
        return res

class DB():
    def __init__(self, url, key) -> None:
        self.url = url
        self.key = key
    
    def get_all(self, offset=None, limit=None):
        query_list = []
        if offset:
            query_list.append(f"offset={offset}")
        if limit:
            query_list.append(f"limit={limit}")
        query_string = "&".join(query_list)
        url = f"{self.url}/memo{self.key}&{query_string}" if query_string else f"{self.url}/memo{self.key}"
        resp = requests.get(url).json()['data']
        memos= [Memo(d['id'], d['content']) for d in resp]
        return memos

    def by_id(self, _id):
        resp = requests.get(f"{self.url}/memo/{_id}{self.key}").json()['data']
        memo = Memo(resp['id'], resp['content'])
        return memo

# usefull to push edits on memos w/ id already in faiss index MAYBE ?
# the overall semantic shouldn't change completly and the latest version of the 
# memo is still being passed as context so FIXME but later
def embed_add(memo, memo_url, index_file):
    BASE_URL = memo_url.split('/memo?')[0]
    OPENID = memo_url.split('/memo')[1]

    E = Embedding('all-mpnet-base-v2')
    qa = Qa('deepset/roberta-base-squad2')
    db = DB(BASE_URL, OPENID)
    e = Engine(index_file, E.model.get_sentence_embedding_dimension())

    e.add_embeddings(memo.set_embedding(E.embed([memo])))


@click.command()
@click.option("--memo-url", type=str, required=True, help="url with OpenID key to the Memos instance")
@click.option("--openai-key", type=str, default='', help="OpenAI API Key (optional)")
@click.option("--openai", type=bool, default="false", help="whether to use OpenAI API")
@click.option("--index-file", type=str, default="memos.index", help="index filename")
@click.argument("question", required=True)
def main(question, memo_url, index_file, openai_key, openai):
    BASE_URL = memo_url.split('/memo?')[0]
    OPENID = memo_url.split('/memo')[1]

    E = Embedding('all-mpnet-base-v2')
    qa = Qa('deepset/roberta-base-squad2')
    db = DB(BASE_URL, OPENID)
    
    e = Engine(index_file, E.model.get_sentence_embedding_dimension())

    # infinite loop so one can keep asking question and not have to reload 
    # models and fetch api
    while True:

        memos = [memo for memo in db.get_all() if not e.isin(memo.id)]
        if memos:
            print(f"Computing embedding for {len(memos)} memos")
            for i, E_ in  enumerate(E.embed(memos)):
                memos[i].set_embedding(E_)

            e.add_embeddings(memos)
            e.save()

        q = Query(question)
        q.get_context(e, E, db)
        q.get_answer(qa)
        if openai:
            print("using openai")
            q.get_answer(Openaiqa(api_key=openai_key))
            pass
        print(q.answer)
        # TODO: print more of context if answer too short or the score is too low
        question = input('Type your next question and press [enter]:\n')

if __name__=='__main__':
    main()