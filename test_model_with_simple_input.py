import lmppl_code as lmppl

"""
print("### MLM ###")
scorer = lmppl.MaskedLM('microsoft/deberta-v3-small')
text = [
    'sentiment classification: I dropped my laptop on my knee, and someone stole my coffee. I am happy.',
    'sentiment classification: I dropped my laptop on my knee, and someone stole my coffee. I am sad.'
]
ppl = scorer.get_perplexity(text)
print(list(zip(text, ppl)))
print(f"prediction: {text[ppl.index(min(ppl))]}")

"""


print("### LM ###")
scorer = lmppl.LM('gpt2')
text = [
    'sentiment classification: I dropped my laptop on my knee, and someone stole my coffee. I am happy.',
    'sentiment classification: I dropped my laptop on my knee, and someone stole my coffee. I am sad.'
]
count = lmppl.get_lex_count(text,'c') 

ppl = scorer.get_perplexity(text,count)
print(ppl)
#print(f"prediction: {text[ppl.index(min(ppl))]}")


print("### Encoder-Decoder LM ###")
scorer = lmppl.EncoderDecoderLM('google/flan-t5-small')
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


