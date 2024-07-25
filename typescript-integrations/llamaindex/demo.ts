import * as Langtrace from '@langtrase/typescript-sdk'


Langtrace.init({ api_key: "LANGTRACE_API_KEY" })
import { SimpleDirectoryReader, VectorStoreIndex} from "llamaindex";
import dotenv from 'dotenv';

// Load environment variables from .env file
dotenv.config();

async function main() {
  // Load essay from abramov.txt in Node


  // Read documents from assets folder
  const reader = new SimpleDirectoryReader();
  const documents = await reader.loadData("./assets");
  


  // Split text and create embeddings. Store them in a VectorStoreIndex
  const index = await VectorStoreIndex.fromDocuments(documents);

  // Query the index
  const queryEngine = index.asQueryEngine();
  const response = await queryEngine.query({
    query: "What is the offside rule?",
  });

  // Output response
  console.log(response.toString());
}

main();