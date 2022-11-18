CREATE TABLE Customers (
     CustomerID STRING(36) NOT NULL,
     CompanyName STRING(MAX) NOT NULL, 
     Name STRING(MAX) NOT NULL,
     Region STRING(MAX) NOT NULL,
     Address STRING(MAX) NOT NULL
) PRIMARY KEY (CompanyID);

CREATE TABLE Orders (
     OrderID STRING(36) NOT NULL, 
     OrderDate Date NOT NULL, 
     CustomerID STRING(36) NOT NULL,
     CONSTRAINT FK_Orders_Customers FOREIGN KEY (CustomerID) REFERENCES Customers (CustomerID)
) PRIMARY KEY (OrderID);

CREATE TABLE OrdersDetails (
    ProductID STRING(36) NOT NULL,
    Qty INT64 NOT NULL,
    Price FLOAT64
) PRIMARY KEY (ProductID)
  , INTERLEAVE IN PARENT Owners ON DELETE CASCADE;
