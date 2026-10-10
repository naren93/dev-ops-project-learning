## SQL server based platform choices
- Azure SQL Databases (PAAS)
- Azure SQL Managed Instances (Full IAAS)
- Using SQL Server on Virtual Machines (Near full SQL Server Compatibility)
- SQL Database in Microsoft Fabric (OLTP with build in analytics)

## Roles played by a table
> OLTP - Transactional records, row by row
> Analytics - Facts and Dimentions, tables
> - Design follows the role - every choice gets cascaded.

## The Four design habits
- Right-sized data types
- Estimate table size early
- Enforce constraints
- Index strategically

## Data types 
- Numeric -> INT, BIGINT, DECIMAL
- STRING -> varchar, char, nvarchar
- Date/time -> DATE, DATETIME2
- Binary -> VARBINARY for files
- Special -> GUID, XML, JSON

### Examples for good table design
```sql
-- Estimate row size for a table
-- Fixed-length columns: sum of column sizes
-- Variable-length: estimate average size
-- Example row calculation:
CREATE TABLE Employee (
    EmployeeID INT,              -- 4 bytes
    FirstName NVARCHAR(50),      -- ~2-100 bytes (avg 40)
    LastName NVARCHAR(50),       -- ~2-100 bytes (avg 40)
    HireDate DATE,               -- 3 bytes
    Salary DECIMAL(10,2)         -- 5 bytes
);  
-- Estimated row size: 4 + 40 + 40 + 3 + 5 = ~92 bytes
-- Plus row overhead (~7 bytes) = ~99 bytes per row
-- 1 million rows ≈ 94 MiB
```
``` sql
CREATE TABLE Product (
    ProductID INT PRIMARY KEY IDENTITY(1,1),       -- Auto-incrementing surrogate key (4 bytes)
    ProductName NVARCHAR(100) NOT NULL,             -- Unicode support, appropriate length, enforced
    Category NVARCHAR(50) NOT NULL,                 -- Smaller than ProductName (categorization needs less space)
    Price DECIMAL(10,2) NOT NULL,                   -- Exact precision for financial data
    StockQuantity INT NOT NULL DEFAULT 0,           -- Integer sufficient for inventory, default prevents nulls
    LastRestocked DATETIME2 DEFAULT GETUTCDATE()    -- Modern date type with automatic timestamp
);
```

## Design best practice 
- Use appropriate data types - Smaller data types reduce storage and improve performance
- Consider table size early - Estimate row size and total table size to plan storage and indexing
- Implement meaningful constraints - Ensure data quality at the database level
- Plan for growth - Design tables to handle future data volume
- Index strategically - Index columns used in WHERE, JOIN, and ORDER BY clauses
- Choose columnstore for analytics - Use columnstore indexes for large tables with analytical queries
- Normalize when appropriate - Balance normalization with query performance needs
- Monitor row and page compression - Enable compression for large tables to save 

## Optimize with indices
### Row store index types
> Clustered index -> sort rows by keys - one per table
> Nonclustered index -> seperate structure pointing to rows, many per table

### Two strorage formats 
> Row store -> OLTP, keeps rows together 
> Column store -> analytics, stores columns seperately
- Pick your choice by work load -> whole record vs wide scans

