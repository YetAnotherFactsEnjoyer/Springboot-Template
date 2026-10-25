#!/usr/bin/env python3
"""Rename a fresh copy of this template before its first deployment."""
import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OLD_PACKAGE = 'com.example.starter'
OLD_DIR = Path('com/example/starter')


def main():
    parser = argparse.ArgumentParser(description='Initialize a new project from this starter.')
    parser.add_argument('--name', required=True, help='Project slug, e.g. stockflow')
    parser.add_argument('--package', required=True, help='Java package, e.g. com.stockflow')
    args = parser.parse_args()
    if not re.fullmatch(r'[a-z][a-z0-9-]*', args.name):
        parser.error('name must be a lowercase slug like stockflow or my-api')
    if not re.fullmatch(r'[a-z][a-z0-9_]*(?:\.[a-z][a-z0-9_]*)+', args.package):
        parser.error('package must be lowercase dotted identifiers like com.acme.stockflow')
    if args.package == OLD_PACKAGE:
        parser.error('use a project-specific package instead of the template package')
    if (ROOT / '.env').exists():
        parser.error('rename before initializing .env and database to avoid credential/schema mismatches')
    if not (ROOT / 'src/main/java' / OLD_DIR).exists():
        parser.error('template was already renamed; use a fresh copy')
    db_name = args.name.replace('-', '_')
    if len(db_name) > 40:
        parser.error('project name is too long for this starter database configuration')

    for file in ROOT.rglob('*'):
        if file.is_file() and file.suffix in {'.java', '.gradle', '.yaml', '.yml', '.md', '.example'}:
            if '.git' in file.parts or 'build' in file.parts:
                continue
            content = file.read_text(encoding='utf-8')
            content = (content.replace(OLD_PACKAGE, args.package)
                     .replace('spring-backend-starter', args.name)
                     .replace('template_app', db_name)
                     .replace('template_user', db_name + '_user')
                     .replace('app-postgres', db_name + '-postgres'))
            if file.name == 'build.gradle':
                parts = args.package.split('.')
                group = '.'.join(parts[:-1]) if len(parts) > 2 else args.package
                content = content.replace("group = 'com.example'", "group = '" + group + "'")
            file.write_text(content, encoding='utf-8')

    for tree in ['src/main/java', 'src/test/java']:
        old = ROOT / tree / OLD_DIR
        if old.exists():
            new = ROOT / tree / args.package.replace('.', '/')
            if new.exists():
                parser.error('target package already exists')
            new.parent.mkdir(parents=True, exist_ok=True)
            old.rename(new)
            parent = old.parent
            while parent != ROOT / tree and not any(parent.iterdir()):
                parent.rmdir()
                parent = parent.parent
    print(f'Initialized {args.name} with package {args.package} and DB {db_name}.')
    print('Next: python3 scripts/init_env.py')


if __name__ == '__main__':
    main()
