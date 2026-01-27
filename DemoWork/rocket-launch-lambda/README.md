# Rocket Launch Lambda Function

Lambda function triggered by Bedrock Action to simulate rocket launch.

## Functionality
- Writes rocket launch report to S3 bucket
- Returns success response with launch details

## Event Parameters
- `bucket_name` (optional): S3 bucket name (default: 'rocket-launch-logs')
- `rocket_name` (optional): Rocket identifier (default: 'Falcon-9')

## IAM Permissions Required
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "s3:PutObject",
      "Resource": "arn:aws:s3:::rocket-launch-logs/*"
    }
  ]
}
```

## Response Format
```json
{
  "statusCode": 200,
  "body": {
    "message": "Successfully launched rocket Falcon-9!",
    "launch_time": "2024-01-15T10:30:00.000000",
    "log_file": "launch-2024-01-15T10:30:00.000000.txt"
  }
}
```
