provider "aws" {
  region = "us-east-1"  
}

module "bedrock_kb" {
  source = "../modules/bedrock_kb" 

  knowledge_base_name        = "my-bedrock-kb"
  knowledge_base_description = "Knowledge base connected to Aurora Serverless database"

  aurora_arn        = "arn:aws:rds:us-east-1:522631657716:cluster:my-aurora-serverless" #TODO Update with output from stack1
  aurora_db_name    = "myapp"
  aurora_endpoint   = "my-aurora-serverless.cluster-c9uagdxjd488.us-east-1.rds.amazonaws.com" # TODO Update with output from stack1
  aurora_table_name = "bedrock_integration.bedrock_kb"
  aurora_primary_key_field = "id"
  aurora_metadata_field = "metadata"
  aurora_text_field = "chunks"
  aurora_verctor_field = "embedding"
  aurora_username   = "dbadmin"
  aurora_secret_arn = "arn:aws:secretsmanager:us-east-1:522631657716:secret:my-aurora-serverless-xD97to" #TODO Update with output from stack1
  s3_bucket_arn = "arn:aws:s3:::bedrock-kb-522631657716" #TODO Update with output from stack1
}