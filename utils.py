

def slugify(value: str) -> str:
    words = value.split()
    slug = "-".join([word.lower() for word in words])
    return slug
