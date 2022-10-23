import ldtab_rs
import sys


def import_demo(path):
    triples = ldtab_rs.import_thick_triples(path)
    for t in triples:
        print(t)


if __name__ == "__main__":
    ontology_path = sys.argv[1]
    import_demo(ontology_path)
