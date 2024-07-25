import * as Langtrace from '@langtrase/typescript-sdk'


Langtrace.init({ api_key: "YOUR_LANGTRACE_API_KEY" })
import OpenAI from 'openai'

const openai = new OpenAI({
    apiKey:"YOUR_PPLX_API_KEY",
    baseURL: "https://api.perplexity.ai" 
  });
  

async function main() {
    const params: OpenAI.Chat.ChatCompletionCreateParams = {
      messages: [{ role: 'user', content: 'Say this is a test' }],
      model: 'mistral-7b-instruct',
    };
    const chatCompletion: OpenAI.Chat.ChatCompletion = await openai.chat.completions.create(params);
  }
  
  main();