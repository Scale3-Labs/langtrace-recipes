import * as Langtrace from '@langtrase/typescript-sdk'


Langtrace.init({ api_key: "YOUR_LANGTRACE_API_KEY" })

import { Pinecone } from '@pinecone-database/pinecone'

async function main() {
    const pc = new Pinecone({
        apiKey: "YOUR_PINECONE_API_KEY"
      });


      await pc.createIndex({
        name: 'sample-index',
        dimension: 8,
        spec: {
          serverless: {
            cloud: 'aws',
            region: 'us-east-1',
          },
        },
        suppressConflicts: true
      })


      const index = await pc.Index("sample-index")

      const vectors = [
        {"id": "A", "values": [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]},
        {"id": "B", "values": [0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2]},
        {"id": "C", "values": [0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3]},
        {"id": "D", "values": [0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4]}
      ]

      await index.upsert(vectors)    }
main();