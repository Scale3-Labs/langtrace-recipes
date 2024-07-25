
import * as Langtrace from '@langtrase/typescript-sdk'


Langtrace.init({ api_key: "YOUR_LANGTRACE_API_KEY" })
import {CohereClient} from "cohere-ai"

const cohere = new CohereClient({
    token: "YOUR_COHERE_TOKEN",
});
async function main() {
    const chat = await cohere.chat({
        model: "command",
        message: "What is LangChain?",
    });
    
    console.log(chat);
}

main();
