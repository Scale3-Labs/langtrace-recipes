
import * as Langtrace from '@langtrase/typescript-sdk'


Langtrace.init({ api_key: "YOUR_LANGTRACE_API_KEY" })

import OpenAI from 'openai'

const openai = new OpenAI({
    apiKey: "YOUR_OPENAI_API_KEY" // This is the default and can be omitted
  });
  

async function main() {
    const params: OpenAI.Chat.ChatCompletionCreateParams = {
      messages: [{ role: 'user', content: 'Say this is a test' }],
      model: 'gpt-3.5-turbo',
    }
    await openai.chat.completions.create(params);
  }
  
  main();