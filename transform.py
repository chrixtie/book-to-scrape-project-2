import re

def sanitize_title(title):
    title = title.lower()
    title = re.sub(r"[^a-z0-9\s]", "", title)
    title = title.replace(" ", "_")
    return title
