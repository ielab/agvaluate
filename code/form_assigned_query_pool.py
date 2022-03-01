import argparse
import time
from collections import defaultdict
import json
from pathlib import Path
from getpass import getpass

import requests
from tqdm import tqdm


def read_run_file(run_file):
    """
    Read a TREC results file.
    :param run_file: filename of TREC results file.
    :return: qid -> [docs].
    """
    results = defaultdict(list)
    with open(run_file) as fh:
        for line in fh:
            qid, _, doc, rank, score, _ = line.split()
            results[qid].append(doc)
    return results


def fuse_run_file(run_files, top_k_docs):
    """
    Fuses multiple ranked files according to recip rank fusion.
    :param run_files: list of filenames of TREC results files.
    :param top_k_docs: truncate at k documents.
    :return: Fused ranked list qid -> [docs].
    """
    runs = [read_run_file(r) for r in run_files]
    fused = defaultdict(list)
    for qid in set([k for r in runs for k in r.keys()]):
        scores = defaultdict(int)
        for r in runs:
            for rank, doc in enumerate(r[qid]):
                scores[doc] += 1 / (rank + 1)
        fused[qid] = [doc for doc, score in sorted(scores.items(), key=lambda item: item[1], reverse=True)]
        if len(fused[qid]) > top_k_docs:
            fused[qid] = fused[qid][:top_k_docs]
    return fused


def pool_to_agotator_json(runs, query_file, tag=None):
    """
    Converts a rank list into a JSON format suitable for Agotator.
    :param tag: A name for this question set to add to Agotator
    :param query_file: file containg query id and query text.
    :param runs: ranked list qid -> [docs].
    :return: JSON for Agotator data/assigned/question endpoint.
    """
    with open(query_file) as fh:
        questions = {line.split(',', 1)[0]: line.split(',', 1)[1].strip() for line in fh if line.strip()}

    if not tag:
        tag = Path(query_file).stem

    pool = []
    for qid, ranking in runs.items():
        pool.append({'questionId': qid, 'questionText': questions[qid], 'passages': ranking, 'tag': tag})

    return pool


def print_trec_ranking(run, tag):
    for qid, docs in runs.items():
        for rank, doc in enumerate(docs):
            print(f"{qid} Q0 {doc} {rank + 1} {-rank + 1} {tag}")


def post_question_to_server(json_content, url, user, passwd):
    for item in tqdm(json_content, desc=f"Uploading questions"):
        r = requests.post(url, data=json.dumps(item), auth=(user, passwd),
                          headers={'Content-type': 'application/json', 'accept': '*/*'})
        r.raise_for_status()

        time.sleep(0.1)


if __name__ == '__main__':
    argparser = argparse.ArgumentParser(description="Load assigned tasks into Agotator")
    argparser.add_argument('-q', '--query_file', help='Query file in "qid, qrt" format.', required=True)
    argparser.add_argument('-t', '--tag', help='Tag to add', required=True)
    argparser.add_argument('run_files', nargs='+', help='TREC format ranking file.')
    argparser.add_argument('-k', '--top_k_docs', type=int, default=100, help='Depth of ranked docs to upload.')
    argparser.add_argument('--trec_ranking', action='store_true', help="Output results in TREC format")
    argparser.add_argument('-u', '--user', help='Username.', required=False)
    argparser.add_argument('-p', '--passwd', help='Password.', action='store_true')
    argparser.add_argument('--url', help='Host of Agotator.')

    args = argparser.parse_args()

    runs = fuse_run_file(args.run_files, top_k_docs=args.top_k_docs)
    json_pool = pool_to_agotator_json(runs, query_file=args.query_file, tag=args.tag)

    if args.url and args.user and args.passwd:
        passwd = getpass('Please enter the password: ')
        post_question_to_server(json_pool, args.url, args.user, passwd)
    elif args.trec_ranking:
        print_trec_ranking(runs, tag=args.tag)
    else:
        print(json.dumps(json_pool))
