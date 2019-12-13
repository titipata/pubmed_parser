#!/usr/bin/env python
import os


if __name__ == '__main__':

    index_file = [
        '---\n',
        'layout: default\n',
        '---\n',
        '\n'
    ]

    with open(os.path.join('..', 'README.md')) as f:
        lines = f.readlines()
        for l in lines:
            index_file.append(l)

    output_file = open('index.md', 'w')
    output_file.write("".join(index_file))
