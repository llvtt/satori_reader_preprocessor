#!/usr/bin/env python3

import csv
import sys


def process_row(row):
    expression = row[2]
    reading = row[3]
    gloss = row[7]
    pos = row[8]

    # Primary context, no furigana
    primary_context = row[9]

    # Secondary context, no furigana
    secondary_context = row[15].strip()
    tertiary_context = row[21].strip()
    additional_contexts = []
    if secondary_context:
        additional_contexts.append(secondary_context)
    if tertiary_context:
        additional_contexts.append(tertiary_context)
    additional_context_markup = ''.join(
        f'<div class="additional-context">{context}</div>'
        for context in additional_contexts
    )

    # Create glossary section.
    glossary = (
        f'{additional_context_markup}'
        f'<div class="parts-of-speech">{pos}</div>'
        f'<div class="glossary">{gloss}</div>'
    )

    return (
        expression,
        reading,
        glossary,
        primary_context,
    )



def process_rows(rows):
    for row in rows:
        yield process_row(row)


def main(ifile, ofile):
    with open(ifile, 'r') as infile:
        reader = csv.reader(infile)
        # Skip header line.
        next(reader)

        with open(ofile, 'w') as outfile:
            writer = csv.writer(outfile)
            writer.writerows(process_rows(reader))

    print('Done')


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print(f'USAGE: {sys.argv[0]} <input filename> <output filename>')
        exit(1)

    main(sys.argv[1], sys.argv[2])
