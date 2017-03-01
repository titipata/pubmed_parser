#!/usr/bin/env python

if __name__ == '__main__':

    index_file = list()
    index_file.extend(['---\n',
                       'layout: default\n',
                       '---\n',
                       '\n'])

    with open('../README.md') as f:
        lines = f.readlines()
        for l in lines:
            index_file.append(l)

    output_file = open('index.md', 'w')
    output_file.write("".join(index_file))
