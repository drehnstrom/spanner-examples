# Managing Relationships with Foreign Keys and Interleaved Tables

## Overview

In this lab, you will create a database with multiple tables, and use both primary-foreign key contraints, and interleaved tables to manage relationships. 

## Objectives

In this lab, you learn how to:
* Create a relational database with proper primary keys and relationships optimized for Spanner 

## Setup and Requirements

![[/fragments/start-qwiklab]]

![[/fragments/cloudshell]]

## Task 1. Creating on Orders database

1. In previous labs, you have learned how to create Spanner instances, databases, and tables using the Google Cloud Console, the gcloud CLI, and Terraform. Using the methood of your choice, create a database with the following criteria. _Feel free to modify the details if you like, or even use your own use case. The point is to create the database and tables without detailed instructions._ 

### __Database name:__ orders-db

### __Tables:__ Customer, Orders, OrderDetails

### __Customers table__

| Fields         
|----------------
| Company        
| Name           
| Region         
| Address        

### __Orders table__
| Fields          
|----------------
| Date           
| Customer       
| Address        

### __OrderDetails table__

| Fields         
|---------------
| Qty           
| Product       
| Price         

### __Data types and primary keys__
It is up to you what data types to use, and how to create the primary keys 

### __Relationships__

Customers have 0 or more Orders
* Use a primary-foreign key relationship between the Customers and Orders table

Orders have 1 or more Details
* Use an interleaved table for the relationship between the Orders and OrderDetails table

## To help, below are sample DDL statements for the Pets database you used earlier

### Owners table

```
CREATE TABLE Owners (
     OwnerID STRING(36) NOT NULL, 
     OwnerName STRING(MAX) NOT NULL
) PRIMARY KEY (OwnerID);
```

### Pets table with Primary Foreign keys

```
CREATE TABLE Pets (
     PetID STRING(36) NOT NULL, 
     OwnerID STRING(36) NOT NULL, 
     PetType STRING(MAX) NOT NULL,
     PetName STRING(MAX) NOT NULL,
     Breed STRING(MAX) NOT NULL,
     CONSTRAINT FK_OwnerPet FOREIGN KEY (OwnerID) REFERENCES Owners (OwnerID),
) PRIMARY KEY (PetID);
```

### Pets table interleaved with Owners

```
CREATE TABLE Pets (
     OwnerID STRING(36) NOT NULL, 
     PetID STRING(MAX) NOT NULL,     
     PetType STRING(MAX) NOT NULL,
     PetName STRING(MAX) NOT NULL,
     Breed STRING(MAX) NOT NULL,) 
     PRIMARY KEY (OwnerID,PetID),
     INTERLEAVE IN PARENT Owners ON DELETE CASCADE;
```



### **Congratulations!** You have created a database with multiple tables, and used both primary-foreign key contraints, and interleaved tables to manage relationships.


![[/fragments/endqwiklab]]

![[/fragments/copyright]]
