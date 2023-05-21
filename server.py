from fastapi import FastAPI
from pydantic import BaseModel
import torch
from transformers import GPT2Tokenizer, GPT2LMHeadModel
from mingpt.model import GPT
from mingpt.utils import set_seed
from mingpt.bpe import BPETokenizer
import pandas as pd
import json

class GenerateRequest(BaseModel):
    text: str
    max_length: int

with open('out/SongData/config.json','r') as f:
    data = json.load(f)

app = FastAPI()
config = GPT.get_default_config()
config.vocab_size = data['vocab_size']
config.block_size = data['block_size']
config.model_type = 'gpt-mini'
model = GPT(config)

model.load_state_dict(torch.load("out/SongData/model.pt",map_location=torch.device('cpu')))
device = 'auto'

df = pd.read_csv('dataset/spotify_millsongdata.csv')
text = df['text'].str.cat(sep="\n")    
chars = sorted(list(set(text)))

@app.post("/generatetext")
def generate_text(request: GenerateRequest):
# def generate_text(text, max_length):

    stoi = { ch:i for i,ch in enumerate(chars) }
    itos = { i:ch for i,ch in enumerate(chars) }

    context = request.text
    if(context == ''): context = ' '
    max_length = request.max_length
    x = torch.tensor([stoi[s] for s in context], dtype=torch.long)[None,...]
    y = model.generate(x, max_length, temperature=1.0, do_sample=True, top_k=10)[0]
    completion = ''.join([itos[int(i)] for i in y])

    return {"generated_text":completion}

        



