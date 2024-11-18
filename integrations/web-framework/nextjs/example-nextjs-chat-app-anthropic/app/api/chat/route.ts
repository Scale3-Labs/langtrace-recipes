import { NextResponse } from 'next/server';
import * as Langtrace from '@langtrase/typescript-sdk'
import { createAnthropic } from '@ai-sdk/anthropic';
// import { openai } from '@ai-sdk/openai';
import * as ai from 'ai';

Langtrace.init({
  instrumentations: { ai },
  api_key: process.env.LANGTRACE_API_KEY as string
})

const anthropicClient = createAnthropic({
  apiKey: process.env.ANTHROPIC_API_KEY as string,
});

const model = anthropicClient('claude-3-5-sonnet-20241022');
// const model = openai('gpt-4o-mini');

export async function POST(req: Request) {
  const { message } = await req.json();

  if (!message) {
    return NextResponse.json({ error: 'Message is required' }, { status: 400 });
  }

  try {
    const response = await ai.generateText({
      model,
      messages: [{ role: 'system', content: 'You are a helpful assistant.' }, { role: 'user', content: message }],
    })

    const reply = response.text;
    return NextResponse.json(reply);
  } catch (error) {
    console.error('Error fetching OpenAI API:', error);
    return NextResponse.json({ error: 'Error fetching OpenAI API' }, { status: 500 });
  }
}
