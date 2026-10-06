# BurrowScout

BurrowScout is an open-source Python data collection and processing tool designed to gather publicly available wage, salary, award, and employment-market information from permitted web sources. The project provides a structured pipeline for retrieving source data, extracting relevant employment and remuneration fields, validating and normalising records, removing duplicates, and preserving provenance so that every data point can be traced back to its original source. BurrowScout is being developed incrementally from a single-source web scraper into a modular, multi-source data collection platform with configurable scheduling, logging, error handling, historical run tracking, structured exports, and extensible scraper adapters. Its primary initial use case is collecting wage and pay-rate information relevant to employment in South Australia, with the longer-term goal of supplying reliable structured labour-market data to other BurrowWerks projects such as BurrowForage, while remaining useful as an independent data collection tool. BurrowScout prioritises responsible data collection, transparent source attribution, maintainable architecture, and compliance with source-specific access requirements.

## Requirements

- Python 3.12+

## Installation

Clone the repository and enter the project directory.

Create a virtual environment:

```bash
python -m venv .venv
```
