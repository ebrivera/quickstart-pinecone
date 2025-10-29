"""
AWS SDK v3 Quick Start - FIXED VERSION
Properly embeds code examples and parameters for RAG retrieval
"""

import os
import json
from openai import OpenAI
from pinecone import Pinecone, ServerlessSpec
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()

# Initialize clients
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

# Configuration
INDEX_NAME = "aws-sdk-v3-quickstart"
EMBEDDING_MODEL = "text-embedding-3-small"
DIMENSION = 1536

# ============================================================================
# ESSENTIAL AWS SDK v3 METHODS (20 Most Common)
# ============================================================================

ESSENTIAL_METHODS = [
    # LAMBDA - 5 methods
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
    {
        "service": "lambda",
        "method": "create_function",
        "description": "Creates a new Lambda function",
        "code": """import { LambdaClient, CreateFunctionCommand } from "@aws-sdk/client-lambda";
import { readFileSync } from "fs";

const client = new LambdaClient({});

const code = readFileSync("./function.zip");

const command = new CreateFunctionCommand({
  FunctionName: "myFunction",
  Runtime: "nodejs20.x",
  Role: "arn:aws:iam::123456789012:role/lambda-role",
  Handler: "index.handler",
  Code: { ZipFile: code }
});

await client.send(command);""",
        "parameters": {
            "FunctionName": "Name for the new function",
            "Runtime": "Runtime environment (nodejs20.x, python3.12, etc)",
            "Role": "ARN of the execution role",
            "Handler": "Entry point for the function",
            "Code": "Function code as ZipFile or S3 location"
        },
        "package": "@aws-sdk/client-lambda"
    },
    {
        "service": "lambda",
        "method": "list_functions",
        "description": "Lists Lambda functions in your account",
        "code": """import { LambdaClient, ListFunctionsCommand } from "@aws-sdk/client-lambda";

const client = new LambdaClient({});

const command = new ListFunctionsCommand({});
const response = await client.send(command);

response.Functions.forEach(func => {
  console.log(func.FunctionName);
});""",
        "parameters": {},
        "package": "@aws-sdk/client-lambda"
    },
    {
        "service": "lambda",
        "method": "update_function_code",
        "description": "Updates Lambda function code",
        "code": """import { LambdaClient, UpdateFunctionCodeCommand } from "@aws-sdk/client-lambda";
import { readFileSync } from "fs";

const client = new LambdaClient({});
const code = readFileSync("./new-function.zip");

const command = new UpdateFunctionCodeCommand({
  FunctionName: "myFunction",
  ZipFile: code
});

await client.send(command);""",
        "parameters": {
            "FunctionName": "Name of function to update",
            "ZipFile": "New function code as zip"
        },
        "package": "@aws-sdk/client-lambda"
    },
    {
        "service": "lambda",
        "method": "delete_function",
        "description": "Deletes a Lambda function",
        "code": """import { LambdaClient, DeleteFunctionCommand } from "@aws-sdk/client-lambda";

const client = new LambdaClient({});

const command = new DeleteFunctionCommand({
  FunctionName: "myFunction"
});

await client.send(command);""",
        "parameters": {
            "FunctionName": "Name of function to delete"
        },
        "package": "@aws-sdk/client-lambda"
    },
    
    # DYNAMODB - 8 methods
    {
        "service": "dynamodb",
        "method": "put_item",
        "description": "Adds a new item to a DynamoDB table",
        "code": """import { DynamoDBClient } from "@aws-sdk/client-dynamodb";
import { PutCommand, DynamoDBDocumentClient } from "@aws-sdk/lib-dynamodb";

const client = new DynamoDBClient({});
const docClient = DynamoDBDocumentClient.from(client);

const command = new PutCommand({
  TableName: "Users",
  Item: {
    userId: "123",
    name: "John Doe",
    email: "john@example.com"
  }
});

await docClient.send(command);""",
        "parameters": {
            "TableName": "Name of the DynamoDB table",
            "Item": "Object with attributes to store"
        },
        "package": "@aws-sdk/lib-dynamodb"
    },
    {
        "service": "dynamodb",
        "method": "get_item",
        "description": "Retrieves an item from a DynamoDB table",
        "code": """import { DynamoDBClient } from "@aws-sdk/client-dynamodb";
import { GetCommand, DynamoDBDocumentClient } from "@aws-sdk/lib-dynamodb";

const client = new DynamoDBClient({});
const docClient = DynamoDBDocumentClient.from(client);

const command = new GetCommand({
  TableName: "Users",
  Key: {
    userId: "123"
  }
});

const response = await docClient.send(command);
console.log(response.Item);""",
        "parameters": {
            "TableName": "Name of the table",
            "Key": "Primary key of the item to retrieve"
        },
        "package": "@aws-sdk/lib-dynamodb"
    },
    {
        "service": "dynamodb",
        "method": "update_item",
        "description": "Updates an existing item in DynamoDB",
        "code": """import { DynamoDBClient } from "@aws-sdk/client-dynamodb";
import { UpdateCommand, DynamoDBDocumentClient } from "@aws-sdk/lib-dynamodb";

const client = new DynamoDBClient({});
const docClient = DynamoDBDocumentClient.from(client);

const command = new UpdateCommand({
  TableName: "Users",
  Key: { userId: "123" },
  UpdateExpression: "set #name = :name, email = :email",
  ExpressionAttributeNames: { "#name": "name" },
  ExpressionAttributeValues: {
    ":name": "Jane Doe",
    ":email": "jane@example.com"
  }
});

await docClient.send(command);""",
        "parameters": {
            "TableName": "Name of the table",
            "Key": "Primary key of item to update",
            "UpdateExpression": "Expression defining the update"
        },
        "package": "@aws-sdk/lib-dynamodb"
    },
    {
        "service": "dynamodb",
        "method": "delete_item",
        "description": "Deletes an item from DynamoDB",
        "code": """import { DynamoDBClient } from "@aws-sdk/client-dynamodb";
import { DeleteCommand, DynamoDBDocumentClient } from "@aws-sdk/lib-dynamodb";

const client = new DynamoDBClient({});
const docClient = DynamoDBDocumentClient.from(client);

const command = new DeleteCommand({
  TableName: "Users",
  Key: { userId: "123" }
});

await docClient.send(command);""",
        "parameters": {
            "TableName": "Name of the table",
            "Key": "Primary key of item to delete"
        },
        "package": "@aws-sdk/lib-dynamodb"
    },
    {
        "service": "dynamodb",
        "method": "query",
        "description": "Queries items in a DynamoDB table",
        "code": """import { DynamoDBClient } from "@aws-sdk/client-dynamodb";
import { QueryCommand, DynamoDBDocumentClient } from "@aws-sdk/lib-dynamodb";

const client = new DynamoDBClient({});
const docClient = DynamoDBDocumentClient.from(client);

const command = new QueryCommand({
  TableName: "Users",
  KeyConditionExpression: "userId = :userId",
  ExpressionAttributeValues: {
    ":userId": "123"
  }
});

const response = await docClient.send(command);
console.log(response.Items);""",
        "parameters": {
            "TableName": "Name of the table",
            "KeyConditionExpression": "Query condition",
            "ExpressionAttributeValues": "Values for the expression"
        },
        "package": "@aws-sdk/lib-dynamodb"
    },
    {
        "service": "dynamodb",
        "method": "scan",
        "description": "Scans all items in a DynamoDB table",
        "code": """import { DynamoDBClient } from "@aws-sdk/client-dynamodb";
import { ScanCommand, DynamoDBDocumentClient } from "@aws-sdk/lib-dynamodb";

const client = new DynamoDBClient({});
const docClient = DynamoDBDocumentClient.from(client);

const command = new ScanCommand({
  TableName: "Users",
  FilterExpression: "age > :age",
  ExpressionAttributeValues: {
    ":age": 18
  }
});

const response = await docClient.send(command);
console.log(response.Items);""",
        "parameters": {
            "TableName": "Name of the table",
            "FilterExpression": "Optional filter condition"
        },
        "package": "@aws-sdk/lib-dynamodb"
    },
    {
        "service": "dynamodb",
        "method": "batch_write",
        "description": "Writes multiple items to DynamoDB in batch",
        "code": """import { DynamoDBClient } from "@aws-sdk/client-dynamodb";
import { BatchWriteCommand, DynamoDBDocumentClient } from "@aws-sdk/lib-dynamodb";

const client = new DynamoDBClient({});
const docClient = DynamoDBDocumentClient.from(client);

const command = new BatchWriteCommand({
  RequestItems: {
    "Users": [
      {
        PutRequest: {
          Item: { userId: "1", name: "Alice" }
        }
      },
      {
        PutRequest: {
          Item: { userId: "2", name: "Bob" }
        }
      }
    ]
  }
});

await docClient.send(command);""",
        "parameters": {
            "RequestItems": "Map of table names to write requests"
        },
        "package": "@aws-sdk/lib-dynamodb"
    },
    {
        "service": "dynamodb",
        "method": "create_table",
        "description": "Creates a new DynamoDB table",
        "code": """import { DynamoDBClient, CreateTableCommand } from "@aws-sdk/client-dynamodb";

const client = new DynamoDBClient({});

const command = new CreateTableCommand({
  TableName: "Users",
  KeySchema: [
    { AttributeName: "userId", KeyType: "HASH" }
  ],
  AttributeDefinitions: [
    { AttributeName: "userId", AttributeType: "S" }
  ],
  BillingMode: "PAY_PER_REQUEST"
});

await client.send(command);""",
        "parameters": {
            "TableName": "Name for the new table",
            "KeySchema": "Primary key definition",
            "AttributeDefinitions": "Attribute types",
            "BillingMode": "PAY_PER_REQUEST or PROVISIONED"
        },
        "package": "@aws-sdk/client-dynamodb"
    },
    
    # S3 - 7 methods
    {
        "service": "s3",
        "method": "put_object",
        "description": "Uploads an object to S3",
        "code": """import { S3Client, PutObjectCommand } from "@aws-sdk/client-s3";

const client = new S3Client({});

const command = new PutObjectCommand({
  Bucket: "my-bucket",
  Key: "path/to/file.txt",
  Body: "Hello World",
  ContentType: "text/plain"
});

await client.send(command);""",
        "parameters": {
            "Bucket": "Name of the S3 bucket",
            "Key": "Object key (file path)",
            "Body": "File content (string, Buffer, or Stream)",
            "ContentType": "MIME type of the object"
        },
        "package": "@aws-sdk/client-s3"
    },
    {
        "service": "s3",
        "method": "get_object",
        "description": "Downloads an object from S3",
        "code": """import { S3Client, GetObjectCommand } from "@aws-sdk/client-s3";

const client = new S3Client({});

const command = new GetObjectCommand({
  Bucket: "my-bucket",
  Key: "path/to/file.txt"
});

const response = await client.send(command);
const bodyString = await response.Body.transformToString();
console.log(bodyString);""",
        "parameters": {
            "Bucket": "Name of the S3 bucket",
            "Key": "Object key to retrieve"
        },
        "package": "@aws-sdk/client-s3"
    },
    {
        "service": "s3",
        "method": "delete_object",
        "description": "Deletes an object from S3",
        "code": """import { S3Client, DeleteObjectCommand } from "@aws-sdk/client-s3";

const client = new S3Client({});

const command = new DeleteObjectCommand({
  Bucket: "my-bucket",
  Key: "path/to/file.txt"
});

await client.send(command);""",
        "parameters": {
            "Bucket": "Name of the S3 bucket",
            "Key": "Object key to delete"
        },
        "package": "@aws-sdk/client-s3"
    },
    {
        "service": "s3",
        "method": "list_objects_v2",
        "description": "Lists objects in an S3 bucket",
        "code": """import { S3Client, ListObjectsV2Command } from "@aws-sdk/client-s3";

const client = new S3Client({});

const command = new ListObjectsV2Command({
  Bucket: "my-bucket",
  Prefix: "path/to/folder/"
});

const response = await client.send(command);
response.Contents.forEach(obj => {
  console.log(obj.Key);
});""",
        "parameters": {
            "Bucket": "Name of the S3 bucket",
            "Prefix": "Optional prefix to filter objects"
        },
        "package": "@aws-sdk/client-s3"
    },
    {
        "service": "s3",
        "method": "create_bucket",
        "description": "Creates a new S3 bucket",
        "code": """import { S3Client, CreateBucketCommand } from "@aws-sdk/client-s3";

const client = new S3Client({ region: "us-west-2" });

const command = new CreateBucketCommand({
  Bucket: "my-new-bucket",
  CreateBucketConfiguration: {
    LocationConstraint: "us-west-2"
  }
});

await client.send(command);""",
        "parameters": {
            "Bucket": "Name for the new bucket",
            "CreateBucketConfiguration": "Region configuration"
        },
        "package": "@aws-sdk/client-s3"
    },
    {
        "service": "s3",
        "method": "copy_object",
        "description": "Copies an object within S3",
        "code": """import { S3Client, CopyObjectCommand } from "@aws-sdk/client-s3";

const client = new S3Client({});

const command = new CopyObjectCommand({
  Bucket: "destination-bucket",
  CopySource: "/source-bucket/path/to/file.txt",
  Key: "new/path/file.txt"
});

await client.send(command);""",
        "parameters": {
            "Bucket": "Destination bucket",
            "CopySource": "Source bucket and key",
            "Key": "Destination key"
        },
        "package": "@aws-sdk/client-s3"
    },
    {
        "service": "s3",
        "method": "get_object_attributes",
        "description": "Gets metadata about an S3 object",
        "code": """import { S3Client, GetObjectAttributesCommand } from "@aws-sdk/client-s3";

const client = new S3Client({});

const command = new GetObjectAttributesCommand({
  Bucket: "my-bucket",
  Key: "path/to/file.txt",
  ObjectAttributes: ["ETag", "StorageClass", "ObjectSize"]
});

const response = await client.send(command);
console.log(response);""",
        "parameters": {
            "Bucket": "Name of the bucket",
            "Key": "Object key",
            "ObjectAttributes": "Attributes to retrieve"
        },
        "package": "@aws-sdk/client-s3"
    }
]


# ============================================================================
# FUNCTIONS
# ============================================================================

def create_chunk_text(method_data):
    """Format method data into embedding-ready text"""
    params_text = "\n".join([
        f"- {name}: {desc}" 
        for name, desc in method_data.get("parameters", {}).items()
    ])
    
    text = f"""AWS {method_data['service'].upper()} {method_data['method']} Method (SDK v3)

Description: {method_data['description']}

V3 Code Example:
{method_data['code'].strip()}

Parameters:
{params_text if params_text else 'See code example for parameters'}

Package: {method_data['package']}
Service: {method_data['service']}
Method: {method_data['method']}
SDK Version: v3
"""
    return text.strip()


def create_pinecone_index():
    """Create or get Pinecone index"""
    print(f"\n{'='*60}")
    print("Setting up Pinecone index...")
    print(f"{'='*60}\n")
    
    # Check if index exists
    existing_indexes = pc.list_indexes().names()
    
    if INDEX_NAME in existing_indexes:
        print(f"✓ Index '{INDEX_NAME}' already exists")
        index = pc.Index(INDEX_NAME)
    else:
        print(f"Creating new index '{INDEX_NAME}'...")
        pc.create_index(
            name=INDEX_NAME,
            dimension=DIMENSION,
            metric="cosine",
            spec=ServerlessSpec(
                cloud="aws",
                region="us-east-1"
            )
        )
        print(f"✓ Index created successfully")
        
        # Wait for index to be ready
        print("Waiting for index to initialize...")
        time.sleep(10)
        index = pc.Index(INDEX_NAME)
    
    return index


def embed_text(text):
    """Generate embedding for text"""
    response = openai_client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=text
    )
    return response.data[0].embedding


def upload_methods_to_pinecone(index):
    """Embed and upload all methods to Pinecone - FIXED VERSION"""
    print(f"\n{'='*60}")
    print(f"Embedding and uploading {len(ESSENTIAL_METHODS)} methods...")
    print(f"{'='*60}\n")
    
    vectors = []
    
    for i, method_data in enumerate(ESSENTIAL_METHODS):
        print(f"Processing {i+1}/{len(ESSENTIAL_METHODS)}: {method_data['service']}.{method_data['method']}")
        
        # Create chunk text for embedding
        text = create_chunk_text(method_data)
        
        # Generate embedding
        embedding = embed_text(text)
        
        # FIXED: Store complete code and parameters in metadata
        vector = {
            "id": f"{method_data['service']}_{method_data['method']}_v3",
            "values": embedding,
            "metadata": {
                "service": method_data['service'],
                "method": method_data['method'],
                "sdk_version": "v3",
                "package": method_data['package'],
                "description": method_data['description'],
                "code": method_data['code'],  # ✅ FULL CODE EXAMPLE
                "parameters": json.dumps(method_data['parameters']),  # ✅ SERIALIZED PARAMS
                "label": f"{method_data['service']}_{method_data['method']}_v3"  # ✅ TRACKING
            }
        }
        
        vectors.append(vector)
    
    # Upload to Pinecone in batch
    print(f"\nUploading {len(vectors)} vectors to Pinecone...")
    index.upsert(vectors=vectors, namespace="quickstart")
    
    print(f"✓ Successfully uploaded {len(vectors)} vectors!\n")


def test_retrieval(index):
    """Test retrieval with sample queries"""
    print(f"\n{'='*60}")
    print("TESTING RETRIEVAL")
    print(f"{'='*60}\n")
    
    test_queries = [
        "how do I invoke a lambda function in v3",
        "add item to dynamodb table",
        "upload file to s3 bucket",
        "list all lambda functions",
        "delete object from s3",
        "query dynamodb by key"
    ]
    
    for query in test_queries:
        print(f"\nQuery: '{query}'")
        print("-" * 60)
        
        # Embed query
        query_embedding = embed_text(query)
        
        # Search Pinecone
        results = index.query(
            vector=query_embedding,
            top_k=3,
            namespace="quickstart",
            include_metadata=True
        )
        
        if results['matches']:
            for i, match in enumerate(results['matches'][:3]):
                meta = match['metadata']
                print(f"\n  Result {i+1} (score: {match['score']:.4f}):")
                print(f"    Service: {meta['service']}")
                print(f"    Method: {meta['method']}")
                print(f"    Package: {meta['package']}")
                
                # Show that we have code and parameters now
                if 'code' in meta:
                    code_preview = meta['code'][:100].replace('\n', ' ')
                    print(f"    Code: {code_preview}...")
                
                if 'parameters' in meta:
                    params = json.loads(meta['parameters'])
                    print(f"    Params: {len(params)} defined")
        else:
            print("  ✗ No results found")
    
    print(f"\n{'='*60}")
    print("✓ RETRIEVAL TESTS COMPLETE")
    print(f"{'='*60}\n")


def verify_metadata(index):
    """Verify that metadata contains code and parameters"""
    print(f"\n{'='*60}")
    print("VERIFYING METADATA STRUCTURE")
    print(f"{'='*60}\n")
    
    # Fetch a sample vector
    sample_query = embed_text("upload file to s3")
    results = index.query(
        vector=sample_query,
        top_k=1,
        namespace="quickstart",
        include_metadata=True
    )
    
    if results['matches']:
        meta = results['matches'][0]['metadata']
        print("✓ Sample metadata structure:")
        print(f"  - service: {meta.get('service', 'MISSING')}")
        print(f"  - method: {meta.get('method', 'MISSING')}")
        print(f"  - package: {meta.get('package', 'MISSING')}")
        print(f"  - description: {meta.get('description', 'MISSING')[:50]}...")
        print(f"  - code: {'✓ Present' if 'code' in meta else '✗ MISSING'}")
        print(f"  - parameters: {'✓ Present' if 'parameters' in meta else '✗ MISSING'}")
        print(f"  - label: {meta.get('label', 'MISSING')}")
        
        if 'code' in meta:
            print(f"\n  Code length: {len(meta['code'])} characters")
            print(f"  Code preview:\n{meta['code'][:200]}...")
        
        if 'parameters' in meta:
            params = json.loads(meta['parameters'])
            print(f"\n  Parameters count: {len(params)}")
            for key in list(params.keys())[:3]:
                print(f"    - {key}: {params[key][:50]}...")
    
    print(f"\n{'='*60}")
    print("✓ METADATA VERIFICATION COMPLETE")
    print(f"{'='*60}\n")


def main():
    """Main execution"""
    print(f"\n{'='*60}")
    print("AWS SDK v3 QUICK START - FIXED VERSION")
    print(f"{'='*60}\n")
    
    # Check environment variables
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ ERROR: OPENAI_API_KEY not found in environment")
        print("Create a .env file with: OPENAI_API_KEY=sk-...")
        return
    
    if not os.getenv("PINECONE_API_KEY"):
        print("❌ ERROR: PINECONE_API_KEY not found in environment")
        print("Create a .env file with: PINECONE_API_KEY=...")
        return
    
    print("✓ Environment variables loaded")
    print(f"✓ Embedding model: {EMBEDDING_MODEL}")
    print(f"✓ Methods to process: {len(ESSENTIAL_METHODS)}")
    
    # Create/get index
    index = create_pinecone_index()
    
    # Upload methods with proper metadata
    upload_methods_to_pinecone(index)
    
    # Test retrieval
    test_retrieval(index)
    
    # Verify metadata structure
    verify_metadata(index)
    
    print("\n🎉 SUCCESS! Your vector DB is properly configured!")
    print(f"\nIndex name: {INDEX_NAME}")
    print(f"Namespace: quickstart")
    print(f"Total vectors: {len(ESSENTIAL_METHODS)}")
    print("\n✅ Metadata now includes:")
    print("  - Full code examples")
    print("  - Complete parameter definitions")
    print("  - Tracking labels")
    print("\nYour RAG system should now generate correct upgrades!")
    
    # Show quick usage example
    print("\n" + "="*60)
    print("USAGE IN YOUR APP:")
    print("="*60)
    print("""
from pinecone import Pinecone
from openai import OpenAI
import json

pc = Pinecone(api_key="YOUR_KEY")
openai_client = OpenAI(api_key="YOUR_KEY")

# Query
index = pc.Index("aws-sdk-v3-quickstart")
query_embedding = openai_client.embeddings.create(
    model="text-embedding-3-small",
    input="upload file to s3"
).data[0].embedding

results = index.query(
    vector=query_embedding,
    top_k=3,
    namespace="quickstart",
    include_metadata=True
)

# Access code and parameters
match = results['matches'][0]
code = match['metadata']['code']
params = json.loads(match['metadata']['parameters'])

print("Code example:")
print(code)
print("\\nParameters:")
print(params)
""")


if __name__ == "__main__":
    main()