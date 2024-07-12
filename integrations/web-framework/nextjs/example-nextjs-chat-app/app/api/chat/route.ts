import { NextResponse } from 'next/server';
import * as Langtrace from '@langtrase/typescript-sdk'
import * as openai from 'openai';

import OpenAI from "openai";

Langtrace.init({
  instrumentations: {openai: openai},
  api_key: process.env.LANGTRACE_API_KEY as string
})

const openAi = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY as string,
});

export async function POST(req: Request) {
  const { message } = await req.json();

  if (!message) {
    return NextResponse.json({ error: 'Message is required' }, { status: 400 });
  }

  try {
    const response = await openAi.chat.completions.create({
      model: process.env.OPENAI_MODEL as string,
      messages: [{ role: 'system', content: 'You are a helpful assistant.' }, { role: 'user', content: message }],
    })

    const reply = response.choices[0].message.content;
    return NextResponse.json(reply);
  } catch (error) {
    console.error('Error fetching OpenAI API:', error);
    return NextResponse.json({ error: 'Error fetching OpenAI API' }, { status: 500 });
  }
}
