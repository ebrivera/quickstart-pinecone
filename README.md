so what i need you to do please is we have functions like this: 
```
{
        "service": "lambda",
        "method": "invoke",
        "description": "Invokes a Lambda function synchronously or asynchronously",
        "code": """import { LambdaClient, InvokeCommand } from "@aws-sdk/client-lambda";

const client = new LambdaClient({});

const command = new InvokeCommand({
  FunctionName: "myFunction",
  Payload: JSON.stringify({ key: "value" }),
  InvocationType: "RequestResponse" // or "Event" for async
});

const response = await client.send(command);
const result = JSON.parse(Buffer.from(response.Payload).toString());""",
        "parameters": {
            "FunctionName": "Name of the Lambda function to invoke",
            "Payload": "JSON payload to send to the function",
            "InvocationType": "RequestResponse (sync) or Event (async)"
        },
        "package": "@aws-sdk/client-lambda"
    },
```
there are loads of them like you can see right after method invoke (ie `create_function` and `list_functions`). I don't expecet you to know what the "new function" is because i don't even know.
ask chat for what the new function would be in aws-sdk3, and then look up that page online, copy the entire page and pass that into chatgpt and say clean it up so it meets the standards of the current.
for that i would pass the old one (the code block copy pasted above is an example of the "old") and then the pasted documentation from online

repeat for all 20 please, and then when you're done:
1) copy and paste my .env that i sent you, save
2) run `python quick_start.py` in your terminal.

if u need help or when ur done lmk
