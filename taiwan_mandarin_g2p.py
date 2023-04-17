import regex
import sys
from unicodedata import category

from g2pw import G2PWConverter
from pyzhuyin import zhuyin_to_pinyin


class TaiwanMandarinG2P:
   def __init__(self):
      self.__g2p = G2PWConverter()

   def g2p_zhuyin(self, sentences):
      """
      :param list[str] sentences: raw sentences to convert to bopomofo

      :return: zhuyin transcriptions
      """
      r = regex.compile(r"(\p{P})+")
      PUNC = [chr(i) for i in range(sys.maxunicode) if category(chr(i)).startswith("P")]

      sentences_zhuyin = []
      for sentence in sentences:
         sentence = ''.join(sentence.split())
         split_sentence = r.split(sentence) # splits punctuation into their own string
         zhuyin = []
         for s in split_sentence:
            if s in PUNC:
               zhuyin.append(s)
            elif len(s) > 0:
               zhuyin.extend(self.__g2p(s)[0])
         sentences_zhuyin.append(zhuyin)

      return sentences_zhuyin

   def g2p_pinyin(self, sentences):
      """
      :param list[str] sentences: raw sentences to convert to pinyin

      :return: (zhuyin transcriptions, pinyin transcriptions)
      """
      PUNC = [chr(i) for i in range(sys.maxunicode) if category(chr(i)).startswith("P")]

      sentences_zhuyin = self.g2p_zhuyin(sentences)

      sentences_pinyin = []
      for sentence in sentences_zhuyin:
         pinyin = []
         for word in sentence:
            if word in PUNC:
               pinyin.append(word)
            else:
               pinyin.append(zhuyin_to_pinyin(word[:-1])[:-1] + word[-1])
         sentences_pinyin.append(pinyin)

      return sentences_zhuyin, sentences_pinyin
