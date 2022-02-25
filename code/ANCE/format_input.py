# _*_ coding:utf-8 _*_
#**********************************************************************************************************************
# author:       Ahmed Mourad
# date:         21 Feb 2022
# description:  Utility script to resolve the mismatch between pyserini query file format and agvaluate format
#               1. Convert hashstring ids to int ids
#               2. Map the results to the original hash id
#**********************************************************************************************************************
import argparse
import os
import pandas as pd

def hash2int(args):
    """ Convert HashQID to IntQID based on the pandas index
    and use tab separator

    Input: list of input csv files for the queries
    Output: List of tsv files with the same names
    """
    for f in args.input:
        queries = pd.read_csv(f, header=None)
        queries.columns = ['QID', 'Query']
        outfpath = os.path.splitext(f)[0]
        queries['Query'].to_csv(outfpath+'.tsv', header=None, sep='\t')

def int2hash(args):
    """ Map IntQID back to HashQID

    Input: list of input csv and trec run files; read in pairs
    Output: list of txt run files with the same names
    """
    for q, r in zip(args.input[::2], args.input[1::2]):
        queries = pd.read_csv(q, header=None)
        queries.columns = ['HashQID', 'Query']
        
        runs = pd.read_csv(r, sep=' ', header=None)
        runs.columns = ['QID', 'QLabel', 'DocID', 'Rank', 'Score', 'Engine']

        runs['QID'] = runs['QID'].replace(queries['HashQID'].to_dict())
        outfpath = os.path.splitext(r)[0]+'.txt'
        runs.to_csv(outfpath, header=None, sep=' ', index=False)
        

if __name__ == "__main__": 
    parser = argparse.ArgumentParser(prog='FORMAT INPUT', description='Utility script to map hashstrings to integers and vise-versa.')
    subparsers = parser.add_subparsers()

    hash2int_parser = subparsers.add_parser('hash2int', description='Convert hashstrings to integers')
    hash2int_parser.add_argument('input', nargs='+', help='list of input csv files for the queries')
    hash2int_parser.set_defaults(func=hash2int)
    
    int2hash_parser = subparsers.add_parser('int2hash', description='Convert integers to hashstrings')
    int2hash_parser.add_argument('input', nargs='+', help='list of input csv and trec run files; read in pairs')
    int2hash_parser.set_defaults(func=int2hash)

    args = parser.parse_args()
    args.func(args)