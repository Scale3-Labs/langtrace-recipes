// Must precede any llm module imports

import * as Langtrace from '@langtrase/typescript-sdk'


Langtrace.init({  api_key:  "YOUR_LANGTRACE_API_KEY"})
import weaviate, { WeaviateClient, ObjectsBatcher, ApiKey } from 'weaviate-ts-client';
import fetch from 'node-fetch';

const client: WeaviateClient = weaviate.client({
  scheme: 'https',
  host: 'YOUR_WEAVIATE_HOST_ENDPOINT',  // Replace with your Weaviate endpoint
  apiKey: new ApiKey("YOUR_WEAVIATE_API_KEY"), 
  headers: { 'X-OpenAI-Api-Key': "YOUR_OPENAI_API_KEY" }
  // Replace with your Weaviate instance API key
});

const className:string = "Jeopardy"

async function getJsonData() {
  const file = await fetch('https://raw.githubusercontent.com/weaviate-tutorials/quickstart/main/data/jeopardy_tiny.json');
  return file.json();
}


async function importQuestions() {
  // Get the questions directly from the URL
  const data = await getJsonData();

  // Prepare a batcher
  let batcher: ObjectsBatcher = client.batch.objectsBatcher();
  let counter = 0;
  const batchSize = 100;

  for (const question of data) {
    // Construct an object with a class and properties 'answer' and 'question'
    const obj = {
      class: className,
      properties: {
        answer: question.Answer,
        question: question.Question,
        category: question.Category,
      },
    };

    // add the object to the batch queue
    batcher = batcher.withObject(obj);

    // When the batch counter reaches batchSize, push the objects to Weaviate
    if (counter++ == batchSize) {
      // flush the batch queue
      const res = await batcher.do();
      console.log(res);

      // restart the batch queue
      counter = 0;
      batcher = client.batch.objectsBatcher();
    }
  }

  // Flush the remaining objects
  const res = await batcher.do();
  console.log(res);
}


async function classExists(className: string): Promise<boolean> {
  try {
    const schema = await client.schema.getter().do();
    console.log(schema)
    console.log(schema.classes!.some((cls: any) => cls.class === className));
    return schema.classes!.some((cls: any) => cls.class === className);
  } catch (error) {
    console.log("Error fetching schema:", error);
    return false;
  }
}

async function createCollection() {
  // Define collection configuration - vectorizer, generative module and data schema
  const classObj = {
      'class': className,
      'vectorizer': 'text2vec-openai',  // If set to "none" you must always provide vectors yourself. Could be any other "text2vec-*" also.
      'moduleConfig': {
        'text2vec-openai': {},
        'generative-openai': {}  // Ensure the `generative-openai` module is used for generative queries
      },
    };
    
    async function addSchema() {
      const res = await client.schema.classCreator().withClass(classObj).do();
     
    }

    //check if the className exists, it it doesnt create the collection and import objects.
    if (await classExists(className) == false ) {
      await addSchema();
      await importQuestions();
    }
    
   
}

async function main() {
   
      await createCollection()

      const res = await client.graphql
      .get()
      .withClassName(className)
      .withFields('question answer category')
      .withNearText({concepts: ['biology']})
      .withLimit(2)
      .do();
  
    console.log(JSON.stringify(res, null, 2));
  
    }
  
  main();




