#!/usr/bin/env python3
# coding=utf-8
# Producer=LPP
import collections
import os
import re
import shutil
from codecs import open
from collections import defaultdict

import numpy


def get_wanted(data, wanted):
    assert isinstance(data, (dict, Ddict, list, tuple))
    end = []
    for i in wanted:
        assert isinstance(i, int)
        end.append(data[i])
    return end


class SmithWaterman:
    """docstring for SmithWaterman
    seq1 需要比对的第一个序列
    seq2 需要比对的第二个序列
    使用align方法进行比对
    而后score属性是每一个比对的打分

    """
    max_j: int

    def __init__(self, seq1, seq2):
        self.identity = 0
        self.max_i, self.max_j = 0, 0
        self.seq1 = re.sub(r"\s+", '', seq1)
        self.seq2 = re.sub(r"\s+", '', seq2)
        self.subs_matrix = [[5, -4, -4, -4, -4], [-4, 5, -4, -4, -4], [-4, -4, 5, -4, -4], [-4, -4, -4, 5, -4],
                            [-4, -4, -4, -4, -4]]
        self.m = len(self.seq1)
        self.n = len(self.seq2)
        self.gap_penalty = -4
        self.max_score = 0
        # the DP table
        self.score = numpy.zeros((self.m + 1, self.n + 1))
        # to store the traceback path
        self.pointer = numpy.zeros((self.m + 1, self.n + 1))
        self.align1, self.align2 = '', ''
        self.create_dp_and_pointers()

    def create_match_score(self, alpha, beta):
        """get match/dismatch score from subs_matrix"""
        alphabet = {"A": 0, "C": 1, "G": 2, "T": 3, "N": 4}
        lut_x = alphabet[alpha]
        lut_y = alphabet[beta]
        return self.subs_matrix[lut_x][lut_y]

    def create_dp_and_pointers(self):
        # calculate DP table and mark pointers
        for i in range(1, self.m + 1):

            for j in range(1, self.n + 1):
                score_up = self.score[i - 1][j] + self.gap_penalty
                score_down = self.score[i][j - 1] + self.gap_penalty
                score_diagonal = self.score[i - 1][j - 1] + self.create_match_score(self.seq1[i - 1], self.seq2[j - 1])
                self.score[i][j] = max(0, score_up, score_down, score_diagonal)
                if self.score[i][j] == 0:
                    # 0 means end of the path
                    self.pointer[i][j] = 0
                if self.score[i][j] == score_up:
                    # 1 means trace up
                    self.pointer[i][j] = 1
                if self.score[i][j] == score_down:
                    # 2 means trace left
                    self.pointer[i][j] = 2
                if self.score[i][j] == score_diagonal:
                    # 3 means trace diagonal
                    self.pointer[i][j] = 3
                if self.score[i][j] >= self.max_score:
                    self.max_i, self.max_j = i, j
                    self.max_score = self.score[i][j]

    def trace_back(self):
        while self.pointer[self.max_i][self.max_j] != 0:
            if self.pointer[self.max_i][self.max_j] == 3:
                self.align1 = self.align1 + self.seq1[self.max_i - 1]
                self.align2 = self.align2 + self.seq2[self.max_j - 1]
                self.max_i -= 1
                self.max_j -= 1
            elif self.pointer[self.max_i][self.max_j] == 2:
                self.align1 = self.align1 + '-'
                self.align2 = self.align2 + self.seq2[self.max_j - 1]
                self.max_j -= 1
            elif self.pointer[self.max_i][self.max_j] == 1:
                self.align1 = self.align1 + self.seq1[self.max_i - 1]
                self.align2 = self.align2 + '-'
                self.max_i -= 1

    @property
    def align(self):
        self.trace_back()

        align1, align2 = self.align1[::-1], self.align2[::-1]

        symbol = ''
        self.score = 0
        identity, similarity = 0, 0
        for i in range(0, len(align1)):
            # if two AAs are the same, then output the letter
            if align1[i] == align2[i]:
                symbol = symbol + align1[i]
                identity += 1
                similarity += 1
                self.score += self.create_match_score(align1[i], align2[i])
            # if there are mismatches
            elif align1[i] != align2[i] and '-' not in [align1[i], align2[i]]:
                self.score += self.create_match_score(align1[i], align2[i])
                # add mismatching base character
                symbol = symbol + '*'

            # if one of them is a gap, output a space
            elif '-' in [align1[i], align2[i]]:
                symbol += '-'
                self.score += self.gap_penalty
        if align1 == 0 or len(align1) == 0:
            self.identity = 0
        else:
            self.identity = float(identity) / len(align1) * 100
        if align2 == 0 or len(align2) == 0:
            self.similarity = 0
        else:
            self.similarity = float(similarity) / len(align2) * 100
        self.align1 = align1
        self.align2 = align2
        self.symbol = symbol
        # print 'Identity =', "%3.3f" % self.identity, 'percent';
        # print 'Similarity =', "%3.3f" % self.similarity, 'percent';
        # print 'Score =', self.score;
        # print align1
        # print symbol
        # print align2
        return self.score


def overwrite_path(path):
    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path)


def check_path(path):
    path = os.path.abspath(path)
    if not os.path.exists(path):
        os.makedirs(path)
    return path + '/'


def complement(char):
    char = re.sub('\s+', '', char)

    libary = str.maketrans('atcgATCG', 'tagcTAGC')
    end = char[::-1].translate(libary)
    return end


class fastq_check(object):
    class NotFastqError(ValueError):
        pass

    def __init__(self, file_handle):

        assert isinstance(getattr(file_handle, "read"),
                          collections.Callable), 'The paramater input must be a File Handle'
        self.linenumber = 0
        self.filename = file_handle.name
        self.file_handle = iter(file_handle)
        for line in self.file_handle:
            self.linenumber += 1
            if line[0] == '@':
                self.define = line

                break

    def __iter__(self):
        return self

    def __next__(self):
        if not self.define:
            self.define = next(self.file_handle)
            self.linenumber += 1
        name = self.define
        seq = next(self.file_handle)
        self.linenumber += 1
        define2 = next(self.file_handle)
        self.linenumber += 1
        quality = next(self.file_handle)
        self.linenumber += 1
        self.define = ''
        return (name, seq, define2, quality)


class Ddict(defaultdict, dict):
    def __init__(self):
        defaultdict.__init__(self, Ddict)

    def __repr__(self):
        return dict.__repr__(self)


class File_dict(object):
    """file_ddict(file_TAG,options)   options=1,from 2 lines to start,
    oprions=0 from the first to start
    """

    def __init__(self, FILE_HANDLE, OPTIONS=0):
        self.__FILE = FILE_HANDLE
        self.__OPTIONS = OPTIONS
        self.__HASH = {}
        for i in range(0, self.__OPTIONS):
            next(self.__FILE)

    def read(self, NUMBER_1, NUMBER_2):
        assert isinstance(NUMBER_1, int);
        assert isinstance(NUMBER_2, int)
        for _line in self.__FILE:
            line_list = _line[:-1].split('\t')
            _1_list = line_list[NUMBER_1 - 1].split(';')
            for element in _1_list:
                self.__HASH[element.strip()] = line_list[NUMBER_2 - 1].strip()
        self.__FILE.seek(0, 0)
        return self.__HASH


class File_Ddict(object):

    @staticmethod
    def check(cache_hash):
        cache_exec = {'': ''}

        def creep(i):
            cache_new = {}
            for j in cache_hash[i]:
                for each_key in cache_exec:
                    cache_new[each_key + '[ key_%s_%s ]' % (i, j)] = ''
            return cache_new

        for i in sorted(cache_hash):
            cache_exec = creep(i)
        return cache_exec

    def __init__(self, _file, options=0, separate=';'):
        assert isinstance(options, int)
        self.file = iter(_file)
        self.separate = separate
        for i in range(0, options):
            next(self.file)
        self.hash = Ddict()

    '''number_1 the first value's number '''

    def read(self, *number_list):
        number_list = [key1 - 1 for key1 in number_list]
        for key1 in number_list:
            assert isinstance(key1, int)
        for line in self.file:
            line_l = line.replace('\n', '').split('\t')
            cache_hash = Ddict()
            i = 0
            for each_number in number_list:
                j = 0
                if not self.separate:
                    line_l_cache = line_l[each_number]
                else:
                    line_l_cache = line_l[each_number].split(self.separate)
                for each_key in line_l_cache:
                    exec('key_%s_%s = each_key' % (i, j))
                    cache_hash[i][j] = ''
                    j = j + 1
                i = i + 1
            for key1 in self.check(cache_hash):
                exec('self.hash%s=\'\'' % (key1))

        return self.hash


class block_reading(object):
    def __init__(self, file_handle, tag):
        self.file = iter(file_handle)
        self.tag = tag

    def __iter__(self):
        return self

    def __next__(self):
        self.container = []
        for line in self.file:
            if re.match(self.tag, line):
                break
            else:
                self.container.append(line)
        self.container = ''.join(self.container)
        if not self.container:
            raise StopIteration
        return self.container


class fasta_check(object):
    def __init__(self, file_handle):
        assert isinstance(getattr(file_handle, "read"),
                          collections.Callable), 'The paramater input must be a File Handle'
        self.file = iter(file_handle)
        for line in self.file:
            if line[0] == '>':
                self.define = line
                break

    def __iter__(self):
        return self

    def __next__(self):
        if not self.define:
            raise StopIteration

        name = self.define
        self.define = ''
        s = []
        for line in self.file:
            if line[0] != '>':
                s.append(line)
            else:
                self.define = line
                break
        s = ''.join(s)
        return name, s


class blast_parse(object):
    def __init__(self, blast_file, output_file):
        self.input = iter(block_reading(blast_file, r'\s*<Iteration>'))
        self.output = output_file

    def parse(self):
        self.tag = 0
        for key1 in self.input:
            if '<Hit>' not in key1:
                continue
            accession = '\t'.join(re.findall(r'<Iteration_\S+?>([^<\n]+)', key1, re.M))
            for key2 in re.split(r'</?Hit>', key1):
                if '<Hit_num>' in key2:
                    modules = re.split(r'</?Hsp>', key2)
                    title = re.findall(r'<([^>]+)>([^<\n]+)', modules[0], re.MULTILINE)
                    head = accession + '\t' + '\t'.join([keym[1] for keym in title])
                    if self.tag == 0:
                        title_out = ['Iteration_iter-num', 'Iteration_query-ID', 'Iteration_query-def',
                                     'Iteration_query-len']
                        title_out.extend([keym[0].replace("\n", "") for keym in title])
                    for key4 in modules[1:]:
                        if '<Hsp_num>' not in key4:
                            continue
                        data_all = re.findall('<([^>]+)>([^<\n]+)', key4, re.MULTILINE)
                        if self.tag == 0:
                            title_out.extend([keym[0].replace(r"\n", "") for keym in data_all if keym[0] != 'Hsp_gaps'])
                            self.output.write('\t'.join(title_out).replace("\n", "") + '\n')
                        self.output.write(
                            head + '\t' + '\t'.join([key3[1] for key3 in data_all if key3[0] != 'Hsp_gaps']) + '\n')
                        self.tag = 1


class EMBL_nul_seq(object):
    @classmethod
    def complement(cls, char):
        libary = str.maketrans('atcgATCG', 'tagcTAGC')
        return char[::-1].translate(libary)

    def getx(self, raw_list):
        [input_data, protein_id] = raw_list
        data_list = input_data.split(',')
        seq_slice = ''
        for data in data_list:
            all_loc = re.search(r'(\d+)\.\.(\d+)', data)
            start = int(all_loc.group(1)) - 1
            end = int(all_loc.group(2))
            cache_slice = self.seq[start:end]
            if data.startswith('complement('):
                cache_slice = self.complement(cache_slice)
            seq_slice += cache_slice
        seq_slice = re.sub(r'(\w{60})(?!\Z)', '\\1\n', seq_slice)
        return '>' + protein_id + '\n' + seq_slice + '\n'

    def retrieve_seq(self, data_list):
        data = list(map(self.getx, data_list))
        return ''.join(list(data))

    def __init__(self, s_file):
        self.file = block_reading(s_file, tag='//')

    def __iter__(self):
        return self

    @property
    def __next__(self):
        block = next(self.file)
        if not block:
            raise StopIteration
        seq = re.search(r'\nSQ {3}[^\n]+\n([^/]+)', block).group(1)
        self.seq = re.sub('\W+|\d+', '', seq)
        cds_all = re.findall(r'\nFT {3}CD {13} ([^/]+).+?\nFT\s+/protein_id="(\S+)"', block)
        fasta_end = self.retrieve_seq(cds_all)
        return fasta_end


class uniprot_parse(object):
    @classmethod
    def seq_manup(cls, seq):
        seq = re.sub(r'\W+', '', seq)
        seq = re.sub(r'(\w{60})', r'\1\n', seq)
        return seq

    def __init__(self, files, tag):
        self.file = iter(block_reading(open(files, 'rU'), tag='//'))
        self.tag = tag

    def __iter__(self):
        return self

    @property
    def __next__(self):
        block = next(self.file)
        if not block:
            raise StopIteration

        oc = re.search(r"\nOC {3}([^\n]+)", block).group(1)
        if self.tag not in oc:
            next(self)
        else:
            uni_id = re.search(r'ID {3}(\S+)', block).group(1)
            uni_ac = re.search(r'\nAC {3}([^\n]+)', block).group(1)
            uni_ac_list = uni_ac.split(';')
            uni_ac = ' ;'.join([key1.strip() for key1 in uni_ac_list if key1.strip()])
            taxon = re.search(r'NCBI_TaxID=(\d+)', block).group(1)
            seq = re.search(r'\nSQ {3}SEQUENCE [^\n]+\n([^/]+)', block).group(1)
            seq = self.seq_manup(seq) + '\n'
            self.id = uni_id
            self.ac = uni_ac
            self.taxon = taxon
            self.seq = seq
        return self


class GBK_nul_seq(object):
    @classmethod
    def complement(cls, char):
        libary = str.maketrans('atcgATCG', 'tagcTAGC')
        return char[::-1].translate(libary)

    def getx(self, raw_list):
        input_data, protein_id, product = raw_list
        product = re.sub(r'\s+', '  ', product)
        data_list = input_data.split(',')
        seq_slice = ''
        for data in data_list:
            all_loc = re.search(r'(\d+)\.\.(\d+)', data)
            start = int(all_loc.group(1)) - 1
            end = int(all_loc.group(2))
            cache_slice = self.seq[start:end]
            if data.startswith('complement('):
                cache_slice = self.complement(cache_slice)
            seq_slice += cache_slice
        seq_slice = re.sub(r'(\w{60})(?!\Z)', '\\1\n', seq_slice.upper())
        return '>' + protein_id + '|' + product + '\n' + seq_slice + '\n'

    def retrieve_seq(self, data_list):
        data = list(map(self.getx, data_list))
        return ''.join(list(data))

    def __init__(self, s_file):
        self.file = block_reading(s_file, tag='//')

    def __iter__(self):
        return self

    @property
    def __next__(self):
        block = next(self.file)
        if not block:
            raise StopIteration
        seq = re.search(r"\nORIGIN\s+\n([^/]+)", block).group(1)
        self.seq = re.sub('\W+|\d+', '', seq)

        all_protein = re.findall(r'''/product="([^"]+)"\s+/protein_id="(\S+)"\s+/translation="([^"]+)"''', block,
                                 re.MULTILINE)
        all_Data = re.findall(r'\s+(?:CDS|rRNA|tRNA).+?(\S+).+?/locus_tag="([^"]+)".+?/product="([^"]+)"', block,
                              re.DOTALL)
        fasta_end = self.retrieve_seq(all_Data)
        all_protein_seq = ''
        for a, b, c in all_protein:
            c = re.sub(r'\s+', '', c)
            c = re.sub(r'(\w{60})', '\\1\n', c)
            a = re.sub(r'\s+', '  ', a)
            all_protein_seq += '>' + b + '|' + a + '\n' + c + '\n'

        return fasta_end, all_protein_seq


all_spieces = {}


def get_taxon_seed(taxon_number):
    all_end = {}

    def creeper(taxon_number:str):
        if taxon_number in all_spieces:
            all_end[taxon_number] = ''
            for key1 in all_spieces[taxon_number]:
                creeper(key1)

    creeper(taxon_number)
    return all_end


def K_Mer(string, length=4):
    '数k-mer的工具，输入序列和k－mer长度，返回k-mer数据集和去冗余之后的数据集'
    assert length <= len(string)
    all_kmer = []
    k_mer_hash = {}
    i = 0
    while i + length <= len(string):
        k_mer = string[i:  length + i]
        all_kmer.append(k_mer)
        k_mer_hash[k_mer] = ''
        i += 1
    return all_kmer, k_mer_hash


def Redis_trans(data_hash):
    out_data: str = ""
    if isinstance(data_hash,Ddict):

        for key1 in data_hash:

            for key2, value in list(data_hash[key1].items()):
                out_data += r"""*4\r\n$4\r\nhset\r\n"""
                out_data += r"$%s\r\n" % (len(key1))
                out_data += r"%s\r\n" % key1
                out_data += r"$%s\r\n" % (len(key2))
                out_data += r"%s\r\n" % key2
                out_data += r"$%s\r\n" % (len(value))

                out_data += "%s\r\n\r\n" % value

    return out_data
