
def map(p, r):
    if r.age > 30:
        r2 = (r.displayname, r.age)
        collect (p, r2)


def map(p1, r3):
    if r3.upvotes < 20:
        r4 = (r.displayname, r.upvotes)
        collect(p, r4)
