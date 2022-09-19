# Spanner Course Outline

## Who Should Attend
Database administrators, programmers, and cloud architects and engineers who want to learn how to create and operate SPanner databases and migrate existing databases into Spanner. 

## Prerequisites
This course is not an introduction to Google Cloud. Some prior Google Cloud experience is assumed. Experience with relational databases and the SQL language are also assumed. 

## Modules
1. The Need for Spanner
1. Getting Started with Spanner
1. Optimizing Spanner Schemas
1. Queries and Transactions
1. Programming Spanner Applications
1. Spanner Administration

## Detailed Outline
1. The Need for Spanner
    * What is Spanner
        * History
    * Features
        * Scalability
        * Performance and Latency
        * High Availability
        * Security
        * Integration
        * Google and PostgreSQL 
        * Operations and Monitoring
    * Use Cases

1. Getting Started with Spanner
    * Creating Spanner Instances
        * Regional Configuration
        * Multi-Regional Configuration
        * Capacity
        * Nodes
        * Processiing Units
        * Capacity Guidance
        * Cost
    * Creating Databases
        * Creating a Database
        * Choosing a Dialect
        * Google Standard SQL versus PostgreSQL
        * Creating Tables
        * CREATE TABLE DDL
        * Data Types
        * Primary Keys
        * Creating Indexes
        * INSERT
        * UPDATE
        * SELECT
        * DELETE
        * __Lab: Creating Spanner Databases (Console)__
    * Automating Spanner Instances
        * Google Cloud SDK
        * gcloud CLI
        * Code Example: CLI
        * Terraform
        * Code Example: Terraform
        * CLI
        * Terraform
        * __Lab: Creating Spanner Databases (CLI and Terraform)__

1. Optimizing Spanner Schemas
    * Spanner Architecture
        * Nodes
        * Splits
        * Difference with traditional RDBMS
    * Choosing Primary Keys
        * Hotspots
        * Avoiding Hotspots
        * UUIDs as Primary Keys
        * Using Timestamps in Primary Keys
        * Using Sequences in Primary Keys
        * Code Example: Using UUIDs
        * Code Example: Bit Reversing
        * __Lab: Choosing Primary Keys__
    * Defining Database Schemas
        * Indexes
        * Relationships 
        * Constraints
        * Interleaved Tables
        * __Lab: Managing Relationships with Foreign Keys and Interleaved Tables__

1. Queries and Transactions
    * Running Queries
        * Strong Reads
        * Stale Reads
        * Reading Data in Parallel
        * __Lab: Running Queries__
    * Running Transactions
        * ACID Transactions
        * Running Transactions
        * Read-Write Transactions
        * __Lab: Managing Transactions__

1. Programming Spanner Applications
    * Authentication and Authorization
        * IAM
        * Spanner Roles
        * Service Accounts
        * Service Account Keys
        * Using Service Accounts
    * Using the Language APIs
        * Client Libraries (Python Examples)
        * Creating Instances
        * Creating Databases
        * Creating Schemas
        * CRUD
        * Running Queries
        * __Lab: Programming Spanner Applications with Python__
    * Using Spanner from Applications
        * JDBC Driver
        * PostgreSQL Interface
        * Cloud Functions
        * Cloud Run
        * __Lab: Deploying Spanner Applications with Cloud Functions and Cloud Run__
    * Building Data Pipelines
        * Dataflow
        * Migrating data to Spanner
        * Exporting Spanner Data to BigQuery
        * __Lab: Intergrating Data Pipelines with Spanner__

1. Spanner Administration
    * Managing Data
        * Backup
        * Restore
        * Exporting Data
        * Bulk Imports
        * __Lab: Spanner Administraton__
    * Managing Change
        * Altering Spanner Schemas
        * Altering Tables
        * Limitations
        * Change Streams
        * __Lab: Altering Spanner Database Schema__
    * Operations
        * Monitoring
        * Logging 
        * __Lab: Spanner Monitoring and Logging__
    * Performance Best-Practices
        * Bulk loading best practices
        * DML best practices
        * Query plan visualizer
        * Troubleshooting latency
        * Using statistics (read, transaction, lock)
        * Request and transaction tags
        * Sessions

1. Capstone Project
    * Priovide the students with a CSV dump of relational data in Google Cloud Storage. Tell them to migrate the data into Spanner any way they want to based on what they have learned in the class. They can using Terraform, the CLI, Python, the Console, or a combination of those tools. 


## Hands-On Labs
* __Lab: Creating Spanner Databases (Console)__
* __Lab: Creating Spanner Databases (CLI and Terraform)__
* __Lab: Choosing Primary Keys__
* __Lab: Managing Relationships with Foreign Keys and Interleaved Tables__
* __Lab: Running Queries__
* __Lab: Managing Transactions__
* __Lab: Programming Spanner Applications with Python__
* __Lab: Deploying Spanner Applications with Cloud Functions and Cloud Run__
* __Lab: Intergrating Data Pipelines with Spanner__
* __Lab: Spanner Administraton__
* __Lab: Altering Spanner Database Schema__
* __Lab: Spanner Monitoring and Logging__