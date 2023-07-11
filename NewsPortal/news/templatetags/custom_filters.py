import re

from django import template

from ..models import BadWord


register = template.Library()

CENSOR_METHOD_ALL_EXCEPT_BEGIN_AND_END = 1
CENSOR_METHOD_ALL_EXCEPT_BEGIN = 2

@register.filter()
def censor(value, censor_method=CENSOR_METHOD_ALL_EXCEPT_BEGIN):
    # return value

    bad_words = list(BadWord.objects.all().values("text"))
    bad_words_strs = [curr_bad_word['text'] for curr_bad_word in bad_words]

    def change_word_all_except_begin_and_end(word, bw_index, bw_len):
        res_word = word
        res_word = res_word[:bw_index + 1] + "*" * (bw_len - 2) + \
            res_word[bw_index + bw_len - 1:]

        return res_word

    def change_word_all_except_begin(word, bw_index, bw_len):
        res_word = word[:1] + "*" * (len(word) - 1)

        return res_word

    if censor_method == CENSOR_METHOD_ALL_EXCEPT_BEGIN_AND_END:
        change_word_func = change_word_all_except_begin_and_end
    else:
        change_word_func = change_word_all_except_begin

    def do_censor(word: str) -> str:
        res_word = word
        for curr_bw in bad_words_strs:
            curr_bw_len = len(curr_bw)
            if curr_bw_len > 1:
                curr_bw_index = res_word.lower().find(curr_bw.lower())
                if curr_bw_index > -1:
                    res_word = change_word_func(res_word, curr_bw_index, curr_bw_len)
                    # res_word = res_word[:curr_bw_index + 1] + "*" * (curr_bw_len - 2) + \
                    #            res_word[curr_bw_index + curr_bw_len - 1:]
        return res_word

    if not isinstance(value, str):
        raise ValueError("censor: value should be string argument!")

    # words = value.split()
    words = re.findall(r"[\w']+|[.,!?;…]", value)
    # print(value)
    # print(words)
    res = ""
    # return value

    for curr_word in words:
        new_word = do_censor(curr_word)
        res += new_word + " "

    # res += "====" + "+".join(bad_words) + "===="

    return res

@register.filter()
def add(value1, value2):
    return value1 + value2