## This repo demonstrates how to get started with the Langtrace Typescript SDK and Llamaindex

### To get the demo.ts file working you will need to follow the following steps:

*  Install the langtrace typescript sdk ,llamaindex and other neccessary dependencies.
```sh
   npm install @langtrase/typescript-sdk
   npm install llamaindex
   npm install dotenv

```

* Create a .env file and expose your openai api key
```
 OPENAI_API_KEY = "YOUR_OPENAI_API_KEY"
 ```

* Replace the placeholders in the demo.ts file with the actual api keys. For example replace LANGTRACE_API_KEY with your actual langtrace api key which you can generate in your langtrace project dashboard.

* Run ts-node demo.ts in your terminal

```sh
   ts-node demo.ts
```
* Your traces should now be exported to Langtrace. 