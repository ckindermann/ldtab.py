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


def init(database_con):

    # 1. create ldtab table
    cur = database_con.cursor()
    query = "CREATE TABLE IF NOT EXISTS ldtab (key TEXT PRIMARY KEY, value TEXT )"
    cur.execute(query)

    query = f"Insert INTO ldtab VALUES (?,?)"
    cur.execute(query, ("ldtab version", "0.0.1"))
    cur.execute(query, ("schema version", "0"))

    # 2. create prefix table
    query = "CREATE TABLE IF NOT EXISTS prefix (prefix TEXT PRIMARY KEY, base TEXT NOT NULL )"
    cur.execute(query)

    # 3. create statement table
    query = "CREATE TABLE IF NOT EXISTS statement (assertion int NOT NULL, retraction int NOT NULL DEFAULT 0, graph TEXT NOT NULL, subject TEXT NOT NULL, predicate TEXT NOT NULL, object TEXT NOT NULL, datatype TEXT NOT NULL, annotation TEXT )"
    cur.execute(query)

    database_con.commit()


def prefix(prefix_path, database_con):
    cur = database_con.cursor()

    file = open(prefix_path, "r")
    next(file)  # skip header
    for line in file:
        cols = line.split("\t")
        prefix = cols[0]
        base = cols[1].rstrip()  # TODO: trimming whitespace here feels wrong
        print(base)
        query = f"Insert INTO prefix VALUES (?,?)"
        cur.execute(query, (prefix, base))

    database_con.commit()


# TODO: export

if __name__ == "__main__":
    ontology_path = sys.argv[1]
    database = sys.argv[2]
    con = sqlite3.connect(database, check_same_thread=False)
    con.row_factory = dict_factory

    prefix(ontology_path, con)

    # init(con)

    # import_demo(ontology_path)
    # import_to_database(ontology_path, con)
