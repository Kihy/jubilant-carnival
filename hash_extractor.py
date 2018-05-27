import re

VALID_TAGS = ["implement", "test", "document", "testmanual",
              "fix", "chore", "refactor", "pair", "commits"]


def extract_hash(message, tag_specifier="(.[a-zA-Z]+)"):
    valid = []
    invalid = []
    match=re.findall(r"#{}(\[.*\])?".format(tag_specifier),message)
    if match:
        for tag, bracket in match:
            if tag in VALID_TAGS:
                valid.append(tag)
            else:
                invalid.append(tag)

    return valid, invalid

def extract_commit(message):
    match = re.search(r"#commits\[(.*?)\]", message)
    if match:
        return match.group(1)
    else:
        return None

def find_pairs(message):
    match = re.search(r"#pair\[(.*?) ?, ?(.*?)\]", message)
    if match:
        return match.group(1, 2)
    else:
        return None
