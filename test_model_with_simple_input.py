import transformers
import lmppl_code as lmppl

print("### LM ###")
# Load a model and tokenizer
tokenizer = transformers.AutoTokenizer.from_pretrained('gpt2')
model = transformers.AutoModelForCausalLM.from_pretrained('gpt2')

# Instantiate the scorer with the pre-loaded model and tokenizer
scorer = lmppl.LM(model='ggggg', tokenizer=tokenizer, model_obj=model)

text = [
    'sentiment classification: I dropped my laptop on my knee, and someone stole my coffee. I am happy.',
    'sentiment classification: I dropped my laptop on my knee, and someone stole my coffee. I am sad.'
]
count = lmppl.get_lex_count(text, 'c') 

ppl = scorer.get_perplexity(text, count)
print(ppl)
#print(f"prediction: {text[ppl.index(min(ppl))]}")



print("### Encoder-Decoder LM ###")

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
ppl = scorer.get_perplexity(input_texts=inputs, output_texts=outputs,lex_count=count)
print(ppl)


