import * as Langtrace from '@langtrase/typescript-sdk'


Langtrace.init({ api_key: "YOUR_LANGTRACE_API_KEY" })
import Anthropic from '@anthropic-ai/sdk';

const anthropic = new Anthropic({
  apiKey: "YOUR_ANTHROPIC_API_KEY", 
});

async function main() {
  const message = await anthropic.messages.create({
    max_tokens: 1024,
    messages: [{ role: 'user', content: 'Hello, Claude' }],
    model: 'claude-3-opus-20240229',
  });

  console.log(message.content);
}

main();