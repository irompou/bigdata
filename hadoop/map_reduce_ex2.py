
def map(p, r):
    if r.reputation > 800:
        r2 = (r.reputation, r.views, r.displayname)
        collect(r.displayname, r2)


def reduce(n, r2):
    s = sum(r.reputation for r in r2)
    avg = float(sum(r.views for r in r2) / len(r2))
    r2 = (r.displayname, sum, avg)
    store(n, r2)
