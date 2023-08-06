#!/usr/bin/env python3
# api: cli
# encoding: utf-8
# type: transform
# title: HTML to mallard
# description: convert mkdocs´ html output to mallard/yelp xml
# category: documentation
# keywords: mkdocs mallard
# version: 0.1.9
# depends: python (>= 3.6), python:PyYAML (>= 5.0)
# license: Public Domain
# url: https://fossil.include-once.org/modseccfg/wiki/html2mallard
# 
# Poor transformation approach, mostly salvaging some HTML structures
# and reshuffling document body into mallard <page> with allowed
# inline markup.
# XSLT might have been easier, but doesn't work on most HTML.
# BS/lxml is way overkill for this task (hence zero such tools).
# Noone's doing a markdown to ducktype/mallard converter either.


import os, sys
import re, html
from textwrap import dedent, indent
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
""").lstrip()

# regex all the way
extract = {
    # meta info
    "mkdocs_page_name = \"(.*?)\";": "title",
    "<title>(.+?)</title>": "title",
    '<a class="reference internal" href="(\w+).html">.+?</a>': "links",
    # flags
    '(<.+>)': "is_html",
    '(mkdocs)': "is_mkdocs",
    '(fossil|timeline)': "is_fossil",
    "(SphinxRtdTheme|readthedocs-doc-embed.js|aria-label=)": "is_sphinx",
     "(&\w+;)": "has_entities",
    '(<p>|<div|<table|<li>|<img|<strong|<em|<h\d|<span|<code)': "convert",
}
rewrite = {
    # trim and cleanup
    ("GENERAL HTML", "is_html"): {
        "<script.+?</script>": "",
        "<head>.+?</head>": "",
        "<!DOCTYPE[^>]+>|<html[^>]*>|</body>|</html>": "",
        "<span></span>": "",
    },
    ("MKDOCS", "is_mkdocs"): {
        "^.+?</nav>": "",   # might strip too much for any bottom-navigation templates
        "^.+?<div\srole=\"main\">": "",   # mkdocs RTD template
        '<footer>.+\\Z': "",    # mkdocs footer
        'Next\s<span\sclass="icon\sicon-circle-arrow-right"></span>.+\\Z': "",   # mkdocs RTD theme
    },
    ("FOSSIL WIKI", "is_fossil"): {
        '<footer\sid="fossil-footer">.+\\Z': "", # fossil footer
        '\\A.+<main[^>]*>': "", # wiki header
    },
    ("RTD.IO/SPHINX", "is_sphinx"): {
        "^.+?</nav>": "",   # might strip too much for any bottom-navigation templates
        '<footer>.+\\Z': "", 
        '<div\srole="navigation"\saria-label="breadcrumbs\snavigation">.+?</div>': "",  # RTD.io
    },
    ("ENTITIES", "has_entities"): {
        "&rarrq;": "→",
        "&nbsp;": "␣",
        "&mdash;": "–",
        "&(?!lt|gt|amp)\w+;": lambda m: html.unescape(m[0]),
    },

    # actual conversions
    ("CONVERSIONS", "convert"): {
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
        "(<h\d[^>]*>.+?(?<!\s))\s*(?=<h\d|<footer|</body|\Z)": "\n<section>\n\\1\n</section>\n",
        "<(?:h1|h2)[^>]*>(.+?)</(?:h1|h2)>": "<title>\\1</title>",
        "<(?:h3|h4)[^>]*>(.+?)</(?:h3|h4)>": "<subtitle>\\1</subtitle>",
        "<(?:h5|h6)[^>]*>(.+?)</(?:h5|h7)>": "<em>\\1</em>",
        "<strong>(.+?)</strong>": "<em style=\"strong\">\\1</em>",
        # lists
        "<ol>(.+?)</ol>": "<steps>\\1</steps>",
        "<ul>(.+?)</ul>": "<list>\\1</list>",
        "<li>(.+?)</li>": "<item><p>\\1</p></item>",
        "<dl>(.+?)</dl>": "<terms>\\1</terms>",
        "<dt>(.+?)</dt>": "<item><title>\\1</title>",
        "<dd>(.+?)</dd>": "<p>\\1</p></item>",
        # fix nested list   \1         \2                 \3                      \4    
        "(<(?:item|steps|terms)>)<p> ([^<]+(?<!\s)) \s* <(list|steps|terms)> \s* (.+?) </\\3>":
            "\\1<p>\\2</p>\n <\\3>\n<item><p>\\4 </\\3>\n</item>",
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
        "<span\sclass=\"([\w\-\s]+)\">(.+?)</span>": "<span style=\"\\1\">\\2</span>",
        "<code\sclass=\"([\w\-\s]+)\">(.+?)</code>": "<code><span style=\"\\1\">\\2</span></code>",
    },
     
    ("HTML BEGONE", "is_html"): { 
        # strip any remaining non-mallard tags, except: |div|revision|thead
        """</? 
           (?!(?:page|section|info|credit|link|link|title|desc|title|keywords|license|desc|
           years|email|name|links|code|media|p|screen|quote|comment|example|figure|listing|
           note|synopsis|list|item|steps|item|terms|item|tree|item|table|col|colgroup|tr|
           tbody|tfoot|td|th|title|subtitle|desc|cite|app|code|cmd|output|em|file|gui|guiseq|hi|
           link|media|keyseq|key|span|sys|input|var)\\b)
           \w+[^>]* >""": "",
    },

    ("PRETTIFY", "is_html"): {
        # prettify sections
        "(<section>)(.+?)(</section>)": lambda m: f"{m[1]}\n{indent(m[2].strip(), prefix=' ')}\n{m[3]}",
        # strip lone </section>, empty spans
        "(<section>.+?</section>)|</section>": "\\1",
        "(<span[^>]*></span>)": "",
    }
}


def convert(html, fn, debug=False):

    # prepare snippets for .format kwargs
    kw = {
        "id": re.sub("^.+/|\.\w+$", "", fn),
        "desc": "",
        "title": "",
        "body": "",
        "links": "",
    }
    for rx, name in extract.items():
        m = re.search(rx, html)
        if m and (not name in kw or not kw[name]):
            if name == "links":
                kw[name] = re.findall(rx, html)
            else:
                kw[name] = re.sub("&\w+;|<.+?>", "", m.group(1))
    if kw["links"]:
        kw["links"] = indent("\n".join(f"<link type=\"guide\" xref=\"{id}\"/>" for id in kw["links"]), prefix=" "*8)
        
    # simplify/convert html
    for (group, flag), patterns in rewrite.items():
        if not flag in kw: # possibly skip rule group
            continue
        elif debug:
            sys.stderr.write(f"group: {group}\n")
        for rx, repl in patterns.items():
            l = len(html)
            html = re.sub(rx, repl, html, 0, re.X|re.M|re.S|re.I)
            if debug and l != len(html):
                sys.stderr.write(f"rewrite: {len(html) - l} bytes, pattern: ~{rx}~\n")
    kw["body"] = html
    
    # return converted
    return template.format(**kw)

# single file
def convert_file(fn, debug=0):
    with open(fn, "r", encoding="utf-8") as f:   # → html2mallard "site/index.html"
        return convert(f.read(), fn, debug)

# process directory
def mkdocs():
    src = open("mkdocs.yml", "r")   # → ought to be in current directory
    cfg = yaml.load(src, Loader=yaml.Loader)
    srcdir = cfg["site_dir"]
    target = cfg["mallard_dir"]    # → required param in mkdocs.yml
    if not os.path.exists(target):
        os.makedirs(target)
    for fn in glob(f"{srcdir}/*.html"):
        page = convert_file(fn)
        fn = re.sub(".+/", "", fn)
        fn = re.sub("\.html", ".page", fn)
        with open(f"{target}/{fn}", "w", encoding="utf-8") as f:
            f.write(page)

# entry_points
def main():
    if len(sys.argv) >= 2:
        dbg = set(["-d", "--debug", "-D"]) & set(sys.argv)
        print(convert_file(sys.argv[1], debug=dbg)) # first argument as input file
    else:
        mkdocs() # iterate through site/*html

if __name__ == "__main__":
    main()
    
