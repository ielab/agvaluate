import argparse
from pyserini.search import SimpleSearcher
from tqdm import tqdm


def write_doc_to_collection(docid, searcher: SimpleSearcher, out_file):
    text = searcher.doc(docid).contents().replace("\n", " ").replace("\t", " ")
    out_file.write(f"{docid}\t{text}\n")


def build_collection(index_dir, collection_outfile, qrels=None):
    searcher = SimpleSearcher(index_dir)

    with open(collection_outfile, 'w') as out_file:
        if qrels:
            with open(qrels) as qfh:
                for line in tqdm(qfh, f"Writing docs from {qrels}"):
                    write_doc_to_collection(line.split()[2], searcher, out_file)
        else:
            for i in tqdm(range(searcher.num_docs), desc=f"Outputting {searcher.num_docs} docs"):
                write_doc_to_collection(searcher.doc(i).docid(), searcher, out_file)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--index_dir', required=True, help="Anserini index")
    parser.add_argument('--collection', help="File to write collection", required=True)
    parser.add_argument('--qrels', help="Use this qrel file for docs")

    args = parser.parse_args()

    build_collection(index_dir=args.index_dir, collection_outfile=args.collection, qrels=args.qrels)
    print(f"Collection written to {args.collection}")
