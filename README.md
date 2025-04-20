# Stock & Mutual Fund NAV Scraper

Designed to scrape the latest Net Asset Value (NAV) or closing prices of stocks and mutual funds. Uses external APIs to gather stock market data and updates an SQLite database with the scraped results.

## Overview

The script performs the following tasks:

1. **Reads Stock and Holdings Information**
2. **Merges Data** : Merges data based on ISIN codes.
3. **Scrapes NAV/Closing Price** : Scrapes NAV for MF or closing prices for stocks.
4. **Stores Data** : Saves scraped data into an SQLite database.

## Features

- **Asynchronous Requests** : Uses `httpx` and `asyncio` for non-blocking, concurrent API requests.
- **Rate Limiting** : Implements rate limiting with `aiolimiter` to avoid overloading the APIs.
- **Data Storage** : The scraped data is stored in `SQLite` database for easy access.
- **Error Handling** : Handles potential API failures.

## Installation & Setup

1. **Clone the Repository**

   - ```bash
      git clone https://github.com/jishnukoliyadan/NAV_Scrapper.git
      cd NAV_Scrapper
      ```
2. **Create new virtual environment using [AStRAL's uv](https://docs.astral.sh/uv/)**
   - [Install uv](https://docs.astral.sh/uv/getting-started/installation/#installing-uv) if you haven't already. Then, run the following command to set up the environment :
   - ```bash
      uv venv
      ```
3. **Sync project dependencies with the environment.**
   - ```bash
      uv sync
      ```

## File Structure

``` bash
NAV_Scrapper/
├── .gitignore            # Ignores files from version control.
├── .python-version       # Specifies Python version to be used.
├── data.json             # JSON data storage, for troubleshooting.
├── DB_Instance
│   └── folio_NAV.db      # SQLite database for storing scraped data.
├── holdings-XXXXXX.xlsx  # Excel file with holdings data.
├── LICENSE               # Project License.
├── NAV_Scrapper.py       # The python scraping script.
├── pyproject.toml        # Project config and dependencies.
├── README.md             # Project documentation.
├── Ticker_Info.csv       # CSV file with ticker information.
└── uv.lock               # Dependency lock file (uvicorn).
```

## Configuration

- **TEST Mode** : You can run the scraper in **TEST** mode by setting `TEST = True` in the script. In this mode, the actual API calls will be skipped and mocked with a default value (0).
- **File Paths** : The script assumes the following files exist in the project directory:
    - `Ticker_Info.csv` : A CSV containing stock ticker data.
    - `holdings-XXXXXX.xlsx` : An Excel file with your holdings data.
    - The SQLite database (`folio_NAV.db`) will be created inside the `DB_Instance` directory.

## Running the Script

- To run the script using the **uv**-managed environment :
    - ```bash
      uv run NAV_Scrapper.py
      ```
- Or alternatively, after activating the environment :
    - ```bash
      source .venv/bin/activate
      python NAV_Scrapper.py
      ```

**Note :** The `uv run` command automatically uses the virtual environment's Python interpreter if we're in the project directory with a `.venv` folder.

## Troubleshooting

- **Missing Tickers** : If there are missing tickers in the `Ticker_Info.csv`, the script will raise an assertion error (`assert len(missing_) == 0`), which will output the missing tickers.

## Automating Script Execution with `Cron`

To automate the execution of the above script, we can set up a **`cron`** job that will run the scraper at scheduled intervals.

### Setting Up a Cron Job

1. **Open the Crontab Editor** :

    Run the following command to open the crontab editor :

    ``` bash
    crontab -e
    ```
2. **Add the Cron Job** :

    Schedule the script to run at specific intervals. For example, to run at *every day* on *10 PM* :
    1. Assuming script is stored at directory `/home/user/.NAV_Scrapper`.
    2. Using the created `uv` environment's `python`, then,
    
    ``` bash
    0 22 * * * ~/.NAV_Scrapper/.venv/bin/python ~/.NAV_Scrapper/NAV_Scrapper.py
    ```

1. **Save and Exit** :

    - If you’re using nano, save with `Ctrl + O`, press `Enter`, then exit with `Ctrl + X`.
    - If you're using **vim**, save and exit with `:wq`.

1. **Verify Cron Jobs** :

    Check scheduled cron jobs by running :

    ``` bash
    crontab -l
    ```

## License

This project is licensed under the [MIT License](LICENSE).
