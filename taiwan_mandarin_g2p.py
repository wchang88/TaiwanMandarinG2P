import regex

from g2pw import G2PWConverter
from pyzhuyin import zhuyin_to_pinyin


class TaiwanMandarinG2P:
   def __init__(self, allow_simplified=False):
      self.__g2p = G2PWConverter(enable_non_tradional_chinese=allow_simplified)

   def g2p_zhuyin(self, sentences):
      """
      :param list[str] sentences: raw sentences to convert to bopomofo

      :return: zhuyin transcriptions
      """
      r = regex.compile(r"([\u4e00-\u9fff]+)")

      sentences_zhuyin = []
      for sentence in sentences:
         sentence = ''.join(sentence.split())
         split_sentence = r.split(sentence) # splits punctuation into their own string
         zhuyin = []
         for s in split_sentence:
            if len(s) > 0:
               if r.search(s):
                  zhuyin.extend(self.__g2p(s)[0])
               else:
                  zhuyin.append(s)
         sentences_zhuyin.append(zhuyin)

      return sentences_zhuyin

   def g2p_pinyin(self, sentences, u_to_v=False):
      """
      :param list[str] sentences: raw sentences to convert to pinyin

      :return: (zhuyin transcriptions, pinyin transcriptions)
      """
      r = regex.compile(r"([\u3100-\u312f]+)")
      change_u_to_v = str.maketrans("u", "v")

      sentences_zhuyin = self.g2p_zhuyin(sentences)

      sentences_pinyin = []
      for sentence in sentences_zhuyin:
         pinyin = []
         for word in sentence:
            if r.search(word):
               p = zhuyin_to_pinyin(word[:-1], u_to_v=u_to_v)[:-1]
               if u_to_v and "ㄩ" in word:
                   p = p.translate(change_u_to_v)
               pinyin.append(p + word[-1])
            else:
               pinyin.append(word)
         sentences_pinyin.append(pinyin)

      return sentences_zhuyin, sentences_pinyin
