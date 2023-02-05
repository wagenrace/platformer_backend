import os

from environs import Env
from py2neo import Graph

env = Env()
env.read_env(".env")

neo4j_url = os.environ.get("neo4jUrl")
user = os.environ.get("user")
pswd = os.environ.get("pswd")

graph = Graph(neo4j_url, auth=(user, pswd))

graph.run(
    """
    MERGE (l1:Level {number: 1}) 
    SET l1.name = "Level 1"
    SET l1.encode_level = "8abcdef9FEDCBA+"
    MERGE (l2:Level {number: 2}) 
    SET l2.name = "Level 2"
    SET l2.encode_level = "8012345679FFfdAe+"
    MERGE (l3:Level {number: 3}) 
    SET l3.name = "Level 3"
    SET l3.encode_level = "8021ABCe9D02daDD+"
    MERGE (l4:Level {number: 4}) 
    SET l4.name = "Level 4"
    SET l4.encode_level = "8aaaaaaa9ffffff+"
    
    MERGE (l1)-[:RED_DOOR]->(l3)
    MERGE (l4)-[:RED_DOOR]->(l2)

    MERGE (l1)-[:BLUE_DOOR]->(l4)
    MERGE (l2)-[:BLUE_DOOR]->(l3)

    MERGE (l1)-[:GREEN_DOOR]->(l2)
    MERGE (l3)-[:GREEN_DOOR]->(l4)
"""
)

graph.run(
    """
    CREATE POINT INDEX node_index_name IF NOT EXISTS FOR (n:Level) ON (n.number)
"""
)
