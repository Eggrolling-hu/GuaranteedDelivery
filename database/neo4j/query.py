
from neo4j import GraphDatabase

uri = "bolt://localhost:7687"
driver = GraphDatabase.driver(uri, auth=("neo4j", "mypassword"))


def print_friends(tx, name):
    result = tx.run("MATCH (a:Person)-[:FRIEND]->(friend) WHERE a.name = $name "
                    "RETURN friend.name ORDER BY friend.name", name=name)
    for record in result:
        print(record["friend.name"])


with driver.session() as session:
    session.read_transaction(print_friends, "Alice")
