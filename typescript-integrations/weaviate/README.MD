## This repo demonstrates how to get started with the Langtrace Typescript SDK and Weaviate

### To get the demo.ts file working you will need to follow the following steps:

*  Install the langtrace typescript sdk and weaviate.
```sh
   npm install @langtrase/typescript-sdk
   npm install weviate-ts-client
```

* Replace the placeholders in the demo.ts file with the actual api keys. For example replace LANGTRACE_API_KEY with your actual langtrace api key which you can generate in your langtrace project dashboard. Note that you will also need a weaviate host endpoint, weaviate api key and open ai api key.

* Run ts-node demo.ts in your terminal

```sh
   ts-node demo.ts
```
* Your traces should now be exported to Langtrace. Make sure to look through the demo.ts file to for a better understanding