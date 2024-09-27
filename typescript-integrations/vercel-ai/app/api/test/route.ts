import * as Langtrace from '@langtrase/typescript-sdk'
import * as ai from 'ai'
import { openai } from '@ai-sdk/openai';
import { NextResponse, NextRequest } from 'next/server';

Langtrace.init({ instrumentations: {ai: ai}, api_key: process.env.LANGTRACE_API_KEY, disable_latest_version_check: true})
export async function GET(req: NextRequest) {
  try {
    const res = await ai.streamText({
      model: openai('gpt-4-turbo', { user: 'TestUserId' }),
      system: 'You are a friendly assistant!',
      temperature: 0,
      topP: 1,
      maxRetries: 3,
      maxTokens: 1024,
      messages: [{ role: 'system', content: 'You are a friendly assistant' }, { role: 'user', content: 'How are you' }]
    });
    const encoder = new TextEncoder();
    const stream = new ReadableStream({
      async start(controller) {
        for await (const message of res.textStream) {
          controller.enqueue(encoder.encode(`${message}\n`));
        }
        controller.close();
      },
      cancel() {
        console.log('Stream canceled');
      }
    });

    return new NextResponse(stream, {
      headers: { 'Content-Type': 'text/plain' },
    });
  } catch (err: any) {
    console.log(err);
    return NextResponse.json({
      error: err.message,
    });
  }
}
