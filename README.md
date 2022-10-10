# Google Cloud Spanner
2-Days

## Objectives
* Build scalable, managed, relational databases using Google Cloud Spanner 
* Create and manage databases using the CLI, Terraform, Python API,  and the Cloud Console
* Optimize relational database schemas for Spanner's distributed database model
* Program and run queries and transactions using the Spanner API
* Integrate Spanner with your applications
* Leverage Google tools for administering Spanner databases and managing data

## Who Should Attend
Database administrators, programmers, and cloud architects and engineers who want to learn how to create and operate Spanner databases and migrate existing databases into Spanner. 

## Prerequisites
This course is not an introduction to Google Cloud. Some prior Google Cloud experience is assumed. Experience with relational databases, the SQL language, and some programming is also assumed. 

## Modules
1. The Need for Spanner
1. Getting Started with Spanner
1. Optimizing Spanner Schemas
1. Queries and Transactions
1. Programming Spanner Applications
1. Spanner Administration
1. Capstone Project

## Detailed Outline
1. The Need for Spanner
    * What is Spanner
    * History
    * Use Cases

1. Getting Started with Spanner
    * Planning Spanner Instances
        * Regional Configuration
        * Multi-Regional Configuration
        * Capacity
        * Nodes
        * Processiing Units
        * Capacity Guidance
        * Cost
        * __Lab: Creating Spanner Instances (Console)__
    * Automating Instance Creation
        * Automating Spanner Instances
        * Google Cloud SDK
        * gcloud CLI
        * Code Example: CLI
        * Terraform
        * Code Example: Terraform
        * __Lab: Creating Spanner Instances (CLI and Terraform)__
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

1. Programming Spanner Applications, Queries, and Transactions
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
    * Running Queries
        * Strong Reads
        * Stale Reads
        * Using Indexes
    * Running Transactions
        * Transaction Types
        * External Consistency
        * Read-Write Transactions
        * Partitioned DML
        * Read-Only Trasactions
        * __Lab: Running Queries and  Transactions__

1. Deploying Spanner Applications
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
        * __Lab: Migrating Data to and from Spanner with Dataflow__

1. Spanner Administration
    * Managing Data
        * Backup
        * Restore
        * Exporting Data
        * Bulk Imports
    * Managing Change
        * Altering Spanner Schemas
        * Altering Tables
        * Limitations
        * Change Streams
    * Operations
        * Monitoring
        * Logging 
    * Performance Best-Practices
        * Bulk loading best practices
        * DML best practices
        * Query plan visualizer
        * Troubleshooting latency
        * Using statistics (read, transaction, lock)
        * Request and transaction tags
        * Sessions
        * __Lab: Administering Spanner Databases__

1. Capstone Project


## Labs
* __Lab: Creating Spanner Instances (Console)__
* __Lab: Creating Spanner Instances (CLI and Terraform)__
* __Lab: Creating Spanner Databases (Console)__
* __Lab: Creating Spanner Databases (CLI and Terraform)__
* __Lab: Choosing Primary Keys__
* __Lab: Managing Relationships with Foreign Keys and Interleaved Tables__
* __Lab: Running Queries and Transactions__
* __Lab: Programming Spanner Applications with Python__
* __Lab: Deploying Spanner Applications with Cloud Functions and Cloud Run__
* __Lab: Migrating Data to and from Spanner with Dataflow__
* __Lab: Administering Spanner Databases__
