"""Exercise full-source database retrieval for manually source-reviewed answers.

Location coverage is an integration check, never an automatic semantic grade.
"""
import json
from lore_store import ROOT, LoreStore, read


def evaluate():
    cases = read(ROOT / 'pilot/answer-cases.json')['cases']
    for name in ('248-259', '299'):
        for case in read(ROOT / f'pilot/reviews/{name}-annotations.json')['task_cases']:
            cases.append({**case, 'answer': case['expected']})
    store = LoreStore()
    results = []
    try:
        for case in cases:
            bundle = store.answer_evidence(case['query'], case['episode'])
            found = {r['evidence'][0]['location'] for r in bundle['context']}
            missing = sorted(set(case['evidence_locations']) - found)
            results.append({**case, 'retrieval_status': 'failed' if missing else 'passed',
                            'missing_windows': missing, 'matched_windows': bundle['matched_windows'],
                            'retrieved_context': bundle['context']})
    finally:
        store.close()
    report = dict(evaluation='development_integration_not_semantic_autograding',
                  cases=results, passed=sum(not r['missing_windows'] for r in results), total=len(results))
    target = ROOT / 'pilot/generated/answer-evidence.json'
    target.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return report


if __name__ == '__main__':
    report = evaluate()
    print(json.dumps(dict(passed=report['passed'], total=report['total'],
                         failures=[{k:r[k] for k in ('id','missing_windows')} for r in report['cases'] if r['missing_windows']]), indent=2))
    raise SystemExit(report['passed'] != report['total'])
