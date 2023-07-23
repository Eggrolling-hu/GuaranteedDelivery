from neo4j import GraphDatabase

uri = "bolt://localhost:7687"
driver = GraphDatabase.driver(uri, auth=("neo4j", "mypassword"))


def create_node(tx, name):
    tx.run("CREATE (n:Person {name: $name})", name=name)


with driver.session() as session:
    session.write_transaction(create_node, "Alice")


def create_friendship(tx, name1, name2):
    tx.run("MERGE (a:Person {name: $name1})"
           "MERGE (b:Person {name: $name2})"
           "MERGE (a)-[:FRIEND]->(b)", name1=name1, name2=name2)


with driver.session() as session:
    session.write_transaction(create_friendship, "Alice", "Bob")


driver.close()
