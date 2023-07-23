import weaviate


client = weaviate.Client(
    url="http://localhost:8080",  # Replace with your endpoint
    auth_client_secret=weaviate.AuthApiKey(api_key="shadowmotion-secret-key"))


try:
    client.schema.delete_class("LangChain")
except:
    print("LangChain class hasn't been created.")
