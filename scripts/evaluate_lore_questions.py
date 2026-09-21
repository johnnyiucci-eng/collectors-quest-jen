"""Original-wording evidence retrieval; not generated-answer or blind semantic scoring."""
import argparse
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lore_store import ROOT, LoreStore, collection_path, read


def evaluate(collections):
    results = []
    for collection in collections:
        base = collection_path(ROOT, collection)
        store = LoreStore(collection=collection)
        try:
            cases = [case for path in sorted((base / 'reviews').glob('*-annotations.json'))
                     for case in read(path).get('task_cases', [])]
            if len({c['id'] for c in cases}) != len(cases):
                raise ValueError('Duplicate task IDs in ' + collection)
            measured = []
            excluded = []
            for case in cases:
                if not isinstance(case.get('question'), str) or not case['question'].strip():
                    excluded.append(case['id'])
                    continue
                bundle = store.answer_evidence(case['question'], case['episode'])
                found = {r['title'] for r in bundle['context']}
                required = set(case['evidence_locations'])
                if not required:
                    raise ValueError('Question lacks required evidence: ' + case['id'])
                measured.append(dict(id=case['id'], episode=case['episode'], question=case['question'],
                                     missing_windows=sorted(required - found),
                                     required_windows=len(required),
                                     context_coverage=bundle['context_coverage'],
                                     query_diagnostics=bundle['query_diagnostics'], route=bundle['route']['intent']))
            results.append(dict(collection=collection, passed=sum(not c['missing_windows'] for c in measured),
                                total=len(measured), excluded_without_original_question=excluded, cases=measured))
        finally:
            store.close()
    return dict(passed=sum(r['passed'] for r in results), total=sum(r['total'] for r in results),
                excluded=sum(len(r['excluded_without_original_question']) for r in results), results=results,
                limits='Original wording, not blind paraphrases. Required-window retrieval only; read context to judge claims. '
                       'High returned-window coverage is reported, not treated as precision or semantic correctness.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--collection', action='append', required=True)
    args = parser.parse_args()
    result = evaluate(args.collection)
    print(json.dumps(result, indent=2))
    return int(result['passed'] != result['total'])


if __name__ == '__main__':
    raise SystemExit(main())
