import React, { useState } from 'react';

function StreamedResponseComponent() {
  const [responseText, setResponseText] = useState('');

  async function fetchStreamedResponse() {
    const response = await fetch('/api/testv2'); // Replace with your actual API route
    const reader = response!.body!.getReader();
    const decoder = new TextDecoder('utf-8');

    let done = false;
    let fullText = '';

    while (!done) {
      const { value, done: streamDone } = await reader.read();
      done = streamDone;
      if (value) {
        const chunk = decoder.decode(value);
        fullText += chunk;
        setResponseText((prev) => prev + chunk); // Update the UI with each chunk
      }
    }

    // Handle the complete response text here if needed
    console.log('Full Response:', fullText);
  }

  return (
    <div>
      <button onClick={fetchStreamedResponse}>Fetch Streamed Response</button>
      <div>
        <h3>Streamed Response:</h3>
        <pre>{responseText}</pre>
      </div>
    </div>
  );
}

export default StreamedResponseComponent;
