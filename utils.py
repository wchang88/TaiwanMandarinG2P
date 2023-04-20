from pypinyin import Style, pinyin
from pypinyin.style._utils import get_finals, get_initials

from taiwan_mandarin_g2p import TaiwanMandarinG2P

def to_pypinyin_phones(sentences_pinyin, strict=False):
   """
   :param list[str] sentences_pinyin: pinyin transcriptions to convert into 
      initial and final phonemes
   :param bool strict: from pypinyin documentation, 
      是否严格遵照《汉语拼音方案》来处理声母和韵母 

   :return: pinyin transcriptions separated by phones
   """
   sentences_phones = []
   for sentence in sentences_pinyin:
      phones = [
         p 
         for pinyin in sentence
         for p in [
            get_initials([pinyin][0], strict=strict),
            get_finals([pinyin][0][:-1], strict=strict) + [pinyin][0][-1]
            if [pinyin][0][-1].isdigit()
            else get_finals([pinyin][0], strict=strict)
            if [pinyin][0][-1].isalnum()
            else [pinyin][0],
         ]
         if len(p) != 0 and not p.isdigit()
      ]
      sentences_phones.append(phones)
   return sentences_phones

def to_espnet_pypinyin_g2p_phone(sentences_pinyin):
   """
   :param list[str] sentences_pinyin: pinyin transcriptions to convert into ESPNet 
      pypinyin_g2p_phone() form

   :return: pinyin transcriptions separated by phones
   """
   return to_pypinyin_phones(sentences_pinyin, strict=True)

def to_zhuyin_from_file(infile, outfile):
   """
   :param str infile: path to file of raw input sentences
   :param str outfile: path to the output file, in tab-separated format
   """
   TWM_g2p = TaiwanMandarinG2P()

   with open(infile, 'r', encoding='utf-8') as f:
      sentences = f.readlines()

      sentences_zhuyin = TWM_g2p.g2p_zhuyin(sentences)

      with open(outfile, 'w', encoding="utf-8") as o:
         for i in range(len(sentences)):
            o.write("{}\t{}\n".format(sentences[i], " ".join(sentences_zhuyin[i])))

def to_pinyin_from_file(infile, outfile):
   """
   :param str infile: path to file of raw input sentences
   :param str outfile: path to the output file, in tab-separated format
   """
   TWM_g2p = TaiwanMandarinG2P()

   with open(infile, 'r', encoding='utf-8') as f:
      sentences = f.readlines()

      _, sentences_pinyin = TWM_g2p.g2p_pinyin(sentences)

      with open(outfile, 'w', encoding="utf-8") as o:
         for i in range(len(sentences)):
            o.write("{}\t{}\n".format(sentences[i], " ".join(sentences_pinyin[i])))

def to_zhuyin_pinyin_from_file(infile, outfile):
   """
   :param str infile: path to file of raw input sentences
   :param str outfile: path to the output file, in tab-separated format
   """
   TWM_g2p = TaiwanMandarinG2P()

   with open(infile, 'r', encoding='utf-8') as f:
      sentences = f.readlines()

      sentences_zhuyin, sentences_pinyin = TWM_g2p.g2p_pinyin(sentences)

      with open(outfile, 'w', encoding="utf-8") as o:
         for i in range(len(sentences)):
            o.write("{}\t{}\t{}\n".format(
               sentences[i], 
               " ".join(sentences_zhuyin[i]),
               " ".join(sentences_pinyin[i])
            ))

def to_pypinyin_phones_from_file(infile, outfile):
   """
   :param str infile: path to file of raw input sentences
   :param str outfile: path to the output file, in tab-separated format
   """
   TWM_g2p = TaiwanMandarinG2P()

   with open(infile, 'r', encoding='utf-8') as f:
      sentences = f.readlines()

      _, sentences_pinyin = TWM_g2p.g2p_pinyin(sentences)
      sentences_phones = to_pypinyin_phones(sentences_pinyin)

      with open(outfile, 'w', encoding="utf-8") as o:
         for i in range(len(sentences)):
            o.write("{}\t{}\t{}\n".format(
               sentences[i], 
               " ".join(sentences_pinyin[i]),
               " ".join(sentences_phones[i])
            ))
