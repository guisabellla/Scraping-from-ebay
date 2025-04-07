# Project03: Web Scraping from Ebay

This project scraps information from ebay and store results in json files.

## Explanation the ebay-dl.py file

The ebay-dl.py file allows search term in the command line, downloads the first 10 webpages of the product in the selected search term, and extract the results. Searched results are stored as JSON files named based on `args.search_term`.

The extracted items that are used to analyze each product includes:
- Name
- Price: in unit of cents instead of dollars
- Status: determines if the product is brand-new, pre-owned, or refurbished
- Shipping: gives the shipping fee in cents, and gives 0 if the product could be shipped for free
- Free-returns: determines if the product has free returns
- Items-sold: number of items sold, and if the information is not presented on the website at all, the result of this part would be "null"

## Instruction running the ebay-dl.py file




    what your ebay-dl.py file does

    how to run your ebay-dl.py file, using markdown code block(s) (and not inline code annotations) to show the exact commands that should be run to generate the 3 json files in your repo

    a link to the course project
