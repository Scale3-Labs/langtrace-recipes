import * as Langtrace from '@langtrase/typescript-sdk'

Langtrace.init({ api_key: "YOUR_LANGTRACE_API_KEY" })

import ollama from 'ollama'
main();
async function main() {
    const response = await ollama.chat({
        model: 'llama2',
        messages: [{ role: 'user', content: 'Why is the sky blue?' }],
      })
      console.log(response.message.content)
}
