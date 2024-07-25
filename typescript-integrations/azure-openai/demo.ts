import * as Langtrace from '@langtrase/typescript-sdk'


Langtrace.init({ api_key: "YOUR_LANGTRACE_API_KEY" })

import { AzureOpenAI } from 'openai'
import OpenAI from 'openai';

const openai = new AzureOpenAI({
    apiKey: "YOUR_AZURE_API_KEY",
    apiVersion: "AZURE_API_VERSION",
    endpoint: "AZURE_ENDPOINT_URL",
    deployment: "DEPLOYMENT_NAME"
  });


  async function main() {
    const params: OpenAI.Chat.ChatCompletionCreateParams = {
      messages: [{ role: 'user', content: 'Say this is a test' }],
      model: 'gpt-3.5-turbo',
    }
    await openai.chat.completions.create(params);
  }

  main();