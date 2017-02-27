#!/usr/bin/env python

import io
import re
import requests
import yaml


def slugify(title):
    return re.sub(r'[^a-zA-Z0-9 _-]', '', title).replace(' ', '-')[:60]


def main():
    # Get feed
    r = requests.get('https://raw.githubusercontent.com/ViDA-NYU/reproducibility-news/master/news.yaml')

    for d in yaml.load_all(r.content):
        # Generate file name
        slug = slugify(d['title'].strip())
        file_name = 'posts/directory/%s_%s.html' % (d['date'].strftime('%Y-%m-%d'), slug)

        # Open
        with io.open(file_name, 'w', encoding='utf-8') as fp:
            fp.write(u"""\
<!--
.. title: {title}
.. slug: {slug}
.. date: {date}
.. link: {link}
.. tags: {tags}
.. description:
-->
<!DOCTYPE html>
<html lang="en">
<body>

<p>{text}</p>

""".format(title=d['title'].strip(), slug=slug,
           date=d['date'].strftime('%Y-%m-%d %H:%M:%S'),
           link=d['link'].strip(), tags=', '.join(d['tags']),
           text=d['description'].strip()))


if __name__ == '__main__':
    main()
