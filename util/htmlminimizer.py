"""Quick-and-dirty HTML minimizer"""

import os
import sys
import re
import html.entities
import itertools

_SERVERS = ['a.wearehugh.com',
            'b.wearehugh.com',
            'c.wearehugh.com',
            'd.wearehugh.com']
available_server = itertools.cycle(_SERVERS)
input_file = sys.argv[1]
output_file = sys.argv[2]
in_pre = False
with open(output_file, 'w', encoding="utf-8") as _out, open(input_file, encoding="utf-8") as _in:
    for line in _in:
        # round-robin image servers
        if "<img src=i/" in line:
            line = line.replace("<img src=i/", "<img src=http://" + next(available_server) + "/dih5/")
        if "url(i/" in line:
            line = line.replace("url(i/", "url(http://" + next(available_server) + "/dih5/")

        # replace entities with Unicode characters
        for e in re.findall('&(.+?);', line):
            if e in ('lt', 'amp', 'quot', 'apos', 'nbsp'):
                continue
            n = html.entities.name2codepoint.get(e)
            if not n:
                if e.count('#x'):
                    # it's late, forgive me
                    n = eval(e.replace('#', '0'))
                elif e.count('#'):
                    n = int(e.replace('#', ''))
                else:
                    continue
            line = line.replace('&' + e + ';', chr(n))
    
        # strip leading and trailing whitespace, except inside <pre> blocks
        g = line.strip()
        if g.count('<pre'):
            in_pre = True
        if g.count('</pre'):
            # XXX this will break if you have </pre><pre> in one line
            in_pre = False
            g = line.rstrip()
        if in_pre:
            _out.write(line)
        else:
            _out.write(g)
        if g.lower() == '<!doctype html>':
            _out.write('\n<!-- sorgente in formato leggibile senza dar fuori di zucca su http://github.com/alieb/diveintohtml5.it/blob/master/{0} -->\n'.format(os.path.basename(input_file)))
