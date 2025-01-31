# Lenovo Warranty Scraper

A Python-based web scraper to extract warranty information from Lenovo's support website.

## Description

This project provides a tool for automating the process of retrieving warranty information for Lenovo products using their serial numbers. It uses Selenium WebDriver to navigate Lenovo's support website and extract detailed warranty data.

## Features

- Automated serial number lookup
- Detailed warranty information extraction
- Headless browser support
- Docker containerization
- Configurable Chrome options
- Comprehensive error handling

## Prerequisites

- Python 3.x
- Docker (optional)
- Chrome browser

## Installation

1. Clone the repository:

```bash
git clone [repository-url]
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Running with Python

```python
from lenovo_scrapper.scraper import LenovoWarrantyScraper
# See main.py for example usage
```

### Running with Docker

```bash
docker build -t lenovo-scraper .
docker run lenovo-scraper
```

## Project Structure

```
├── src/
│   └── lenovo_scrapper/
│       ├── browser/         # Browser configuration
│       ├── config/          # Settings and selectors
│       ├── utils/           # Utility functions
│       └── scraper.py       # Main scraper logic
├── Dockerfile
├── requirements.txt
└── README.md
```

## Configuration

See `config/setting.py` for configurable options including:

- Base URL
- Timeout settings
- User agent configuration
- Chrome browser options

## Error Handling

The scraper includes comprehensive error handling for:

- Network issues
- Element location failures
- Timeout scenarios
- Browser automation errors

## License

[License Type] - See LICENSE file for details

## Authors

Luis Angel Soler Ramirez
