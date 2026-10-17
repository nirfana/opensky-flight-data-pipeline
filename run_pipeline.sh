#!/bin/bash

PROJECT_DIR="/home/nirfana/de-portfolio-project"
cd $PROJECT_DIR
source venv/bin/activate

echo "--- 1. Running Ingestion ---"
if ! python pipeline/ingest.py; then
    python pipeline/alert.py "Ingestion failed: Unable to fetch OpenSky API vectors." true
    exit 1
fi

echo "--- 2. Running Data Quality Scan ---"
if ! soda scan -d analytics -c observability/soda_configuration.yml observability/soda_checks.yml; then
    python pipeline/alert.py "Soda Core data quality checks failed! Schema or data anomaly detected." true
    exit 1
fi

echo "--- 3. Running dbt Transformations ---"
cd transformations
if ! dbt run; then
    python pipeline/alert.py "dbt model transformations failed execution." true
    exit 1
fi

if ! dbt test --select stg_flights fct_country_flight_stats; then
    python pipeline/alert.py "dbt data tests failed on flight models." true
    exit 1
fi
cd ..

echo "--- Pipeline execution complete ---"