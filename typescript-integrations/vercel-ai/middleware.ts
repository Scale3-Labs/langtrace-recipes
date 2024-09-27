// /pages/api/_middleware.js
import { NextResponse } from 'next/server';

export async function middleware(req: any) {
  const { pathname } = req.nextUrl;
 // Add other global middleware logic here
 console.log(`Global middleware applied to ${req.nextUrl.pathname}`);
  // Example: Check if the request is for a protected route
    const token = req.headers.get('Authorization');

    // if (!token) {
    //   return NextResponse.redirect(new URL('/api/auth', req.url));
    // }

    // Validate the token asynchronously (this is just an example, implement your logic)
    const isValid = await validateToken(token);
    // if (!isValid) {
    //   return new NextResponse('Unauthorized', { status: 401 });
    // }

  // Add other middleware logic here
  // For example, logging requests
  console.log(`Request for ${pathname}`);

  // Continue with the request
  return NextResponse.next();
}

async function validateToken(token: any) {
  // Implement your token validation logic here
  // For example, make an asynchronous API call to validate the token
  const response = await fetch('https://jsonplaceholder.typicode.com/todos/1', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    }
  });

  if (!response.ok) {
    return false;
  }

  const data = await response.json();
  return data.isValid;
}
