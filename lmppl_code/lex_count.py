import pygments 
from pygments.lexers import get_lexer_by_name


def get_lex_count(texts,lang,show_lex=True):
	lexer = get_lexer_by_name(lang)
	if show_lex:
		print(f'the count is made with: {lexer}')
	pygments_len=sum(len(list(pygments.lex(t, lexer))) for t in texts)
	lex_vocab = sum(len(v) for v in lexer.tokens.values())
	return pygments_len*lex_vocab