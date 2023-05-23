import torch
from torch.utils.data import Dataset
from torch.utils.data.dataloader import DataLoader
from mingpt.model import GPT
from mingpt.trainer import Trainer
from mingpt.utils import set_seed, setup_logging, CfgNode as CN
import sys
import numpy as np
import pandas as pd
import os
import fire

def get_config(fp, lr):
    print("file path: ",fp)
    print("learning rate: ",lr)

    C = CN()

    # system
    C.system = CN()
    C.system.seed = 3407
    C.system.work_dir = 'out/SongData'

    # data
    C.data = SongDataset.get_default_config()

    # model
    C.model = GPT.get_default_config()
    C.model.model_type = 'gpt-mini'

    # trainer
    C.trainer = Trainer.get_default_config()
    C.trainer.learning_rate = lr # the model we're using is so small that we can go a bit faster

    return (C, fp)

class SongDataset(Dataset):
    @staticmethod
    def get_default_config():
        C = CN()
        C.block_size = 128
        return C

    def __init__(self, config, data):
        self.config = config

        self.chars = sorted(list(set(data)))
        data_size, vocab_size = len(data), len(self.chars)
        print('data has %d characters, %d unique.' % (data_size, vocab_size))

        self.stoi = { ch:i for i,ch in enumerate(self.chars) }
        self.itos = { i:ch for i,ch in enumerate(self.chars) }
        self.vocab_size = vocab_size
        self.data = data

    def get_vocab_size(self):
            return self.vocab_size

    def get_block_size(self):
        return self.config.block_size

    def __len__(self):
        return len(self.data) - self.config.block_size

    def __getitem__(self, idx):
        # grab a chunk of (block_size + 1) characters from the data
        chunk = self.data[idx:idx + self.config.block_size + 1]
        # encode every character to an integer
        dix = [self.stoi[s] for s in chunk]
        # return as tensors
        x = torch.tensor(dix[:-1], dtype=torch.long)
        y = torch.tensor(dix[1:], dtype=torch.long)
        return x, y

if __name__ == '__main__':

    # get default config and overrides from the command line, if any
    (config, data_path) = fire.Fire(get_config)
    set_seed(config.system.seed)

    # construct the training dataset
    df = pd.read_csv(data_path)
    text = df['text'].str.cat(sep="\n")    
    train_dataset = SongDataset(config.data, text)

    # update the config with the block as well as model size and log it into the working directory
    config.model.block_size = train_dataset.get_block_size()
    config.model.vocab_size = train_dataset.get_vocab_size()
    config.block_size = train_dataset.get_block_size()
    config.vocab_size = train_dataset.get_vocab_size()
    config.chars = train_dataset.chars
    setup_logging(config)

    # instantiate the model
    model = GPT(config.model)
    model.load_state_dict(torch.load('out/SongData/model.pt', torch.device('cpu')))

    #printing the configurations of the model
    print(config)

    trainer = Trainer(config.trainer, model, train_dataset)

    # iteration callback
    def batch_end_callback(trainer):

        if trainer.iter_num % 10 == 0:
            print(f"iter_dt {trainer.iter_dt * 1000:.2f}ms; iter {trainer.iter_num}: train loss {trainer.loss.item():.5f}")

        if trainer.iter_num % 500 == 0:
            # evaluate both the train and test score
            model.eval()
            # save the latest model
            print("saving model")
            ckpt_path = os.path.join(config.system.work_dir, "model.pt")
            torch.save(model.state_dict(), ckpt_path)
            # revert model to training mode
            model.train()

    trainer.set_callback('on_batch_end', batch_end_callback)

    # run the optimization
    trainer.run()

