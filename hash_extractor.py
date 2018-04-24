import re

VALID_TAGS=["#implement","#test","#document","#testmanual","#fix","#chore","#refactor","#pair","#commits"]
def extract_hash(message,tag_specifier=""):
    valid=[]
    invalid=[]
    for i in message.split():
        if i.startswith("#{}".format(tag_specifier)):
            tag=re.sub('\[.*\]','',i)
            if tag in VALID_TAGS:
                valid.append(tag)
            else:
                invalid.append(tag)

    return valid, invalid
