"""Run with python -m jen_agent. The CLI is trusted local access, not a server."""

import argparse
import json
import os
from pathlib import Path
import sys
import uuid

from .archive import Archive
from .core import Agent, ModelError, ResponsesClient, profile
from .state import State, private_directory

ROOT = Path(__file__).resolve().parents[1]
HELP = '''Commands:
  /remember TEXT     Save exactly this CQ-related note for the current session.
  /notes             Inspect saved notes.
  /forget ID         Remove one saved note (old chat messages are separate).
  /clear-history     Delete this session's chat history; saved notes remain.
  /new               Start a new, isolated session. Old sessions remain on disk.
  /profile           Show the current profile fingerprint and source files.
  /help              Show these commands.
  /quit              Exit. Reopen the same session to continue.
Natural-language requests cannot write notes or change the canonical personality.
'''


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--session', default='johnny-main', help='Private conversation name to resume')
    parser.add_argument('--model', default=os.getenv('JEN_MODEL', 'gpt-5.5'))
    parser.add_argument('--data-dir', type=Path, default=Path(os.getenv('JEN_DATA_DIR', str(ROOT.parent / 'jen-agent-private'))))
    parser.add_argument('--check', action='store_true', help='Build/check archive and profile without an API call')
    parser.add_argument('--search', help='Search the archive locally without an API key')
    parser.add_argument('--episode', type=int)
    args = parser.parse_args()
    data = private_directory(ROOT, args.data_dir)
    archive = Archive(ROOT, data / 'archive.sqlite3')
    stats = archive.build()
    if args.check:
        _, fingerprint, sources = profile(ROOT)
        print(json.dumps({'archive': stats, 'profile_hash': fingerprint, 'profile_sources': sources,
                          'api_key_configured': bool(os.getenv('OPENAI_API_KEY')), 'data_directory': str(data)}, indent=2))
        return
    if args.search is not None:
        print(json.dumps(archive.search(args.search, args.episode), ensure_ascii=False, indent=2))
        return
    client = ResponsesClient()
    state = State(data / 'conversations.sqlite3')
    agent = Agent(ROOT, archive, state, client, args.model)
    owner, session = 'local-johnny', args.session
    print(f'Default Jen | session: {session} | model: {args.model}')
    print('Using your existing Jen profile. Type /help for memory controls.')
    print(f'Private history: {data}\nAPI calls send your message, recent context, profile, saved notes and retrieved passages to OpenAI.')
    while True:
        try:
            text = input('\nJohnny: ').strip()
        except (EOFError, KeyboardInterrupt):
            print('\nSession closed.')
            break
        if not text:
            continue
        command, _, value = text.partition(' ')
        try:
            if command == '/quit':
                break
            elif command == '/help':
                print(HELP)
            elif command == '/notes':
                print(json.dumps(state.notes(owner, session), ensure_ascii=False, indent=2))
            elif command == '/remember':
                print(f'Saved note {state.remember(owner, session, value)} in {session}.')
            elif command == '/forget':
                print('Note removed.' if state.forget(owner, session, int(value)) else 'No matching note in this session.')
            elif command == '/clear-history':
                state.clear_history(owner, session)
                print('This session history is deleted. Saved notes remain; use /forget to remove them.')
            elif command == '/new':
                session = 'johnny-' + uuid.uuid4().hex[:10]
                print(f'New session: {session}. Resume later with --session {session}.')
            elif command == '/profile':
                _, fingerprint, files = profile(ROOT)
                print(json.dumps({'profile_hash': fingerprint, 'files': files}, indent=2))
            elif command.startswith('/'):
                print('Unknown command. Type /help.')
            else:
                result = agent.reply(owner, session, text, is_johnny=True)
                print('\nJen: ' + result['text'])
        except (ValueError, ModelError) as error:
            print(str(error))
        except KeyboardInterrupt:
            print('\nTurn interrupted. Type /quit to leave.')


if __name__ == '__main__':
    try:
        main()
    except (ModelError, ValueError) as error:
        print(str(error), file=sys.stderr)
        sys.exit(1)
