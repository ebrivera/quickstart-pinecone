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
  "description": "Invokes an AWS Lambda function synchronously (RequestResponse) or asynchronously (Event).",
  "code": """import { LambdaClient, InvokeCommand } from "@aws-sdk/client-lambda";

const client = new LambdaClient({});

const command = new InvokeCommand({
  // Required
  FunctionName: "myFunction",

  // Optional
  InvocationType: "RequestResponse", // or "Event" (async) | "DryRun"
  LogType: "Tail",                   // sync-only: returns last 4 KB of logs (base64) in LogResult
  // ClientContext must be base64-encoded JSON; sync-only:
  // ClientContext: Buffer.from(JSON.stringify({ app: "my-app" })).toString("base64"),
  // Qualifier: "1", // version or alias

  // Payload (Uint8Array). If sending JSON, encode it:
  Payload: new TextEncoder().encode(JSON.stringify({ key: "value" }))
});

const response = await client.send(command);

// Optional: access response fields
// const { StatusCode, FunctionError, LogResult, Payload, ExecutedVersion } = response;

// Optional: decode/parse JSON payload if present
// const text = Payload ? new TextDecoder().decode(Payload) : null;
// const result = text ? JSON.parse(text) : null;""",
  "parameters": {
    "FunctionName": "Name or ARN of the Lambda function. Required.",
    "InvocationType": "\"RequestResponse\" (sync, default), \"Event\" (async), or \"DryRun\". Optional.",
    "LogType": "\"Tail\" to include last 4 KB of logs (sync-only). Optional.",
    "ClientContext": "Base64-encoded JSON string passed to the function (sync-only). Optional.",
    "Qualifier": "Version or alias to invoke. Optional.",
    "Payload": "Request body as Uint8Array (encode JSON with TextEncoder). Optional."
  },
  "package": "@aws-sdk/client-lambda"
},
    {
  "service": "lambda",
  "method": "create_function",
  "description": "Creates a new Lambda function from a ZIP deployment package (ZipFile or S3) or a container image (ImageUri), using the specified execution role.",
  "code": """import { LambdaClient, CreateFunctionCommand } from "@aws-sdk/client-lambda";

const client = new LambdaClient({});

const command = new CreateFunctionCommand({
  // --- Required ---
  FunctionName: "my-function",
  Role: "arn:aws:iam::123456789012:role/MyLambdaRole",
  Code: {
    // Choose ONE source:

    // 1) Inline ZIP bytes
    // ZipFile: new Uint8Array(/* bytes of your .zip file */),

    // 2) ZIP from S3
    // S3Bucket: "my-bucket",
    // S3Key: "path/to/code.zip",
    // S3ObjectVersion: "optional-object-version",

    // 3) Container image
    // ImageUri: "123456789012.dkr.ecr.us-east-1.amazonaws.com/my-image:latest"
  },

  // --- Conditionally required (ZIP only) ---
  // Runtime: "nodejs22.x",
  // Handler: "index.handler",

  // --- Optional ---
  // PackageType: "Zip", // or "Image" when using ImageUri
  // Architectures: ["x86_64"], // or ["arm64"]
  // MemorySize: 128,           // MB (default 128)
  // Timeout: 3,                // seconds (default 3)
  // Description: "My function created via SDK v3",
  // Environment: { Variables: { NODE_ENV: "production" } },
  // VpcConfig: { SubnetIds: ["subnet-..."], SecurityGroupIds: ["sg-..."] },
  // DeadLetterConfig: { TargetArn: "arn:aws:sqs:..." },
  // TracingConfig: { Mode: "Active" }, // or "PassThrough"
  // KMSKeyArn: "arn:aws:kms:...",
  // Layers: ["arn:aws:lambda:us-east-1:123456789012:layer:MyLayer:1"],
  // ImageConfig: { Command: ["node", "app.js"], EntryPoint: [], WorkingDirectory: "/" },
  // EphemeralStorage: { Size: 1024 }, // MB (512–10240)
  // FileSystemConfigs: [{ Arn: "arn:aws:efs:...", LocalMountPath: "/mnt/efs" }],
  // LoggingConfig: { LogFormat: "Text", ApplicationLogLevel: "INFO", SystemLogLevel: "INFO" },
  // SnapStart: { ApplyOn: "PublishedVersions" }, // supported runtimes (e.g., Java)
  // RuntimeManagementConfig: { UpdateRuntimeOn: "Auto" }, // or "FunctionUpdate" | "Manual"
  // Tags: { project: "alpha" },
  // Publish: true
});

const response = await client.send(command);

// Optional: access response fields
// const { FunctionArn, Runtime, Handler, LastModified, State } = response;""",
  "parameters": {
    "FunctionName": "Name of the new Lambda function. Required.",
    "Role": "IAM role ARN the function assumes. Required.",
    "Code": "Deployment package or image definition. Use ZipFile/S3Bucket+S3Key for ZIP, or ImageUri for container. Required.",
    "Runtime": "Language runtime (e.g., nodejs22.x). Required when PackageType is 'Zip'; not used for 'Image'.",
    "Handler": "Entry point for ZIP functions (e.g., index.handler). Required when PackageType is 'Zip'.",
    "PackageType": "'Zip' (default) or 'Image' for container-based functions.",
    "ImageConfig": "For container images: optional Command, EntryPoint, WorkingDirectory.",
    "Architectures": "Instruction set, e.g., ['x86_64'] or ['arm64'].",
    "MemorySize": "Memory in MB (also influences CPU). Default 128.",
    "Timeout": "Function timeout in seconds. Default 3.",
    "Environment": "Key–value environment variables.",
    "VpcConfig": "Subnets and security groups for VPC access.",
    "DeadLetterConfig": "ARN for SQS/SNS destination of failed async invocations.",
    "TracingConfig": "AWS X-Ray tracing mode ('Active' or 'PassThrough').",
    "KMSKeyArn": "KMS key ARN to encrypt environment variables.",
    "Layers": "List of layer version ARNs.",
    "EphemeralStorage": "Size of /tmp in MB (512–10240).",
    "FileSystemConfigs": "Mount EFS access points into the function.",
    "LoggingConfig": "Function logging format and levels (where supported).",
    "SnapStart": "Startup snapshotting for supported runtimes (e.g., Java).",
    "RuntimeManagementConfig": "How runtime updates are applied ('Auto', 'FunctionUpdate', or 'Manual').",
    "Tags": "Tags to assign at creation.",
    "Publish": "If true, publishes version 1 immediately."
  },
  "package": "@aws-sdk/client-lambda"
},
    {
  "service": "lambda",
  "method": "list_functions",
  "description": "Returns a paginated list of Lambda functions. Set FunctionVersion='ALL' to include all published versions; otherwise only the unpublished ($LATEST) version is returned.",
  "code": """import { LambdaClient, ListFunctionsCommand } from "@aws-sdk/client-lambda";

const client = new LambdaClient({});

const command = new ListFunctionsCommand({
  // No required parameters

  // Optional parameters
  // FunctionVersion: "ALL",   // Include all published versions (in addition to $LATEST)
  // Marker: "<TOKEN>",        // Pagination token from a prior response.NextMarker
  // MaxItems: 50,             // Page size
  // MasterRegion: "us-east-1" // For replicated functions, filter by master region
});

const response = await client.send(command);

// Optional: access response fields
// const { Functions = [], NextMarker } = response;

// Example: simple pagination
// let marker;
// do {
//   const page = await client.send(new ListFunctionsCommand({ Marker: marker, MaxItems: 50 }));
//   for (const fn of page.Functions || []) {
//     // fn.FunctionName, fn.Runtime, fn.LastModified, etc.
//   }
//   marker = page.NextMarker;
// } while (marker);
""",
  "parameters": {
    "No required parameters": "This operation accepts only optional inputs.",
    "FunctionVersion": "Set to 'ALL' to include all published versions (default returns only $LATEST).",
    "Marker": "Pagination token from the previous response's NextMarker.",
    "MaxItems": "Maximum number of functions to return in one page.",
    "MasterRegion": "For replicated functions, restrict results to the specified master region."
  },
  "package": "@aws-sdk/client-lambda"
},
    {
  "service": "lambda",
  "method": "update_function_code",
  "description": "Updates the code for an existing Lambda function from a ZIP package (inline or S3) or a container image. Supports Publish and DryRun.",
  "code": """import { LambdaClient, UpdateFunctionCodeCommand } from "@aws-sdk/client-lambda";

const client = new LambdaClient({});

const command = new UpdateFunctionCodeCommand({
  // --- Required ---
  FunctionName: "my-function",

  // --- Choose ONE code source ---
  // 1) Inline ZIP bytes:
  // ZipFile: new Uint8Array(/* bytes of your .zip file */),

  // 2) S3 ZIP (bucket must be in the same Region as the function):
  // S3Bucket: "my-bucket",
  // S3Key: "path/to/code.zip",
  // S3ObjectVersion: "optional-version",

  // 3) Container image (function must already be PackageType='Image'):
  // ImageUri: "123456789012.dkr.ecr.us-east-1.amazonaws.com/my-image:latest",

  // --- Optional ---
  // Publish: true,                    // publish a new version
  // DryRun: false,                    // validate without applying
  // RevisionId: "expected-revision-id", // optimistic concurrency control
  // SourceKMSKeyArn: "arn:aws:kms:...", // decrypt S3 object if encrypted with CMK
  // Architectures: ["x86_64"]          // or ["arm64"] if supported by the function
});

const response = await client.send(command);

// Optional: access response fields
// const { FunctionArn, LastModified, Version, State, LastUpdateStatus } = response;""",
  "parameters": {
    "FunctionName": "Name or ARN of the target Lambda function. Required.",
    "ZipFile": "Raw bytes (Uint8Array/Buffer) of the ZIP deployment package. Use only for ZIP package type.",
    "S3Bucket": "S3 bucket containing the ZIP package (must be in the same Region).",
    "S3Key": "S3 object key for the ZIP package.",
    "S3ObjectVersion": "Version ID of the S3 object when using a versioned bucket.",
    "ImageUri": "ECR image URI for container-based functions (PackageType must already be 'Image').",
    "Publish": "If true, publishes a new version after updating the code.",
    "DryRun": "If true, validates parameters/permissions without applying changes.",
    "RevisionId": "Update only if the current function revision matches this ID (optimistic locking).",
    "SourceKMSKeyArn": "KMS key ARN used to decrypt the S3 object, if encrypted.",
    "Architectures": "Instruction set compatibility: ['x86_64'] or ['arm64'] (where supported)."
  },
  "package": "@aws-sdk/client-lambda"
},
    {
  "service": "lambda",
  "method": "delete_function",
  "description": "Deletes a Lambda function. To delete only a specific published version, provide Qualifier (cannot be $LATEST).",
  "code": """import { LambdaClient, DeleteFunctionCommand } from "@aws-sdk/client-lambda";

const client = new LambdaClient({});

const command = new DeleteFunctionCommand({
  // Required
  FunctionName: "my-function", // name, full ARN, or partial ARN

  // Optional
  // Qualifier: "3" // delete a specific published version (cannot be $LATEST)
});

await client.send(command);

// No payload is returned on success.
// Wrap in try/catch to handle errors as needed.
""",
  "parameters": {
    "FunctionName": "Name, full ARN, or partial ARN of the function to delete. Required.",
    "Qualifier": "Version number to delete a specific published version (cannot be $LATEST). Optional."
  },
  "package": "@aws-sdk/client-lambda"
},

    # DYNAMODB - 8 methods
    {
  "service": "dynamodb",
  "method": "put_item",
  "description": "Creates a new item or replaces an existing item in a DynamoDB table; supports conditional writes and optional return of the old item.",
  "code": """import { DynamoDBClient, PutItemCommand } from "@aws-sdk/client-dynamodb";

const client = new DynamoDBClient({});

const command = new PutItemCommand({
  // --- Required ---
  TableName: "MyTable",
  Item: {
    // Include the table's primary key attributes (and sort key if defined)
    pk: { S: "USER#123" },
    sk: { S: "PROFILE#v1" },
    createdAt: { S: new Date().toISOString() },
    loginCount: { N: "0" } // numbers are strings in AttributeValue
  },

  // --- Optional (use only if referenced) ---
  // ConditionExpression: "attribute_not_exists(pk)",
  // ExpressionAttributeNames: { "#c": "createdAt" },
  // ExpressionAttributeValues: { ":zero": { N: "0" } },

  // Return control
  // ReturnValues: "ALL_OLD",                 // PutItem supports: "NONE" (default) | "ALL_OLD"
  // ReturnConsumedCapacity: "TOTAL",         // "INDEXES" | "TOTAL" | "NONE"
  // ReturnItemCollectionMetrics: "SIZE",     // "SIZE" | "NONE"
  // ReturnValuesOnConditionCheckFailure: "ALL_OLD" // or "NONE"
});

const response = await client.send(command);

// Optional: access response fields
// const { Attributes, ConsumedCapacity, ItemCollectionMetrics } = response;

// Tip: Prefer the Document Client for plain JS objects:
// import { DynamoDBDocumentClient, PutCommand } from "@aws-sdk/lib-dynamodb";
// const doc = DynamoDBDocumentClient.from(client);
// await doc.send(new PutCommand({ TableName, Item: { pk: "USER#123", ... } }));
""",
  "parameters": {
    "TableName": "Target table name. Required.",
    "Item": "Map of attribute names to AttributeValue objects (S, N, BOOL, M, L, etc.). Must include the table's key attributes. Required.",
    "ConditionExpression": "A condition that must be satisfied for the write to succeed.",
    "ExpressionAttributeNames": "Substitution tokens for attribute names used in expressions.",
    "ExpressionAttributeValues": "Values for tokens referenced in expressions.",
    "ReturnValues": "For PutItem: 'NONE' (default) or 'ALL_OLD'.",
    "ReturnConsumedCapacity": "'INDEXES' | 'TOTAL' | 'NONE'.",
    "ReturnItemCollectionMetrics": "'SIZE' | 'NONE'.",
    "ReturnValuesOnConditionCheckFailure": "'ALL_OLD' | 'NONE' when the condition check fails."
  },
  "package": "@aws-sdk/client-dynamodb"
},
    {
  "service": "dynamodb",
  "method": "get_item",
  "description": "Retrieves a single item by primary key from a DynamoDB table; supports optional strong consistency and attribute projection.",
  "code": """import { DynamoDBClient, GetItemCommand } from "@aws-sdk/client-dynamodb";

const client = new DynamoDBClient({});

const command = new GetItemCommand({
  // --- Required ---
  TableName: "MyTable",
  Key: {
    pk: { S: "USER#123" },
    // Include sort key only if the table defines one:
    sk: { S: "PROFILE#v1" }
  },

  // --- Optional ---
  // ConsistentRead: true, // default is eventually consistent
  // ProjectionExpression: "#n, email, createdAt",
  // ExpressionAttributeNames: { "#n": "name" }, // needed if using reserved words/aliases
  // ReturnConsumedCapacity: "TOTAL" // "INDEXES" | "TOTAL" | "NONE"
});

const response = await client.send(command);

// Optional: access response fields
// const { Item, ConsumedCapacity } = response;
// Note: Item may be undefined if no matching item exists.

// Tip: Prefer the Document Client for plain JS objects:
// import { DynamoDBDocumentClient, GetCommand } from "@aws-sdk/lib-dynamodb";
// const doc = DynamoDBDocumentClient.from(client);
// const out = await doc.send(new GetCommand({ TableName, Key: { pk: "USER#123", sk: "PROFILE#v1" }, ProjectionExpression: "#n, email, createdAt", ExpressionAttributeNames: { "#n": "name" } }));
""",
  "parameters": {
    "TableName": "Target table name. Required.",
    "Key": "Map of attribute names to AttributeValue for the full primary key (partition key and sort key if defined). Types must match the table schema. Required.",
    "ConsistentRead": "Boolean to request a strongly consistent read; default is eventually consistent.",
    "ProjectionExpression": "Attributes to return, expressed as a projection expression.",
    "ExpressionAttributeNames": "Token map for attribute names referenced in expressions (use for reserved words/aliases).",
    "ReturnConsumedCapacity": "Include capacity details: 'INDEXES' | 'TOTAL' | 'NONE'."
  },
  "package": "@aws-sdk/client-dynamodb"
},
    {
  "service": "dynamodb",
  "method": "update_item",
  "description": "Updates attributes of an existing item (or creates it if missing) using an update expression; supports conditional writes and returning updated attributes.",
  "code": """import { DynamoDBClient, UpdateItemCommand } from "@aws-sdk/client-dynamodb";

const client = new DynamoDBClient({});

const command = new UpdateItemCommand({
  // --- Required ---
  TableName: "MyTable",
  Key: {
    pk: { S: "USER#123" },
    // Include sort key only if the table defines one:
    sk: { S: "PROFILE#v1" }
  },
  // Use one or more clauses (SET | REMOVE | ADD | DELETE)
  UpdateExpression: "SET #count = if_not_exists(#count, :zero) + :inc REMOVE obsoleteAttr",

  // --- Optional (only if referenced) ---
  // ConditionExpression: "attribute_exists(pk) AND #version = :expected",
  // ExpressionAttributeNames: { "#count": "loginCount", "#version": "version" },
  // ExpressionAttributeValues: { ":zero": { N: "0" }, ":inc": { N: "1" }, ":expected": { N: "3" } },

  // Return controls
  // ReturnValues: "UPDATED_NEW",            // NONE | ALL_OLD | UPDATED_OLD | ALL_NEW | UPDATED_NEW
  // ReturnConsumedCapacity: "TOTAL",        // INDEXES | TOTAL | NONE
  // ReturnItemCollectionMetrics: "SIZE",    // SIZE | NONE
  // ReturnValuesOnConditionCheckFailure: "ALL_OLD" // or NONE
});

const response = await client.send(command);

// Optional: access response fields
// const { Attributes, ConsumedCapacity, ItemCollectionMetrics } = response;

// Notes:
// - If no item exists for the given Key and no ConditionExpression blocks it, UpdateItem creates a new item.
// - You cannot update primary key attributes (partition/sort keys).
// - ADD works with numbers and set types; DELETE works with set types.
""",
  "parameters": {
    "TableName": "Target table name. Required.",
    "Key": "Full primary key as an AttributeValue map (partition key and sort key if defined). Types must match schema. Required.",
    "UpdateExpression": "One or more clauses (SET, REMOVE, ADD, DELETE) describing the update. Required unless using legacy AttributeUpdates.",
    "ConditionExpression": "Boolean expression that must evaluate to true for the update to proceed.",
    "ExpressionAttributeNames": "Placeholders mapping (e.g., #attr -> real name) used in expressions.",
    "ExpressionAttributeValues": "Placeholders (e.g., :v) to AttributeValue objects referenced in expressions.",
    "ReturnValues": "Attributes to return: NONE | ALL_OLD | UPDATED_OLD | ALL_NEW | UPDATED_NEW.",
    "ReturnConsumedCapacity": "Include capacity details: INDEXES | TOTAL | NONE.",
    "ReturnItemCollectionMetrics": "Include item collection metrics: SIZE | NONE.",
    "ReturnValuesOnConditionCheckFailure": "When a condition fails, optionally return item attributes: ALL_OLD | NONE."
  },
  "package": "@aws-sdk/client-dynamodb"
},
    {
  "service": "dynamodb",
  "method": "delete_item",
  "description": "Deletes a single item identified by its primary key; supports conditional deletes and optional return of the deleted attributes.",
  "code": """import { DynamoDBClient, DeleteItemCommand } from "@aws-sdk/client-dynamodb";

const client = new DynamoDBClient({});

const command = new DeleteItemCommand({
  // --- Required ---
  TableName: "MyTable",
  Key: {
    pk: { S: "USER#123" },
    // Include sort key only if the table defines one:
    sk: { S: "PROFILE#v1" }
  },

  // --- Optional (only if referenced) ---
  // ConditionExpression: "attribute_exists(pk) AND #version = :expected",
  // ExpressionAttributeNames: { "#version": "version" },
  // ExpressionAttributeValues: { ":expected": { N: "3" } },

  // Return controls
  // ReturnValues: "ALL_OLD",               // DeleteItem supports: "NONE" (default) | "ALL_OLD"
  // ReturnConsumedCapacity: "TOTAL",       // "INDEXES" | "TOTAL" | "NONE"
  // ReturnItemCollectionMetrics: "SIZE",   // "SIZE" | "NONE"
  // ReturnValuesOnConditionCheckFailure: "ALL_OLD" // or "NONE"
});

const response = await client.send(command);

// Optional: access response fields
// const { Attributes, ConsumedCapacity, ItemCollectionMetrics } = response;
// Note: If the item did not exist, Attributes will be undefined.
// Tip: With the Document Client, you can work with plain JS objects:
// import { DynamoDBDocumentClient, DeleteCommand } from "@aws-sdk/lib-dynamodb";
// const doc = DynamoDBDocumentClient.from(client);
// await doc.send(new DeleteCommand({ TableName, Key: { pk: "USER#123", sk: "PROFILE#v1" }, ReturnValues: "ALL_OLD" }));
""",
  "parameters": {
    "TableName": "Target table name. Required.",
    "Key": "Full primary key as an AttributeValue map (partition key and sort key if defined). Types must match the table schema. Required.",
    "ConditionExpression": "Boolean expression that must evaluate to true for the delete to proceed.",
    "ExpressionAttributeNames": "Placeholder map (e.g., { \"#v\": \"version\" }) used in expressions.",
    "ExpressionAttributeValues": "Values map (e.g., { \":n\": { N: \"1\" } }) for expression placeholders.",
    "ReturnValues": "For DeleteItem: 'NONE' (default) or 'ALL_OLD' (deleted item's attributes).",
    "ReturnConsumedCapacity": "'INDEXES' | 'TOTAL' | 'NONE'.",
    "ReturnItemCollectionMetrics": "'SIZE' | 'NONE'.",
    "ReturnValuesOnConditionCheckFailure": "'ALL_OLD' | 'NONE' when a condition fails."
  },
  "package": "@aws-sdk/client-dynamodb"
},
    {
  "service": "dynamodb",
  "method": "query",
  "description": "Queries items that share a partition key (and optional sort-key condition), with support for filters, projections, pagination, and optional strong consistency on the base table/LSIs.",
  "code": """import { DynamoDBClient, QueryCommand } from "@aws-sdk/client-dynamodb";

const client = new DynamoDBClient({});

const command = new QueryCommand({
  // --- Required ---
  TableName: "MyTable",
  // Partition key equality is required; sort key condition is optional:
  KeyConditionExpression: "pk = :pk AND begins_with(sk, :prefix)",

  // --- Values / Names used in expressions ---
  // ExpressionAttributeValues: { ":pk": { S: "USER#123" }, ":prefix": { S: "PROFILE#" } },
  // ExpressionAttributeNames: { "#n": "name" },

  // --- Optional modifiers ---
  // FilterExpression: "attribute_exists(email) AND loginCount > :min", // post-filter, does not reduce RCUs
  // ProjectionExpression: "#n, email, createdAt",
  // IndexName: "GSI1",                 // query a secondary index instead of the base table
  // ConsistentRead: true,              // only for base table & LSIs; GSIs are eventually consistent
  // ScanIndexForward: true,            // true = ascending, false = descending (by sort key)
  // Limit: 50,                         // page size (items evaluated/returned)
  // ExclusiveStartKey: { pk: { S: "USER#123" }, sk: { S: "PROFILE#v1" } }, // pagination cursor
  // ReturnConsumedCapacity: "TOTAL",   // "INDEXES" | "TOTAL" | "NONE"
  // Select: "ALL_ATTRIBUTES"           // "ALL_ATTRIBUTES" | "ALL_PROJECTED_ATTRIBUTES" | "COUNT" | "SPECIFIC_ATTRIBUTES"
});

const response = await client.send(command);

// Optional: access response fields
// const { Items = [], Count, ScannedCount, LastEvaluatedKey, ConsumedCapacity } = response;

// Example: simple pager
// let lastKey;
// do {
//   const page = await client.send(new QueryCommand({
//     TableName: "MyTable",
//     KeyConditionExpression: "pk = :pk",
//     ExpressionAttributeValues: { ":pk": { S: "USER#123" } },
//     ExclusiveStartKey: lastKey,
//     Limit: 50
//   }));
//   (page.Items || []).forEach(item => { /* handle item */ });
//   lastKey = page.LastEvaluatedKey;
// } while (lastKey);

// Notes:
// - KeyConditionExpression requires equality on the partition key; the sort key may include comparisons,
//   BETWEEN, or begins_with(...).
// - If using Select other than SPECIFIC_ATTRIBUTES, omit ProjectionExpression.
// - AttributeValue shapes require numbers as strings (e.g., { N: "1" }).
""",
  "parameters": {
    "TableName": "Target table name. Required.",
    "KeyConditionExpression": "Must specify equality on the partition key; may include a comparison, BETWEEN, or begins_with on the sort key. Required.",
    "ExpressionAttributeValues": "Values map for placeholders in expressions (AttributeValue shapes, e.g., { \":pk\": { S: \"USER#123\" } }).",
    "ExpressionAttributeNames": "Substitution map for attribute names used in expressions (e.g., { \"#n\": \"name\" }).",
    "FilterExpression": "Post-query filter applied after matching the key condition; does not reduce RCU consumption.",
    "ProjectionExpression": "Attributes to include in the result; omit if Select ≠ 'SPECIFIC_ATTRIBUTES'.",
    "IndexName": "Name of a secondary index to query instead of the base table.",
    "ConsistentRead": "Strongly consistent reads for base table and LSIs only; GSIs are eventually consistent.",
    "ScanIndexForward": "Sort order on the sort key (true = ascending, false = descending).",
    "Limit": "Maximum number of items to evaluate/return per page.",
    "ExclusiveStartKey": "Primary key of the first item to evaluate (pagination cursor).",
    "Select": "Which attributes to return: 'ALL_ATTRIBUTES' | 'ALL_PROJECTED_ATTRIBUTES' | 'COUNT' | 'SPECIFIC_ATTRIBUTES'.",
    "ReturnConsumedCapacity": "Include capacity details: 'INDEXES' | 'TOTAL' | 'NONE'."
  },
  "package": "@aws-sdk/client-dynamodb"
},
    {
  "service": "dynamodb",
  "method": "scan",
  "description": "Scans a table or secondary index and returns items that match an optional filter; supports projections, pagination, and parallel scan.",
  "code": """import { DynamoDBClient, ScanCommand } from "@aws-sdk/client-dynamodb";

const client = new DynamoDBClient({});

const command = new ScanCommand({
  // --- Required ---
  TableName: "MyTable",

  // --- Optional ---
  // IndexName: "GSI1",                   // scan a secondary index instead of the base table
  // FilterExpression: "attribute_exists(email) AND #cnt >= :min", // post-filter; does NOT reduce RCUs
  // ProjectionExpression: "#id, email, #cnt",
  // ExpressionAttributeNames: { "#id": "pk", "#cnt": "loginCount" },
  // ExpressionAttributeValues: { ":min": { N: "5" } },
  // ConsistentRead: true,                // base table & LSIs only; GSIs are eventually consistent
  // Limit: 100,                          // page size (max items evaluated/returned per page)
  // ExclusiveStartKey: { pk: { S: "USER#123" }, sk: { S: "PROFILE#v1" } }, // pagination token
  // ReturnConsumedCapacity: "TOTAL",     // "INDEXES" | "TOTAL" | "NONE"
  // Select: "ALL_ATTRIBUTES",            // "ALL_ATTRIBUTES" | "ALL_PROJECTED_ATTRIBUTES" | "COUNT" | "SPECIFIC_ATTRIBUTES"
  // Segment: 0,                          // for parallel scan: this worker's segment (0-based)
  // TotalSegments: 4                     // for parallel scan: total number of segments
});

const response = await client.send(command);

// Optional: access response fields
// const { Items = [], Count, ScannedCount, LastEvaluatedKey, ConsumedCapacity } = response;

// Example: full-table scan with pagination (use sparingly; Query is usually cheaper)
// let lastKey;
// do {
//   const page = await client.send(new ScanCommand({
//     TableName: "MyTable",
//     ExclusiveStartKey: lastKey,
//     Limit: 200
//   }));
//   (page.Items || []).forEach(item => { /* handle item */ });
//   lastKey = page.LastEvaluatedKey;
// } while (lastKey);

// Notes:
// - FilterExpression is applied after items are read, so it doesn't reduce read capacity.
// - If Select != "SPECIFIC_ATTRIBUTES", omit ProjectionExpression.
// - For parallel scans, provide both Segment and TotalSegments for each worker.
""",
  "parameters": {
    "TableName": "Name of the table to scan. Required.",
    "IndexName": "Scan a secondary index instead of the base table.",
    "FilterExpression": "Post-scan filter; non-matching items are discarded but still consume RCUs.",
    "ProjectionExpression": "Attributes to include in the result; omit if Select ≠ 'SPECIFIC_ATTRIBUTES'.",
    "ExpressionAttributeNames": "Substitution tokens for attribute names used in expressions.",
    "ExpressionAttributeValues": "Values for tokens referenced in expressions (AttributeValue shapes).",
    "ConsistentRead": "Strongly consistent reads for base table and LSIs only; GSIs are eventually consistent.",
    "Limit": "Maximum number of items evaluated/returned per page.",
    "ExclusiveStartKey": "Primary key of the first item to evaluate (pagination cursor).",
    "ReturnConsumedCapacity": "'INDEXES' | 'TOTAL' | 'NONE'.",
    "Select": "'ALL_ATTRIBUTES' | 'ALL_PROJECTED_ATTRIBUTES' | 'COUNT' | 'SPECIFIC_ATTRIBUTES'.",
    "Segment": "Parallel scan: this worker's segment number (0-based). Use with TotalSegments.",
    "TotalSegments": "Parallel scan: total number of segments being processed."
  },
  "package": "@aws-sdk/client-dynamodb"
},
    {
  "service": "dynamodb",
  "method": "batch_write_item",
  "description": "Writes or deletes up to 25 items across one or more tables in a single request; returns unprocessed items for retry.",
  "code": """import { DynamoDBClient, BatchWriteItemCommand } from "@aws-sdk/client-dynamodb";

const client = new DynamoDBClient({});

const command = new BatchWriteItemCommand({
  // --- Required ---
  RequestItems: {
    // Table name -> array of write requests
    MyTable: [
      { PutRequest: { Item: { pk: { S: "USER#123" }, sk: { S: "PROFILE#v1" }, loginCount: { N: "0" } } } },
      { DeleteRequest: { Key:  { pk: { S: "USER#124" }, sk: { S: "PROFILE#v1" } } } }
    ]
  },

  // --- Optional ---
  // ReturnConsumedCapacity: "TOTAL",      // "INDEXES" | "TOTAL" | "NONE"
  // ReturnItemCollectionMetrics: "SIZE"   // "SIZE" | "NONE"
});

const response = await client.send(command);

// Handle retries for throttled/unprocessed items
// (Best practice: exponential backoff + jitter)
let unprocessed = response.UnprocessedItems;
let attempt = 0;
while (unprocessed && Object.keys(unprocessed).length) {
  const delayMs = Math.min(1000 * 2 ** attempt, 15000) * (0.5 + Math.random()); // backoff + jitter
  await new Promise(r => setTimeout(r, delayMs));
  const retry = await client.send(new BatchWriteItemCommand({ RequestItems: unprocessed }));
  unprocessed = retry.UnprocessedItems;
  attempt++;
}

// Optional: access response fields
// const { UnprocessedItems, ConsumedCapacity, ItemCollectionMetrics } = response;

// Notes:
// - Max 25 requests per call; total payload ≤ 16 MB; each item ≤ 400 KB.
// - Requests are best-effort; you must retry UnprocessedItems.
// - No ConditionExpression support here; use TransactWriteItems or single-item ops for conditional writes.
""",
  "parameters": {
    "RequestItems": "Map of table name to an array (≤ 25 total requests) of { PutRequest: { Item } } or { DeleteRequest: { Key } }. Required.",
    "ReturnConsumedCapacity": "Include capacity details in the response: 'INDEXES' | 'TOTAL' | 'NONE'. Optional.",
    "ReturnItemCollectionMetrics": "Include item collection metrics: 'SIZE' | 'NONE'. Optional."
  },
  "package": "@aws-sdk/client-dynamodb"
},
    {
  "service": "dynamodb",
  "method": "create_table",
  "description": "Creates a new DynamoDB table by defining attributes, key schema, and capacity mode (provisioned or on-demand).",
  "code": """import { DynamoDBClient, CreateTableCommand } from "@aws-sdk/client-dynamodb";

const client = new DynamoDBClient({});

const command = new CreateTableCommand({
  // --- Required ---
  TableName: "MyTable",
  AttributeDefinitions: [
    // Include every attribute used by the table key schema and any index key schema.
    // Only 'S' (string), 'N' (number), or 'B' (binary) types are allowed here.
    { AttributeName: "pk", AttributeType: "S" },
    { AttributeName: "sk", AttributeType: "S" } // include only if you use a sort key
    // Add index key attributes as needed, e.g., { AttributeName: "gsi1pk", AttributeType: "S" }
  ],
  KeySchema: [
    { AttributeName: "pk", KeyType: "HASH" },   // partition key
    { AttributeName: "sk", KeyType: "RANGE" }   // optional sort key
  ],

  // --- Capacity mode ---
  // BillingMode: "PAY_PER_REQUEST", // on-demand; omit all ProvisionedThroughput fields when using this
  // ProvisionedThroughput: { ReadCapacityUnits: 5, WriteCapacityUnits: 5 }, // required if BillingMode is PROVISIONED (default)

  // --- Local Secondary Indexes (define only at table creation; share the table's partition key) ---
  // LocalSecondaryIndexes: [
  //   {
  //     IndexName: "LSI1",
  //     KeySchema: [
  //       { AttributeName: "pk", KeyType: "HASH" },
  //       { AttributeName: "createdAt", KeyType: "RANGE" } // ensure AttributeDefinitions includes 'createdAt'
  //     ],
  //     Projection: { ProjectionType: "INCLUDE", NonKeyAttributes: ["email", "status"] }
  //   }
  // ],

  // --- Global Secondary Indexes (can also be added later with UpdateTable) ---
  // GlobalSecondaryIndexes: [
  //   {
  //     IndexName: "GSI1",
  //     KeySchema: [
  //       { AttributeName: "gsi1pk", KeyType: "HASH" },
  //       { AttributeName: "gsi1sk", KeyType: "RANGE" }
  //     ],
  //     Projection: { ProjectionType: "ALL" },
  //     // If table BillingMode is PROVISIONED, each GSI must also specify throughput:
  //     // ProvisionedThroughput: { ReadCapacityUnits: 5, WriteCapacityUnits: 5 }
  //   }
  // ],

  // --- Other options ---
  // StreamSpecification: { StreamEnabled: true, StreamViewType: "NEW_AND_OLD_IMAGES" },
  // SSESpecification: { Enabled: true, SSEType: "KMS", KMSMasterKeyId: "alias/aws/dynamodb" },
  // Tags: [{ Key: "project", Value: "alpha" }],
  // TableClass: "STANDARD", // or "STANDARD_INFREQUENT_ACCESS"
  // DeletionProtectionEnabled: false
});

const response = await client.send(command);

// Optional: access response fields
// const { TableDescription } = response;
""",
  "parameters": {
    "TableName": "Name for the new table. Required.",
    "AttributeDefinitions": "List of attributes referenced by the table/index key schemas (types: 'S' | 'N' | 'B'). Must include all key attributes. Required.",
    "KeySchema": "Primary key definition: one HASH (partition) key and optional RANGE (sort) key. Required.",
    "BillingMode": "Capacity mode: 'PROVISIONED' (default) or 'PAY_PER_REQUEST' (on-demand).",
    "ProvisionedThroughput": "Read/Write capacity units for the table (and for each GSI) when using PROVISIONED.",
    "LocalSecondaryIndexes": "LSIs (max 5). Must be defined at table creation; share the table's partition key. Include KeySchema and Projection.",
    "GlobalSecondaryIndexes": "GSIs with their own key schema and Projection; in PROVISIONED mode, specify ProvisionedThroughput per GSI.",
    "StreamSpecification": "Enable DynamoDB Streams and choose the view type (e.g., KEYS_ONLY, NEW_IMAGE, OLD_IMAGE, NEW_AND_OLD_IMAGES).",
    "SSESpecification": "Server-side encryption settings (KMS usage and key).",
    "Tags": "Array of { Key, Value } to tag the table at creation.",
    "TableClass": "Storage class: 'STANDARD' or 'STANDARD_INFREQUENT_ACCESS'.",
    "DeletionProtectionEnabled": "If true, prevents table deletion until disabled."
  },
  "package": "@aws-sdk/client-dynamodb"
},

    # S3 - 7 methods
    {
  "service": "s3",
  "method": "put_object",
  "description": "Uploads (creates or overwrites) an object in an S3 bucket; supports metadata, ACLs, server-side encryption, checksums, and storage classes.",
  "code": """import { S3Client, PutObjectCommand } from "@aws-sdk/client-s3";

const client = new S3Client({});

const command = new PutObjectCommand({
  // --- Required ---
  Bucket: "my-bucket",
  Key: "path/to/object.txt",

  // --- Body (choose one) ---
  // Body: new TextEncoder().encode("hello world"), // bytes (Uint8Array)
  // Body: fileBlobOrBufferOrStream,                // Blob (browser) or Buffer/Readable (Node)
  // ContentType: "text/plain",

  // --- Common optional headers ---
  // ACL: "private", // e.g., "public-read", "bucket-owner-full-control" (ignored if Object Ownership is BucketOwnerEnforced)
  // Metadata: { "x-app-id": "alpha", "env": "prod" },
  // CacheControl: "max-age=3600",
  // ContentEncoding: "gzip",
  // ContentLanguage: "en",
  // ContentDisposition: "inline",
  // ContentLength: 11, // only needed for some streams; SDK infers for bytes/buffers
  // ContentMD5: "base64-md5-hash",

  // --- Storage tier & tagging ---
  // StorageClass: "STANDARD", // e.g., "STANDARD_IA" | "ONEZONE_IA" | "GLACIER" | "DEEP_ARCHIVE"
  // Tagging: "k1=v1&k2=v2",   // URL-encoded tag string
  // WebsiteRedirectLocation: "/some/redirect",

  // --- Server-side encryption (choose ONE approach) ---
  // 1) SSE-S3:
  // ServerSideEncryption: "AES256",
  //
  // 2) SSE-KMS:
  // ServerSideEncryption: "aws:kms",
  // SSEKMSKeyId: "arn:aws:kms:us-east-1:123456789012:key/...",
  //
  // 3) SSE-C (customer-provided key):
  // SSECustomerAlgorithm: "AES256",
  // SSECustomerKey: "base64-encoded-key",
  // SSECustomerKeyMD5: "base64-encoded-md5",

  // --- Checksums (preferred over ContentMD5) ---
  // ChecksumAlgorithm: "CRC32", // or "CRC32C" | "SHA1" | "SHA256"
  // ChecksumCRC32: "...",
  // ChecksumCRC32C: "...",
  // ChecksumSHA1: "...",
  // ChecksumSHA256: "...",

  // --- Ownership/permissions context ---
  // ExpectedBucketOwner: "123456789012",
  // RequestPayer: "requester", // for requester-pays buckets

  // --- Object Lock (if bucket has it enabled) ---
  // ObjectLockMode: "GOVERNANCE", // or "COMPLIANCE"
  // ObjectLockRetainUntilDate: new Date(Date.now() + 7*24*3600*1000),
  // ObjectLockLegalHoldStatus: "ON" // or "OFF"
});

const response = await client.send(command);

// Optional: access response fields
// const { ETag, VersionId, ServerSideEncryption, SSEKMSKeyId } = response;

// Note: PutObject max size is 5 GB. Use Multipart Upload for larger objects.
""",
  "parameters": {
    "Bucket": "Target S3 bucket name. Required.",
    "Key": "Object key (path/filename within the bucket). Required.",
    "Body": "Object data: Uint8Array/Buffer/Blob/Readable stream/string.",
    "ContentType": "MIME type of the object (e.g., 'image/png').",
    "ACL": "Canned ACL (e.g., 'private', 'public-read'). Ignored if Object Ownership is BucketOwnerEnforced.",
    "Metadata": "User-defined metadata map (string keys/values).",
    "CacheControl": "Caching directives.",
    "ContentEncoding": "Content encodings applied to the object (e.g., 'gzip').",
    "ContentLanguage": "Language of the content.",
    "ContentDisposition": "Presentation style (e.g., 'inline' or 'attachment; filename=\"x\"').",
    "ContentLength": "Size in bytes (needed for some streams).",
    "ContentMD5": "Base64-encoded MD5 for integrity check (prefer checksum headers when possible).",
    "StorageClass": "Storage tier (e.g., 'STANDARD', 'STANDARD_IA', 'ONEZONE_IA', 'GLACIER', 'DEEP_ARCHIVE').",
    "Tagging": "URL-encoded tag string: 'k1=v1&k2=v2'.",
    "WebsiteRedirectLocation": "Redirect requests for this object to the specified location.",
    "ServerSideEncryption": "SSE at rest: 'AES256' (SSE-S3) or 'aws:kms' (SSE-KMS).",
    "SSEKMSKeyId": "KMS key ARN/ID when using 'aws:kms'.",
    "SSECustomerAlgorithm": "Algorithm for SSE-C, typically 'AES256'. Mutually exclusive with SSE-S3/SSE-KMS.",
    "SSECustomerKey": "Base64-encoded customer-provided key (SSE-C).",
    "SSECustomerKeyMD5": "Base64-encoded MD5 of the SSE-C key.",
    "ChecksumAlgorithm": "Checksum algorithm S3 validates (CRC32 | CRC32C | SHA1 | SHA256).",
    "ChecksumCRC32": "Checksum value for CRC32.",
    "ChecksumCRC32C": "Checksum value for CRC32C.",
    "ChecksumSHA1": "Checksum value for SHA1.",
    "ChecksumSHA256": "Checksum value for SHA256.",
    "ExpectedBucketOwner": "Account ID expected to own the bucket.",
    "RequestPayer": "Use 'requester' for requester-pays buckets.",
    "ObjectLockMode": "Object Lock mode if enabled: 'GOVERNANCE' or 'COMPLIANCE'.",
    "ObjectLockRetainUntilDate": "Retention timestamp for Object Lock.",
    "ObjectLockLegalHoldStatus": "'ON' or 'OFF' legal hold status."
  },
  "package": "@aws-sdk/client-s3"
},
    {
  "service": "s3",
  "method": "get_object",
  "description": "Retrieves an object from S3; supports range/conditional requests, header overrides, SSE-C decryption, checksums, and part-number retrieval for multipart objects.",
  "code": """import { S3Client, GetObjectCommand } from "@aws-sdk/client-s3";

const client = new S3Client({});

const command = new GetObjectCommand({
  // --- Required ---
  Bucket: "my-bucket",
  Key: "path/to/object.txt",

  // --- Optional ---
  // Range: "bytes=0-1048575",               // return only this byte range (206 Partial Content)
  // IfMatch: "\\"<ETAG>\\"",                // only if ETag matches (include quotes)
  // IfNoneMatch: "\\"<ETAG>\\"",            // return 304 if ETag matches (include quotes)
  // IfModifiedSince: new Date("2025-01-01"),
  // IfUnmodifiedSince: new Date("2025-01-01"),
  // VersionId: "3HL4kqtJlcpXrof3",
  // PartNumber: 1,                          // retrieve a specific part of a multipart object
  // ResponseCacheControl: "max-age=3600",   // override response headers (affects response only)
  // ResponseContentType: "text/plain",
  // ResponseContentDisposition: "attachment; filename=\\"export.txt\\"",
  // ResponseContentEncoding: "gzip",
  // ResponseContentLanguage: "en",
  // ResponseExpires: new Date(Date.now() + 3600_000),
  // ChecksumMode: "ENABLED",                // request checksum fields in response if available

  // SSE-C (customer-provided keys) — only for objects encrypted with SSE-C:
  // SSECustomerAlgorithm: "AES256",
  // SSECustomerKey: "<base64-encoded-key>",
  // SSECustomerKeyMD5: "<base64-encoded-md5>",

  // Ownership/permissions
  // ExpectedBucketOwner: "123456789012",
  // RequestPayer: "requester"               // for requester-pays buckets
});

const response = await client.send(command);

// Body is a stream. In Node.js 18+ you can do:
const bytes = response.Body ? await response.Body.transformToByteArray() : undefined;
const text  = bytes ? new TextDecoder().decode(bytes) : undefined;

// Common metadata fields:
// const { ETag, LastModified, ContentLength, ContentType, Metadata, VersionId } = response;

// Notes:
// - Range responses return 206 and ContentLength equals the range length.
// - Response* header overrides affect only the HTTP response, not the stored object.
// - SSECustomer* headers are for SSE-C objects and are mutually exclusive with SSE-S3/SSE-KMS.
""",
  "parameters": {
    "Bucket": "Name of the S3 bucket. Required.",
    "Key": "Full object key (path/filename). Required.",
    "Range": "Byte range to return (e.g., 'bytes=0-9'); response status is 206 Partial Content.",
    "IfMatch": "Return the object only if its ETag matches (include quotes around the ETag).",
    "IfNoneMatch": "Return 304 Not Modified if the ETag matches (include quotes).",
    "IfModifiedSince": "Return the object only if it has been modified since the given date.",
    "IfUnmodifiedSince": "Return the object only if it has not been modified since the given date.",
    "VersionId": "Retrieve a specific version of an object in a versioned bucket.",
    "PartNumber": "For multipart objects, return only the specified part.",
    "ResponseCacheControl": "Override Cache-Control header in the response.",
    "ResponseContentType": "Override Content-Type header in the response.",
    "ResponseContentDisposition": "Override Content-Disposition header in the response.",
    "ResponseContentEncoding": "Override Content-Encoding header in the response.",
    "ResponseContentLanguage": "Override Content-Language header in the response.",
    "ResponseExpires": "Override Expires header in the response.",
    "ChecksumMode": "Set to 'ENABLED' to include checksum response fields when available.",
    "SSECustomerAlgorithm": "Algorithm for SSE-C decryption (typically 'AES256').",
    "SSECustomerKey": "Base64-encoded customer-provided key for SSE-C decryption.",
    "SSECustomerKeyMD5": "Base64-encoded MD5 of the SSE-C key.",
    "ExpectedBucketOwner": "Account ID expected to own the bucket; request fails if different.",
    "RequestPayer": "Use 'requester' for requester-pays buckets."
  },
  "package": "@aws-sdk/client-s3"
},
    {
  "service": "s3",
  "method": "delete_object",
  "description": "Deletes an object from an S3 bucket. In versioned buckets, omitting VersionId adds a delete marker; providing VersionId deletes that specific version. In non-versioned buckets, the object is permanently deleted.",
  "code": """import { S3Client, DeleteObjectCommand } from "@aws-sdk/client-s3";

const client = new S3Client({});

const command = new DeleteObjectCommand({
  // --- Required ---
  Bucket: "my-bucket",
  Key: "path/to/object.txt",

  // --- Optional ---
  // VersionId: "3HL4kqtJlcpXrof3",       // delete a specific version (versioned buckets)
  // MFA: "arn:aws:iam::123456789012:mfa/user 123456", // required if MFA Delete is enabled
  // BypassGovernanceRetention: true,      // requires s3:BypassGovernanceRetention; Object Lock Governance mode
  // ExpectedBucketOwner: "123456789012",  // ensure bucket owner matches
  // RequestPayer: "requester"             // for requester-pays buckets
});

const response = await client.send(command);

// Success returns HTTP 204 and no body.
// In versioned buckets, response may include:
// const { DeleteMarker, VersionId, RequestCharged } = response;
""",
  "parameters": {
    "Bucket": "Name of the bucket containing the object. Required.",
    "Key": "Object key (path/filename). Required.",
    "VersionId": "If set, deletes that specific object version. If omitted in a versioned bucket, a delete marker is added.",
    "MFA": "Two-factor token in the format '<serial> <code>' (e.g., 'arn:aws:iam::123456789012:mfa/user 123456'). Required only if MFA Delete is enabled.",
    "BypassGovernanceRetention": "Bypass Object Lock Governance mode retention (requires 's3:BypassGovernanceRetention').",
    "ExpectedBucketOwner": "Account ID expected to own the bucket; the call fails if different.",
    "RequestPayer": "Set to 'requester' for requester-pays buckets."
  },
  "package": "@aws-sdk/client-s3"
},
    {
  "service": "s3",
  "method": "list_objects_v2",
  "description": "Lists objects in an S3 bucket (up to 1,000 per page) with support for prefixes, delimiters, pagination tokens, and optional owner/attribute fields.",
  "code": """import { S3Client, ListObjectsV2Command } from "@aws-sdk/client-s3";

const client = new S3Client({});

const command = new ListObjectsV2Command({
  // --- Required ---
  Bucket: "my-bucket",

  // --- Optional ---
  // Prefix: "path/to/",               // limit to keys beginning with this prefix
  // Delimiter: "/",                   // group by 'folders' -> returns CommonPrefixes
  // MaxKeys: 1000,                    // page size (max 1000)
  // StartAfter: "path/to/last-key",   // initial starting point (exclusive)
  // ContinuationToken: "<TOKEN>",     // use token from prior page for pagination
  // FetchOwner: true,                 // include Owner per object
  // EncodingType: "url",              // URL-encode keys in the response
  // OptionalObjectAttributes: ["RestoreStatus"], // request extra attributes when available
  // RequestPayer: "requester",        // requester-pays buckets
  // ExpectedBucketOwner: "123456789012"
});

const response = await client.send(command);

// Optional: access response fields
// const { Contents = [], CommonPrefixes = [], IsTruncated, NextContinuationToken } = response;

// Example: paginator
// let token;
// do {
//   const page = await client.send(new ListObjectsV2Command({
//     Bucket: "my-bucket",
//     ContinuationToken: token,
//     MaxKeys: 1000,
//     Prefix: "path/to/",
//     Delimiter: "/"
//   }));
//   (page.Contents || []).forEach(obj => {
//     // obj.Key, obj.Size, obj.LastModified, obj.StorageClass, obj.Owner, obj.ChecksumAlgorithm, ...
//   });
//   token = page.NextContinuationToken;
// } while (token);

// Notes:
// - Delimiter groups keys into CommonPrefixes to simulate folders; only that level appears in Contents.
// - StartAfter is for the first page; use ContinuationToken for subsequent pages.
// - This is not a version listing; use ListObjectVersions for versions.
""",
  "parameters": {
    "Bucket": "Name of the bucket to list. Required.",
    "Prefix": "Limit results to keys that begin with this prefix.",
    "Delimiter": "Group keys by a delimiter (commonly '/'); grouped prefixes are returned in CommonPrefixes.",
    "MaxKeys": "Maximum number of keys to return per page (up to 1000).",
    "StartAfter": "Key after which listing begins for the first page (exclusive).",
    "ContinuationToken": "Opaque token from the previous response to retrieve the next page.",
    "FetchOwner": "If true, includes the Owner field for each object.",
    "EncodingType": "If set to 'url', keys are URL-encoded in the response.",
    "OptionalObjectAttributes": "Request additional attributes per object (e.g., ['RestoreStatus']).",
    "RequestPayer": "Use 'requester' for requester-pays buckets.",
    "ExpectedBucketOwner": "Account ID expected to own the bucket; request fails if different."
  },
  "package": "@aws-sdk/client-s3"
},
    {
  "service": "s3",
  "method": "create_bucket",
  "description": "Creates a new S3 bucket; optionally specify region, ACL grants, and enable Object Lock at creation.",
  "code": """import { S3Client, CreateBucketCommand } from "@aws-sdk/client-s3";

const client = new S3Client({ /* region: "us-east-1" */ });

const command = new CreateBucketCommand({
  // --- Required ---
  Bucket: "my-unique-bucket-name-123", // 3–63 chars, lowercase, digits, hyphens; globally unique

  // --- Optional ---
  // When creating outside us-east-1, you must specify the region and it must match the client:
  // CreateBucketConfiguration: { LocationConstraint: "us-west-2" },

  // ACLs (ignored if Object Ownership is BucketOwnerEnforced; prefer policies/IAM)
  // ACL: "private", // e.g., "public-read", "public-read-write", "authenticated-read"

  // Object Lock (can only be enabled at creation; requires support in the account/region)
  // ObjectLockEnabledForBucket: true,

  // Grant headers (legacy-style grants)
  // GrantFullControl: "id=<canonicalId>",
  // GrantRead: "uri=http://acs.amazonaws.com/groups/global/AllUsers",
  // GrantReadACP: "id=<canonicalId>",
  // GrantWrite: "id=<canonicalId>",
  // GrantWriteACP: "id=<canonicalId>"
});

const response = await client.send(command);

// Optional: access response fields
// const { Location } = response;

// Notes:
// - If Block Public Access is enabled (recommended), ACLs will not make the bucket public.
// - To version, encrypt, or configure lifecycle rules, call the corresponding APIs after creation.
""",
  "parameters": {
    "Bucket": "Globally unique bucket name (3–63 chars, lowercase letters, numbers, hyphens). Required.",
    "CreateBucketConfiguration": "Region config required when creating outside us-east-1: { LocationConstraint: '<region>' }.",
    "ACL": "Canned ACL ('private', 'public-read', etc.). Ignored with BucketOwnerEnforced object ownership; prefer policies/IAM.",
    "ObjectLockEnabledForBucket": "Enable S3 Object Lock at creation; cannot be enabled later.",
    "GrantFullControl": "Grants full control to specified grantees (canonical ID/email/URI).",
    "GrantRead": "Grants READ permission to specified grantees.",
    "GrantReadACP": "Grants permission to read the bucket ACL.",
    "GrantWrite": "Grants WRITE permission to specified grantees.",
    "GrantWriteACP": "Grants permission to write the bucket ACL."
  },
  "package": "@aws-sdk/client-s3"
},
    {
  "service": "s3",
  "method": "copy_object",
  "description": "Creates a server-side copy of an existing S3 object to a destination bucket/key; supports metadata/tagging directives, encryption, and conditional copy.",
  "code": """import { S3Client, CopyObjectCommand } from "@aws-sdk/client-s3";

const client = new S3Client({});

const srcBucket = "source-bucket";
const srcKey = "path/to/source.txt";
const dstBucket = "dest-bucket";
const dstKey = "path/to/dest.txt";

// Build CopySource: include leading slash; URL-encode the key; append ?versionId=... if needed.
const copySource = `/${srcBucket}/${encodeURIComponent(srcKey)}`;
// const copySource = `/${srcBucket}/${encodeURIComponent(srcKey)}?versionId=<VERSION_ID>`;

const command = new CopyObjectCommand({
  // --- Required ---
  Bucket: dstBucket,
  Key: dstKey,
  CopySource: copySource,

  // --- Optional: metadata & tags ---
  // Metadata: { "x-app-id": "alpha" },
  // MetadataDirective: "REPLACE", // "COPY" (default) copies source metadata; "REPLACE" uses provided values
  // Tagging: "k1=v1&k2=v2",
  // TaggingDirective: "REPLACE",   // "COPY" to copy source tags

  // --- Optional: headers on destination (require REPLACE to take effect) ---
  // ContentType: "text/plain",
  // CacheControl: "max-age=3600",
  // ContentDisposition: "attachment; filename=\\"renamed.txt\\"",
  // ContentEncoding: "gzip",
  // ContentLanguage: "en",
  // Expires: new Date(Date.now() + 7*24*3600*1000),
  // WebsiteRedirectLocation: "/new/location",

  // --- Storage class ---
  // StorageClass: "STANDARD", // e.g., "STANDARD_IA" | "ONEZONE_IA" | "GLACIER" | "DEEP_ARCHIVE"

  // --- Conditional copy (applies to SOURCE) ---
  // CopySourceIfMatch: "\\"<ETAG>\\"",
  // CopySourceIfNoneMatch: "\\"<ETAG>\\"",
  // CopySourceIfModifiedSince: new Date("2025-01-01"),
  // CopySourceIfUnmodifiedSince: new Date("2025-01-01"),

  // --- Destination encryption (choose ONE family) ---
  // 1) SSE-S3:
  // ServerSideEncryption: "AES256",
  //
  // 2) SSE-KMS:
  // ServerSideEncryption: "aws:kms",
  // SSEKMSKeyId: "arn:aws:kms:us-east-1:123456789012:key/...",
  // BucketKeyEnabled: true, // S3 Bucket Keys with SSE-KMS
  //
  // 3) SSE-C for DESTINATION (mutually exclusive with SSE-S3/SSE-KMS):
  // SSECustomerAlgorithm: "AES256",
  // SSECustomerKey: "<base64-encoded-key>",
  // SSECustomerKeyMD5: "<base64-encoded-md5>",

  // --- If SOURCE object was encrypted with SSE-C, provide its keys to decrypt during copy ---
  // CopySourceSSECustomerAlgorithm: "AES256",
  // CopySourceSSECustomerKey: "<base64-encoded-key>",
  // CopySourceSSECustomerKeyMD5: "<base64-encoded-md5>",

  // --- Ownership/permissions ---
  // ACL: "private", // e.g., "public-read" | "bucket-owner-full-control" (ignored if BucketOwnerEnforced)
  // GrantFullControl: "id=<canonicalId>",
  // GrantRead: "uri=http://acs.amazonaws.com/groups/global/AllUsers",
  // GrantReadACP: "id=<canonicalId>",
  // GrantWriteACP: "id=<canonicalId>",
  // ExpectedBucketOwner: "123456789012",
  // ExpectedSourceBucketOwner: "123456789012",
  // RequestPayer: "requester",

  // --- Object Lock (destination bucket must have Object Lock enabled) ---
  // ObjectLockMode: "GOVERNANCE", // or "COMPLIANCE"
  // ObjectLockRetainUntilDate: new Date(Date.now() + 30*24*3600*1000),
  // ObjectLockLegalHoldStatus: "ON" // or "OFF"

  // --- Checksums on destination metadata (optional) ---
  // ChecksumAlgorithm: "CRC32" // or "CRC32C" | "SHA1" | "SHA256"
});

const response = await client.send(command);

// Optional: access response fields
// const { CopyObjectResult, VersionId, Expiration, ServerSideEncryption, SSEKMSKeyId } = response;

// Note:
// - CopyObject copies up to 5 GB per request. For larger objects, use multipart UploadPartCopy.
""",
  "parameters": {
    "Bucket": "Destination bucket name. Required.",
    "Key": "Destination object key. Required.",
    "CopySource": "Source in the form '/<src-bucket>/<url-encoded-src-key>' (append '?versionId=...' to target a specific version). Required.",
    "Metadata": "User-defined metadata to apply to the destination object. Requires MetadataDirective='REPLACE'.",
    "MetadataDirective": "'COPY' (default) to copy source metadata, or 'REPLACE' to use provided metadata/headers.",
    "Tagging": "URL-encoded tag string for the destination object (e.g., 'k1=v1&k2=v2').",
    "TaggingDirective": "'COPY' to copy source tags, or 'REPLACE' to use provided tags.",
    "StorageClass": "Destination storage class (e.g., 'STANDARD', 'STANDARD_IA', 'ONEZONE_IA', 'GLACIER', 'DEEP_ARCHIVE').",
    "Expires": "Sets the Expires header on the destination object.",
    "WebsiteRedirectLocation": "Redirect location for the destination object.",
    "CopySourceIfMatch": "Copy only if the source ETag matches (quote the ETag).",
    "CopySourceIfNoneMatch": "Copy only if the source ETag does not match (quote the ETag).",
    "CopySourceIfModifiedSince": "Copy only if the source was modified after this time.",
    "CopySourceIfUnmodifiedSince": "Copy only if the source was not modified after this time.",
    "ContentType": "Override Content-Type for the destination (requires MetadataDirective='REPLACE').",
    "CacheControl": "Override Cache-Control on the destination (requires 'REPLACE').",
    "ContentDisposition": "Override Content-Disposition on the destination (requires 'REPLACE').",
    "ContentEncoding": "Override Content-Encoding on the destination (requires 'REPLACE').",
    "ContentLanguage": "Override Content-Language on the destination (requires 'REPLACE').",
    "ServerSideEncryption": "Encrypt destination with 'AES256' (SSE-S3) or 'aws:kms' (SSE-KMS).",
    "SSEKMSKeyId": "KMS key ARN/ID when using 'aws:kms'.",
    "BucketKeyEnabled": "Enables S3 Bucket Keys for SSE-KMS.",
    "ChecksumAlgorithm": "Destination checksum algorithm: 'CRC32' | 'CRC32C' | 'SHA1' | 'SHA256'.",
    "CopySourceSSECustomerAlgorithm": "Algorithm for decrypting an SSE-C–encrypted source (typically 'AES256').",
    "CopySourceSSECustomerKey": "Base64-encoded customer key to decrypt the source (SSE-C).",
    "CopySourceSSECustomerKeyMD5": "Base64-encoded MD5 of the SSE-C source key.",
    "SSECustomerAlgorithm": "Algorithm for encrypting destination with SSE-C (typically 'AES256').",
    "SSECustomerKey": "Base64-encoded customer-provided key for SSE-C destination encryption.",
    "SSECustomerKeyMD5": "Base64-encoded MD5 of the SSE-C destination key.",
    "ACL": "Canned ACL for the destination object (ignored if Object Ownership is BucketOwnerEnforced).",
    "GrantFullControl": "Grants full control to specified grantees.",
    "GrantRead": "Grants READ permission to specified grantees.",
    "GrantReadACP": "Grants permission to read the ACL.",
    "GrantWriteACP": "Grants permission to write the ACL.",
    "ExpectedBucketOwner": "Expected account ID for the destination bucket.",
    "ExpectedSourceBucketOwner": "Expected account ID for the source bucket.",
    "RequestPayer": "Set to 'requester' for requester-pays buckets.",
    "ObjectLockMode": "'GOVERNANCE' or 'COMPLIANCE' (destination bucket must have Object Lock enabled).",
    "ObjectLockRetainUntilDate": "Retention timestamp for Object Lock.",
    "ObjectLockLegalHoldStatus": "'ON' or 'OFF' legal hold status."
  },
  "package": "@aws-sdk/client-s3"
},
    {
  "service": "s3",
  "method": "get_object_attributes",
  "description": "Returns selected attributes for an S3 object (e.g., ETag, checksum, size, storage class, and multipart part metadata) without returning the object body.",
  "code": """import { S3Client, GetObjectAttributesCommand } from "@aws-sdk/client-s3";

const client = new S3Client({});

const command = new GetObjectAttributesCommand({
  // --- Required ---
  Bucket: "my-bucket",
  Key: "path/to/object.txt",
  ObjectAttributes: ["ETag", "Checksum", "ObjectSize", "StorageClass", "ObjectParts"],

  // --- Optional ---
  // VersionId: "3HL4kqtJlcpXrof3", // specific version in a versioned bucket
  // MaxParts: 1000,                 // max parts to return when requesting ObjectParts
  // PartNumberMarker: 0,            // continue listing parts after this part number
  // ChecksumMode: "ENABLED",        // include checksum details when available
  // ExpectedBucketOwner: "123456789012",
  // RequestPayer: "requester"       // requester-pays buckets
});

const response = await client.send(command);

// Examples:
// const { ETag, Checksum, ObjectSize, StorageClass, ObjectParts } = response;
// if (ObjectParts) {
//   const { PartsCount, TotalPartsCount, IsTruncated, NextPartNumberMarker, PartNumberMarker } = ObjectParts;
// }

// Notes:
// - ObjectParts is relevant for objects uploaded via multipart upload.
// - Checksum details are included only if the object has stored checksums and ChecksumMode is 'ENABLED'.
""",
  "parameters": {
    "Bucket": "Name of the S3 bucket. Required.",
    "Key": "Object key (path/filename). Required.",
    "ObjectAttributes": "Array of attributes to return (e.g., 'ETag', 'Checksum', 'ObjectSize', 'StorageClass', 'ObjectParts'). Required.",
    "VersionId": "Return attributes for a specific object version in a versioned bucket.",
    "MaxParts": "Maximum number of parts to include when returning ObjectParts metadata.",
    "PartNumberMarker": "When listing ObjectParts, return parts after this part number (for pagination).",
    "ChecksumMode": "Set to 'ENABLED' to include checksum details if present for the object.",
    "ExpectedBucketOwner": "Account ID expected to own the bucket; the call fails if different.",
    "RequestPayer": "Use 'requester' for requester-pays buckets."
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
