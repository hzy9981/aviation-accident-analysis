import pandas as pd
from neo4j import GraphDatabase
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Neo4j Connection Details
URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
USER = os.getenv("NEO4J_USER", "neo4j")
PASSWORD = os.getenv("NEO4J_PASSWORD", "password")

def import_to_neo4j(entities_path, relationships_path):
    # Load data
    entities_df = pd.read_parquet(entities_path)
    relationships_df = pd.read_parquet(relationships_path)

    driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))

    with driver.session() as session:
        # Import Entities
        print("Importing entities...")
        for _, row in entities_df.iterrows():
            session.run("""
                MERGE (e:Entity {id: $id})
                SET e.name = $name, e.type = $type, e.description = $description
            """, id=row['id'], name=row['human_readable_id'], 
                 type=row.get('type', 'Unknown'), description=row.get('description', ''))

        # Import Relationships
        print("Importing relationships...")
        for _, row in relationships_df.iterrows():
            session.run("""
                MATCH (s:Entity {id: $source_id})
                MATCH (t:Entity {id: $target_id})
                MERGE (s)-[r:RELATIONSHIP {type: $type}]->(t)
                SET r.description = $description, r.weight = $weight
            """, source_id=row['source'], target_id=row['target'], 
                 type=row.get('relationship_type', 'RELATED'),
                 description=row.get('description', ''), weight=row.get('weight', 0))

    driver.close()
    print("Import complete.")

if __name__ == "__main__":
    import_to_neo4j("output/entities.parquet", "output/relationships.parquet")
