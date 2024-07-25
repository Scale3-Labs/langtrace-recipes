import * as Langtrace from '@langtrase/typescript-sdk'


Langtrace.init({ api_key: "YOUR_LANGTRACE_API_KEY" })
import { ChromaClient } from 'chromadb'
const client = new ChromaClient();
const collection_name = "my_collection"

async function main() {
  await client.createCollection({
    name: collection_name,
  });

  let collection = await client.getCollection({
    name: collection_name,
  });

  collection.add({documents: ["This is document1", "This is document2"],
  metadatas: [{ "source": "notion" }, { "source": "google-docs" }],
  ids: ["doc1", "doc2"],})
}

main();