Language Model Perplexity Library (lmppl_code)

This library provides easy ways to compute perplexity scores using various transformer-based language models. It supports both standalone language models and encoder-decoder language models.
Installation

Install the required dependencies:

bash

pip install transformers torch

Usage
Standalone Language Models

python

import transformers
import lmppl_code as lmppl

# Load a model and tokenizer
tokenizer = transformers.AutoTokenizer.from_pretrained('gpt2')
model = transformers.AutoModelForCausalLM.from_pretrained('gpt2')

# Instantiate the scorer with the pre-loaded model and tokenizer
scorer = lmppl.LM(model='gpt2', tokenizer=tokenizer, model_obj=model)

text = [
    'sentiment classification: I dropped my laptop on my knee, and someone stole my coffee. I am happy.',
    'sentiment classification: I dropped my laptop on my knee, and someone stole my coffee. I am sad.'
]
# Get the lexical count 
count = lmppl.get_lex_count(text, 'c') 

# Get perplexity
ppl = scorer.get_perplexity(text, count)
print(ppl)

Encoder-Decoder Language Models

python

import transformers
import lmppl_code as lmppl

tokenizer = transformers.AutoTokenizer.from_pretrained('google/flan-t5-small')
model = transformers.AutoModelForSeq2SeqLM.from_pretrained('google/flan-t5-small')

scorer = lmppl.EncoderDecoderLM(tokenizer=tokenizer, model_obj=model)
inputs = [
    'sentiment classification: I dropped my laptop on my knee, and someone stole my coffee.',
    'sentiment classification: I dropped my laptop on my knee, and someone stole my coffee.'
]
outputs = [
    'I am happy.',
    'I am sad.'
]

count = lmppl.get_lex_count(outputs,'c') 

# Get perplexity
ppl = scorer.get_perplexity(input_texts=inputs, output_texts=outputs, lex_count=count)
print(ppl)

Contributing

[Explain how others can contribute to your project]
License

[Your License Here]

Please make sure to replace placeholders (like [Your License Here]) with actual content. Modify the text according to your needs.