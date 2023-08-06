# -*- coding: UTF-8 -*-
################################################################################
#
#   Copyright (c) 2020  Baidu, Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#################################################################################

"""
该模块实现用户自定义词典的功能
"""

from io import open
import logging

try:
    from ._compat import strdecode
    from .prefix_tree import TriedTree
except:
    from _compat import strdecode
    from prefix_tree import TriedTree


class Customization(object):
    """
    基于AC自动机实现用户干预的功能
    """

    def __init__(self):
        self.dictitem = {}
        self.ac = None
        pass
    
    def add_word(self, words, sep=None):
        """装载人工干预词典（单词输入）"""
        if self.ac is None:
            self.ac = TriedTree()
        words = strdecode(words)
        if sep == None:
            words = words.strip().split()
        else:
            sep = strdecode(sep)
            words = words.strip().split(sep)

        if len(words) == 0:
            return

        phrase = ""
        tags = []
        offset = []
        for word in words:
            if word.rfind('/') < 1:
                phrase += word
                tags.append('')
            else:
                phrase += word[:word.rfind('/')]
                tags.append(word[word.rfind('/') + 1:])
            offset.append(len(phrase))

        if len(phrase) < 2 and tags[0] == '':
            return

        self.dictitem[phrase] = (tags, offset)
        self.ac.add_word(phrase)

    def load_customization(self, filename, sep=None):
        """装载人工干预词典"""
        self.ac = TriedTree()
        with open(filename, 'r', encoding='utf8') as f:
            for line in f:
                if sep == None:
                    words = line.strip().split()
                else:
                    sep = strdecode(sep)
                    words = line.strip().split(sep)

                if len(words) == 0:
                    continue

                phrase = ""
                tags = []
                offset = []
                for word in words:
                    if word.rfind('/') < 1:
                        phrase += word
                        tags.append('')
                    else:
                        phrase += word[:word.rfind('/')]
                        tags.append(word[word.rfind('/') + 1:])
                    offset.append(len(phrase))

                if len(phrase) < 2 and tags[0] == '':
                    continue

                self.dictitem[phrase] = (tags, offset)
                self.ac.add_word(phrase)
        self.ac.make()

    def parse_customization(self, query, lac_tags):
        """使用人工干预词典修正lac模型的输出"""
        if not self.ac:
            logging.warning("customization dict is not load")
            return

        # FMM前向最大匹配
        ac_res = self.ac.search(query)

        for begin, end in ac_res:
            phrase = query[begin:end]
            index = begin

            tags, offsets = self.dictitem[phrase]
            for tag, offset in zip(tags, offsets):
                while index < begin + offset:
                    if len(tag) == 0:
                        lac_tags[index] = lac_tags[index][:-1] + 'I'
                    else:
                        lac_tags[index] = tag + "-I"
                    index += 1

            lac_tags[begin] = lac_tags[begin][:-1] + 'B'
            for offset in offsets:
                index = begin + offset
                if index < len(lac_tags):
                    lac_tags[index] = lac_tags[index][:-1] + 'B'


if __name__ == '__main__':

    custom = Customization()
    custom.load_customization('./icwb2_gold/pku_training_words.utf8')
    query = u"共同创造美好的新世纪——二○○一年新年贺词"
    tags = ['O'] * len(query)
    custom.parse_customization(query, tags)
    print('after parse: ', tags)
