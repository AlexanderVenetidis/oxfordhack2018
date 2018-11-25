import boto3

# Get the service resource.
dynamodb = boto3.resource('dynamodb')

# Create the DynamoDB table.
table = dynamodb.create_table(
    TableName='Frames',
    KeySchema=[
        {
            'AttributeName': 'Frame',
            'KeyType': 'HASH'
        },
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'Frame',
            'AttributeType': 'N'
        },
    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 40,
        'WriteCapacityUnits': 40
    }
)

# Wait until the table exists.
table.meta.client.get_waiter('table_exists').wait(TableName='Frames')

# Print out some data about the table.
print(table.item_count)
