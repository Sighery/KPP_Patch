#!/usr/bin/env python

from src.tui.cli import form_parser

TAG_START = "<!--CH0-->\n"
TAG_END = "<!--CH1-->\n"

if __name__ == "__main__":
    parser = form_parser()

    processed = []

    with open("README.md", "r", encoding="utf-8") as readme:
        in_replace = False

        for line in readme:
            if line == TAG_START:
                in_replace = True
                processed.append(line)
                processed.append("```\n")
                processed.append(parser.format_help())
                processed.append("```\n")
                continue

            if line == TAG_END:
                in_replace = False
                processed.append(line)
                continue

            if in_replace:
                continue

            processed.append(line)

    with open("README.md", "w", encoding="utf-8") as readme:
        readme.write("".join(processed))
