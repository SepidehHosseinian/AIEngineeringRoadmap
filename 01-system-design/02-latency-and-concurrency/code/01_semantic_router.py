import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_core.utils.embedding import compute_similarity

load_dotenv()

class SemanticRouter:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings()
        
        self.routes = {
            "banking_query": "Information about interest rates, loans, credit cards, and bank accounts.",
            "general_query": "General knowledge, weather, news, and everyday conversation."
        }
       
        self.route_embeddings = {
            name: self.embeddings.embed_query(description) 
            for name, description in self.routes.items()
        }

    def route(self, user_query):
        query_embedding = self.embeddings.embed_query(user_query)
        
       
        scores = {}
        for route_name, route_emb in self.route_embeddings.items():
           
            score = compute_similarity(query_embedding, route_emb)
            scores[route_name] = score
        
     
        best_route = max(scores, key=scores.get)
        return best_route, scores[best_route]


if __name__ == "__main__":
    router = SemanticRouter()
    
    test_queries = [
        "What is the current interest rate for a housing loan?",
        "How is the weather in Tehran today?"
    ]
    
    for q in test_queries:
        route, score = router.route(q)
        print(f"Query: '{q}'\nDetected Route: {route} (Score: {score:.4f})\n")