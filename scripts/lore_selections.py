"""Explicit source-backed list membership; never infer picks from discussion time."""
import re


def validate_selection_lists(record, source):
    lists = record.get('selection_lists', [])
    if not isinstance(lists, list):
        raise ValueError('Selection lists must be a list')
    games = {g['id'] for g in record['games']}
    seen = set()
    count = 0
    def evidence(proofs):
        if not isinstance(proofs, list) or not proofs:
            raise ValueError('Selection membership needs source evidence')
        for proof in proofs:
            if not proof.get('quote') or proof['quote'] not in source.get(proof.get('location'), ''):
                raise ValueError('Unsupported selection evidence')
    for group in lists:
        if not group.get('id') or group['id'] in seen:
            raise ValueError('Selection list needs unique ID')
        seen.add(group['id'])
        if not group.get('label') or not group.get('summary') or not group.get('purpose'):
            raise ValueError('Selection list needs criteria and purpose')
        if 'subject' not in group or not (group['subject'] is None or isinstance(group['subject'], str)):
            raise ValueError('Selection list needs explicit subject or uncertainty')
        evidence(group.get('evidence'))
        if not group.get('entries'):
            raise ValueError('Empty selection list')
        members, ordinals = set(), set()
        for entry in group['entries']:
            ref = entry.get('game_ref')
            if ref not in games or ref in members:
                raise ValueError('Unknown or repeated list member')
            members.add(ref)
            if entry.get('status') not in ('selected', 'considered', 'rejected', 'joke'):
                raise ValueError('List membership status must be explicit')
            ordinal = entry.get('ordinal')
            if ordinal is not None:
                if type(ordinal) is not int or ordinal < 1 or ordinal in ordinals or entry['status'] != 'selected':
                    raise ValueError('Invalid or repeated selected-list ordinal')
                ordinals.add(ordinal)
            if not entry.get('reason'):
                raise ValueError('List membership needs rationale')
            evidence(entry.get('evidence'))
            count += 1
    return count


def selection_query(record, query):
    """Return candidates and disclosed constraints, never a merged consensus list."""
    q = query.casefold()
    # A second question about a named person's reaction must not turn a
    # shared first-clause list into that person's authored list.
    owner_query = re.split(r'\band\s+(?:which|what|how|why)\b', query, maxsplit=1, flags=re.IGNORECASE)[0]
    groups = record.get('selection_lists', [])
    subjects = {g['subject'] for g in groups if g.get('subject')}
    named = {name for name in subjects if re.search(r'\b' + re.escape(name.casefold()) + r'\b', owner_query.casefold())}
    explicit = re.search(r"\b([A-Za-z]+)['’]s\s+(?:(?:starter|aspirational|strive|hot|secondary)\s+)?(?:lists?|picks|selections)\b", query)
    if explicit is None:
        explicit = re.match(r'^([A-Z][a-z]+(?: [A-Z][a-z]+)?)\s+(?:starter|aspirational|strive|hot|secondary)\s+(?:lists?|picks|selections)\b', query)
    unresolved = None
    if explicit and explicit.group(1).casefold() not in ('what', 'which', 'the', 'both'):
        if explicit.group(1).casefold() not in {n.casefold() for n in subjects}:
            unresolved = 'Requested list owner is not represented in typed list data'
            groups = []
    if named:
        groups = [g for g in groups if g['subject'] in named]
    aliases = {'starter': ('starter', 'starting'), 'aspirational': ('aspirational', 'strive'),
               'hot': ('hot',), 'secondary': ('secondary',), 'launch': ('launch',)}
    wanted, excluded = set(), set()
    for purpose, terms in aliases.items():
        for term in terms:
            if re.search(r'\b(?:not|except|excluding|without)\s+(?:(?:his|her|their|the|any)\s+)?' + term + r'\b', q):
                excluded.add(purpose)
            elif re.search(r'\b' + term + r'\b', q):
                wanted.add(purpose)
    groups = [g for g in groups if g['purpose'] not in excluded and (not wanted or g['purpose'] in wanted)]
    if not groups and wanted and unresolved is None:
        unresolved = 'Requested purpose has no matching typed list for this owner/scope'
    count_match = re.search(r'\b(\d+|ten|three|five)[ -]games?\b', q)
    count = None
    if count_match:
        value = count_match.group(1)
        count = int(value) if value.isdigit() else {'ten': 10, 'three': 3, 'five': 5}[value]
        groups = [g for g in groups if sum(e['status'] == 'selected' for e in g['entries']) == count]
    return dict(lists=groups, subject_filters=sorted(named), purpose_filters=sorted(wanted),
                excluded_purposes=sorted(excluded), selected_count=count, unresolved=unresolved,
                warning='Explicit source-backed list candidates; keep actors, purposes and membership states separate. Missing typed data is not archive absence.')


def matching_selection_lists(record, query):
    return selection_query(record, query)['lists']
