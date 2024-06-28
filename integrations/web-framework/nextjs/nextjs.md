
## Steps

Follow the steps below to integrate Langtrace with your NextJS application:

<Note>
  Langtrace can be initialized only in the server-side code of NextJS
  applications. This includes `app/api/` pages for app router and `pages/api/`
  for pages router. You can also initialize Langtrace in server side rendered
  pages.
</Note>

- Update the next.config.(m)js file to include opentelemetry:

```js
const nextConfig = {
  webpack: (config, { isServer }) => {
    config.module.rules.push({
      test: /\.node$/,
      loader: "node-loader",
    });
    if (isServer) {
      config.ignoreWarnings = [{ module: /opentelemetry/ }];
    }
    return config;
  },
};
module.exports = nextConfig;
```

- Install the Langtrace SDK and initialize it in your APIs:

```typescript Typescript
import * as Langtrace from "@langtrase/typescript-sdk"; // Ensure this import precedes any LLM module imports

/**
 * Ensure you have OPENAI_API_KEY in your environment variables and LANGTRACE_API_KEY in your environment variables
 */
Langtrace.init({
  api_key: "<LANGTRACE_API_KEY>",
  instrumentations: {
    openai: OpenAI,
    // other llm instrumentations
  },
});
```

Frameworks that call other instrumentations need to be manually instrumented. Lamaindex example below

```typescript Typescript
Langtrace.init({
  api_key: "<LANGTRACE_API_KEY>",
  instrumentations: {
    llamaindex: llamaindex,
    openai: openai.OpenAI,
  },
});
```

## Examples for different LLMs, VectorDBs and Frameworks

- **Anthropic**:

```typescript Typescript
import * as Langtrace from "@langtrase/typescript-sdk";
import * as anthropic from "@anthropic-ai/sdk";
/**
 * Ensure you have ANTHROPIC_API_KEY in your environment variables and LANGTRACE_API_KEY in your environment variables
 */
Langtrace.init({
  instrumentations: {
    anthropic: anthropic,
  },
});
```

- **OpenAI**:

```typescript Typescript
import * as Langtrace from "@langtrase/typescript-sdk";
import * as openai from "openai";
/**
 * Ensure you have OPENAI_API_KEY in your environment variables and LANGTRACE_API_KEY in your environment variables
 */
Langtrace.init({
  instrumentations: {
    openai: openai,
  },
});
```

- **Llamaindex**:

```typescript Typescript
import * as Langtrace from "@langtrase/typescript-sdk";
import * as llamaindex from "llamaindex";
import * as openai from "openai";
/**
 * Ensure you have OPENAI_API_KEY in your environment variables and LANGTRACE_API_KEY in your environment variables
 */
Langtrace.init({
  instrumentations: {
    llamaindex: llamaindex,
    openai: openai,
  },
});
```

- **Pinecone**:

```typescript Typescript
import * as Langtrace from "@langtrase/typescript-sdk";
import * as pinecone from "@pinecone-database/pinecone";
import * as openai from "openai";

/**
 * Ensure you have PINECONE_API_KEY in your environment variables and LANGTRACE_API_KEY in your environment variables
 */
Langtrace.init({
  instrumentations: {
    pinecone: pinecone,
    openai: openai,
  },
});
```

- **ChromaDB**:

```typescript Typescript
import * as Langtrace from "@langtrase/typescript-sdk";
import * as chroma from "chromadb";
import * as openai from "openai";
/**
 * Ensure you have installed chromadb
 * Make sure you have pipx installed.
 * python3 -m venv ./app/api/chroma/chromaenv
 * source ./app/api/chroma/chromaenv/bin/activate
 * pipx install chromadb
 * chroma run --path ./app/api/chroma/db
 * Ensure you have OPENAI_API_KEY in your environment variables and LANGTRACE_API_KEY in your environment variables
 */
Langtrace.init({
  instrumentations: {
    openai: openai,
    chromadb: chroma,
  },
});
```
