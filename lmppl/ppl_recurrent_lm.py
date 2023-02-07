""" Calculate perplexity.
>>> scorer = LM()
>>> scores = scorer.get_perplexity(
    input_texts=['sentiment classification: I have a bad day is happy',
                 'sentiment classification: I have a bad day is sad'],
)
>>> print(scores)
[128.80070356559577, 100.5730992106926]
"""

import os
import logging
from math import exp
from typing import List

import transformers
import torch

from .util import internet_connection


os.environ["OMP_NUM_THREADS"] = "1"  # to turn off warning message
os.environ["TOKENIZERS_PARALLELISM"] = "false"  # to turn off warning message
PAD_TOKEN_LABEL_ID = torch.nn.CrossEntropyLoss().ignore_index


class LM:
    """ Language Model. """

    def __init__(self,
                 model: str = 'distilgpt2',
                 use_auth_token: bool = False,
                 max_length: int = None,
                 device: str = None,
                 num_gpus: int = None):
        """ Language Model.

        @param model: Model alias or path to local model file.
        @param use_auth_token: Huggingface transformers argument of `use_auth_token`
        @param device: Device name to load the models.
        @param num_gpus: Number of gpus to be used.
        """
        logging.info(f'Loading Model: `{model}`')

        # load model
        local_files_only = not internet_connection()
        self.tokenizer = transformers.AutoTokenizer.from_pretrained(
            model, local_files_only=local_files_only, use_auth_token=use_auth_token)
        self.config = transformers.AutoConfig.from_pretrained(
            model, local_files_only=local_files_only, use_auth_token=use_auth_token)
        self.model = transformers.AutoModelForCausalLM.from_pretrained(
            model, config=self.config, local_files_only=local_files_only, use_auth_token=use_auth_token)
        self.max_length = max_length if max_length is not None else self.tokenizer.model_max_length
        self.tokenizer.pad_token = self.tokenizer.eos_token
        assert self.max_length <= self.tokenizer.model_max_length, f"{self.max_length} > {self.tokenizer.model_max_length}"

        # loss function
        self.loss_fct = torch.nn.CrossEntropyLoss(reduction='none')

        # GPU setup
        if device is None:
            self.device = 'cuda' if torch.cuda.device_count() > 0 else 'cpu'
        else:
            self.device = device
        num_gpus = torch.cuda.device_count() if num_gpus is None else num_gpus
        if num_gpus > 1:
            self.parallel = True
            self.model = torch.nn.DataParallel(self.model)
        self.model.to(self.device)
        self.model.eval()
        logging.info(f'\t * Num of GPU in use: {torch.cuda.device_count()}')

    def get_perplexity(self, input_texts: str or List, batch: int = None):
        """ (pseudo) Perplexity """

        # batch preparation
        single_input = type(input_texts) == str
        input_texts = [input_texts] if single_input else input_texts
        batch = len(input_texts) if batch is None else batch
        batch_id = list(range(0, len(input_texts), batch)) + [len(input_texts)]
        batch_id = list(zip(batch_id[:-1], batch_id[1:]))

        loss_list = []
        with torch.no_grad():
            for s, e in batch_id:

                # run model inference
                model_inputs = self.tokenizer(
                    input_texts[s:e], max_length=self.max_length, truncation=True, padding='max_length',
                    return_tensors='pt')
                output = self.model(**{k: v.to(self.device) for k, v in model_inputs.items()})

                # compute loss
                label = model_inputs['input_ids']
                label[label == self.tokenizer.eos_token_id] = PAD_TOKEN_LABEL_ID
                loss = self.loss_fct(output['logits'].view(-1, self.config.vocab_size), label.view(-1))
                loss = loss.view(len(output['logits']), -1)
                loss_list += torch.mean(loss, -1).cpu().tolist()

        # conversion to perplexity
        ppl = [exp(i) for i in loss_list]

        if single_input:
            return ppl[0]
        return ppl

