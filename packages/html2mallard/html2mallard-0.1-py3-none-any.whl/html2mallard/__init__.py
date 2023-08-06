#!/usr/bin/env python3
# api: cli
# encoding: utf-8
# type: transform
# title: HTML to mallard
# description: convert mkdocs´ html output to mallard/yelp xml
# category: documentation
# keywords: mkdocs mallard
# version: 0.1
# license: Public Domain
# url: https://fossil.include-once.org/modseccfg/wiki/html2mallard
# 
# Poor transformation approach, mostly salvaging some HTML structures
# and reshuffling document body into mallard <page> and allowed
# inline markup.
# XSLT might have been easier, but doesn't work on HTML.
#


import os, sys
import re
from textwrap import dedent
from glob import glob
import yaml


# output
template = dedent("""
    <page
        xmlns="http://projectmallard.org/1.0/"
        type="guide"
        id="{id}">

        <info>
            <link type="guide" xref="index#nav"/>
            {links}
            <desc>{desc}</desc>
        </info>

        <title>{title}</title>

        {body}

    </page>
""")

# regex all the way
extract = {
    "mkdocs_page_name = \"(.*?)\";": "title",
    "<title>(.+?)</title>": "title",
    '<a class="reference internal" href="(\w+).html">.+?</a>': "links",
}
rewrite = {
    # trim and cleanup
    "^.+?</nav>": "",
    "^.+?<div\srole=\"main\">": "",   # mkdocs RTD template
    "<script.+?</script>": "",
    "<head>.+?</head>": "",
    "</body>|</html>": "",
    "<span></span>": "",
    '<footer>.+\\Z': "",    # mkdocs footer
    'Next\s<span\sclass="icon\sicon-circle-arrow-right"></span>.+\\Z': "",
    "&rarrq;": "→",
    "&nbsp;": "␣",
    #"&quot;": "\"",
    #"&apos;": "\'"",
    "&(?!lt|gt|amp)\w+;": "",
    
    # actual conversions
    "<div\sclass=\"admonition\s(?:note|abstract|summary|tldr)\">(.+?)</div>": "<note style=\"tip\">\\1</note>",
    "<div\sclass=\"admonition\s(?:todo|seealso)\">(.+?)</div>": "<note style=\"advanced\">\\1</note>",
    "<div\sclass=\"admonition\s(?:danger|error|failure|fail|missing|bug)\">(.+?)</div>": "<note style=\"bug\">\\1</note>",
    "<div\sclass=\"admonition\s(?:info|todo)\">(.+?)</div>": "<note style=\"important\">\\1</note>",
    "<div\sclass=\"admonition\s(?:example|quote|cite)\">(.+?)</div>": "<note style=\"plain\">\\1</note>",
    "<div\sclass=\"admonition\s(?:question|help|faq)\">(.+?)</div>": "<note style=\"sidebar\">\\1</note>",
    "<div\sclass=\"admonition\s(?:notes|tip|hint|important)\">(.+?)</div>": "<note style=\"tip\">\\1</note>",
    "<div\sclass=\"admonition\s(?:warning|caution|attention)\">(.+?)</div>": "<note style=\"warning\">\\1</note>",
    "<div\sclass=\"admonition(?:\s\w+)?\">(.+?)</div>": "<note style=\"tip\">\\1</note>",
    "<p\sclass=\"admonition-title\">(.+?)</p>": "<subtitle>\\1</subtitle>",
    # headlines
    "(<h\d[^>]*>.+?)(?=<h\d|<footer|</body|\Z)": "\n<section>\n\\1</section>\n",
    "<(?:h1|h2)[^>]*>(.+?)</(?:h1|h2)>": "<title>\\1</title>",
    "<(?:h3|h4)[^>]*>(.+?)</(?:h3|h4)>": "<subtitle>\\1</subtitle>",
    "<(?:h5|h6)[^>]*>(.+?)</(?:h5|h7)>": "<em>\\1</em>",
    "<strong>(.+?)</strong>": "<em>\\1</em>",
    # links
    "<ol>(.+?)</ol>": "<steps>\\1</steps>",
    "<ul>(.+?)</ul>": "<list>\\1</list>",
    "<li>(.+?)</li>": "<item><p>\\1</p></item>",
    # links
    "<a\shref=\"([^\">]+)\.html\">(.+?)</a>": "<link type=\"seealso\" xref=\"\\1\">\\2</link>",
    "<a\shref=\"(\w+://[^\">]+)\">(.+?)</a>": "<link type=\"seealso\" href=\"\\1\">\\2</link>",
    # media
    "<img[^>]+src=\"(.+?)\"[^>]*>": "<media type=\"image\" src=\"\\1\" mime=\"image/png\" />",
    # tables
    "</?tbody>": "",
    "<table[^>]*>": "<table shade=\"rows cols\" rules=\"rows cols\"><tbody>",
    "</table>": "</tbody></table>",
    "<tr[^>]*>": "<tr>",
    "<(td|th)\\b[^>]*>": "    <td><p>",
    "</(td|th)\\b[^>]*>": "</p></td>",

    # strip codehilite markup
    "<span\sclass=\"\w{1,2}\">(.+?)</span>": "<span>\\1</span>",
    
    # strip any remaining non-mallard tags, except: |div|revision|thead
    """</? 
       (?!(?:page|section|info|credit|link|link|title|desc|title|keywords|license|desc|
       years|email|name|links|code|media|p|screen|quote|comment|example|figure|listing|
       note|synopsis|list|item|steps|item|terms|item|tree|item|table|col|colgroup|tr|
       tbody|tfoot|td|th|title|subtitle|desc|cite|app|code|cmd|output|em|file|gui|guiseq|hi|
       link|media|keyseq|key|span|sys|input|var)\\b)
       \w+[^>]* >""": ""
}


def convert(html, fn):

    # prepare snippets for .format kwargs
    kw = {
        "id": re.sub("^.+/|\.\w+$", "", fn),
        "desc": "",
        "title": "",
        "body": "",
        "links": [],
    }
    for rx, name in extract.items():
        m = re.search(rx, html)
        if m and not kw[name]:
            if name == "links":
                kw[name] = re.findall(rx, html)
            else:
                kw[name] = m.group(1)
    if kw["links"]:
        kw["links"] = "\n        ".join(f"<link type=\"guide\" xref=\"{id}\"/>" for id in kw["links"])
        
    # simplify/convert html
    for rx, repl in rewrite.items():
        html = re.sub(rx, repl, html, 0, re.X|re.M|re.S|re.I)
    kw["body"] = html
    
    # return converted
    return template.format(**kw)


def cnv_file(fn):
    with open(fn, "r", encoding="utf-8") as f:
        return convert(f.read(), fn)

def mkdocs():
    src = open("mkdocs.yml", "r") # mkdocs config should be in current directory
    cfg = yaml.load(src, Loader=yaml.Loader)
    srcdir = cfg["site_dir"]
    target = cfg["mallard_dir"]
    if not os.path.exists(target):
        os.makedirs(target)
    for fn in glob(f"{srcdir}/*.html"):
        page = cnv_file(fn)
        fn = re.sub(".+/", "", fn)
        fn = re.sub("\.html", ".page", fn)
        with open(f"{target}/{fn}", "w", encoding="utf-8") as f:
            f.write(page)

def main():
    if len(sys.argv) == 2:
        print(cnv_file(sys.argv[1])) # e.g. "site/index.html"
    else:
        mkdocs() # iterate through site/*html

if __name__ == "__main__":
    main()
    
