#!/usr/bin/env python
import json
import sys
import urllib.request


def copy_to_clipboard(text):
    try:
        import pyperclip
    except ImportError:
        print('pyperclip <https://pypi.org/project/pyperclip/> is missing.', file=sys.stderr)
        print('copy-paste the following text manually:', file=sys.stderr)
        print('  ' + text, file=sys.stderr)
    else:
        pyperclip.copy(text)


for prid in sys.argv[1:]:
    url = "https://api.github.com/repos/RaRe-Technologies/sqlitedict/pulls/%s" % prid
    with urllib.request.urlopen(url) as fin:
        prinfo = json.load(fin)

    prinfo['user_login'] = prinfo['user']['login']
    prinfo['user_html_url'] = prinfo['user']['html_url']
    text = '- %(title)s (PR [#%(number)s](%(html_url)s), [@%(user_login)s](%(user_html_url)s))' % prinfo
    print(text)
