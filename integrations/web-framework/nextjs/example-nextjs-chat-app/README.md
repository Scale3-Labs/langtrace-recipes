## Getting Started

To get started with this project, follow these steps:

### Clone the Repository

```bash
git clone https://github.com/obinnascale3/nextjs-chat-app
cd nextjs-chat-app
```

### Install Dependencies

Make sure you have [Node.js](https://nodejs.org/) installed. Then, install the project dependencies:

```bash
npm install
```

### Set up environment variables

This project uses OpenAI so you'll need an OpenAI API key. You'll need to add your Langtrace API key as well ([Sign up](https://langtrace.ai/signup) to Langtrace if you don't have an account). You can also change the model to gtp-4 if your API key has access.

```bash
OPENAI_API_KEY=
OPENAI_MODEL=gpt-3.5-turbo
LANGTRACE_API_KEY=
```

### Run the Application

Run the development server:

```bash
npm run dev
```

### Try out the Application

Open your browser and go to [http://localhost:3000](http://localhost:3000) to view the app. Send a message, wait for a reply then go to your Langtrace dashboard to start viewing traces and other metrics.
