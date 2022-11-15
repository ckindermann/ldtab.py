import ldtab_rs
import json
import sqlite3
import sys


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def import_demo(path):
    triples = ldtab_rs.import_thick_triples(path)

    for t in triples:
        print(t)


def encode_string(input):
    if isinstance(input, str):
        return input
    else:
        if input == {}:
            return None
        else:
            return json.dumps(input)


def import_to_database(ontology_path, database_con):
    triples = ldtab_rs.import_thick_triples(ontology_path)
    cur = database_con.cursor()
    for t in triples:

        json_triple = json.loads(t)

        assertion = int(json_triple["assertion"])
        retraction = int(json_triple["retraction"])
        graph = encode_string(json_triple["graph"])
        subject = encode_string(json_triple["subject"])
        predicate = encode_string(json_triple["predicate"])
        object = encode_string(json_triple["object"])
        datatype = encode_string(json_triple["datatype"])
        annotation = encode_string(json_triple["annotation"])

        params = (
            assertion,
            retraction,
            graph,
            subject,
            predicate,
            object,
            datatype,
            annotation,
        )

        query = f"Insert INTO statement VALUES (?,?,?,?,?,?,?,?)"

        cur.execute(query, params)

    database_con.commit()


# TODO: init, export, prefix

if __name__ == "__main__":
    ontology_path = sys.argv[1]
    database = sys.argv[2]
    con = sqlite3.connect(database, check_same_thread=False)
    con.row_factory = dict_factory
    # import_demo(ontology_path)
    import_to_database(ontology_path, con)
