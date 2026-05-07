# Retail Sales Data Warehouse – ETL & Data Quality Validation

## Overview

This project implements an end-to-end Retail Sales Data Warehouse using Medallion Architecture (Bronze → Silver → Gold). The solution includes:

- Full & Incremental ETL Loads
- SCD Type-2 Implementation
- Data Quality Validation
- Fact & Dimension Modeling
- File Archival Automation
- Gold Layer Reporting

---

# Architecture

```text
Raw Files
   ↓
Bronze Layer
   ↓
Silver Layer
   ↓
Gold Layer
   ↓
Validation & Reporting
```

---

# Technologies Used

- Databricks
- SQL
- Python
- AWS S3
- Delta Lake
- GitHub

---

# Project Structure

```text
├── bronze_script
├── silver_script
├── silver_incremental_script
├── gold_script
├── archival_script
└── validation_script
```

---

# Source Files

- customers_src.csv
- products_src.csv
- stores_src.csv
- sales_transactions_src.csv

---

# Bronze Layer

Stores raw ingested data from source files.

Tables:
- customers_raw
- products_raw
- stores_raw
- sales_raw

---

# Silver Layer

Performs cleansing, transformations, and dimensional modeling.

## DimCustomer (SCD Type-2)

Features:
- Historical tracking
- Active/Inactive records
- Incremental customer updates

Transformations:
- Proper Case
- Lowercase
- Trim

## DimProduct
- Static dimension
- Product transformations

## DimStore
- Store dimension processing

## FactSales
- Transaction-level fact table
- Amount derivation
- Duplicate prevention

```text
Amount = Quantity × UnitPrice
```

---

# Gold Layer

Business-ready reporting tables:

- DailySalesSummary
- StoreSalesSummary
- ProductCategorySummary
- CustomerSalesSummary
- RegionSalesSummary

---

# Incremental Load Strategy

## DimCustomer
- SCD Type-2 logic
- Expire old records
- Insert updated records
- Preserve history

## DimProduct & DimStore
- Truncate + Reload

## FactSales
- Insert only new transactions
- Duplicate prevention using TransactionID

---

# Archival Automation

Python-based archival process:

- Moves old files to archive
- Keeps only latest active file
- Supports raw and processed zones
- Uses timestamp-based file detection

File naming convention:

```text
<filename>_DDMMYYYY_HHMMSS.csv
```

---

# Validation Coverage

The validation framework includes:

- Source-to-target validation
- Duplicate checks
- Null validation
- Referential integrity
- SCD Type-2 validation
- Amount calculation validation
- Gold layer reconciliation
- Incremental load validation

---

# Pipeline Flow

## Full Load

```text
archive_script
    ↓
bronze_script
    ↓
silver_script
    ↓
gold_script
    ↓
validation_script
```

## Incremental Load

```text
archive_script
    ↓
bronze_script
    ↓
silver_incremental_script
    ↓
gold_script
    ↓
validation_script
```

---

# Key Features

- Medallion Architecture
- SCD Type-2
- Incremental ETL
- Delta Lake Processing
- Automated Archival
- ETL Validation Framework
- Gold Layer Reporting

---

# Conclusion

This project demonstrates a complete enterprise-style ETL and Data Warehouse implementation with:

- Historical data tracking
- Incremental processing
- Automated archival
- Data quality validation
- Reporting-ready Gold layer

The architecture closely aligns with real-world ETL and Data Engineering workflows.

