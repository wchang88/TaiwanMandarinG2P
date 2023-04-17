from pypinyin import Style, pinyin
from pypinyin.style._utils import get_finals, get_initials

def to_pypinyin_phones(sentences_pinyin):
   """
   :param list[str] sentences_pinyin: pinyin transcriptions to convert into ESPNet 
      pypinyin_g2p_phone() form

   :return: pinyin transcriptions separated by phones
   """
   sentences_phones = []
   for sentence in sentences_pinyin:
      phones = [
         p 
         for pinyin in sentence
         for p in [
            get_initials([pinyin][0], strict=True),
            get_finals([pinyin][0][:-1], strict=True) + [pinyin][0][-1]
            if [pinyin][0][-1].isdigit()
            else get_finals([pinyin][0], strict=True)
            if [pinyin][0][-1].isalnum()
            else [pinyin][0],
         ]
         if len(p) != 0 and not p.isdigit()
      ]
      sentences_phones.append(phones)
   return sentences_phones
