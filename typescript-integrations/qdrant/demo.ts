// Must precede any llm module imports

import * as Langtrace from '@langtrase/typescript-sdk'


Langtrace.init({ api_key: "YOUR_LANGTRACE_API_KEY" })
import {QdrantClient} from '@qdrant/js-client-rest';

const collection_name = "my_collection" //Define the name of the Qdrant collection to be created. Feel free to change this to your preferred name.
async function main(){
    

    const client = new QdrantClient({
        url: 'YOUR_QDRANT_URL',
        apiKey: 'YOUR_QDRANT_API_KEY',
    });

    const response = await client.getCollections();

    const collectionNames = response.collections.map((collection) => collection.name);

    // if your collection name is not defined then create a new collection
    if (collectionNames.includes(collection_name) == false) {
      
        await client.createCollection(collection_name, {
            vectors: {
                size: 4,
                distance: 'Cosine',
            },
            optimizers_config: {
                default_segment_number: 2,
            },
            replication_factor: 2,
        });
    }


    await client.upsert(collection_name, {
        wait: true,
        points: [
            {
                id: 1,
                vector: [0.05, 0.61, 0.76, 0.74],
                payload: {
                    city: 'Berlin',
                    country: 'Germany',
                    count: 1000000,
                    square: 12.5,
                    coords: {lat: 1.0, lon: 2.0},
                },
            },
            {id: 2, vector: [0.19, 0.81, 0.75, 0.11], payload: {city: ['Berlin', 'London']}},
            {id: 3, vector: [0.36, 0.55, 0.47, 0.94], payload: {city: ['Berlin', 'Moscow']}},
            {id: 4, vector: [0.18, 0.01, 0.85, 0.8], payload: {city: ['London', 'Moscow']}},
        ],
    });
    
    const search_result = await client.search(collection_name,{vector:[0.2, 0.1, 0.9, 0.7], limit:3 })

    console.log(search_result)
}


main();