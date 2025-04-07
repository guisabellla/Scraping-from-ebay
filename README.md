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

I searched for "bag women", "bowl", and "jewelry". These are the commands that I use to generate the 3 json files in my repository:
```
python3 ebay-dl.py bowl
python3 ebay-dl.py jewelry
python3 ebay-dl.py bag+women
```

### Course link

This project is produced under the instruction of [CMC-CSCI040/Project_03](https://github.com/mikeizbicki/cmc-csci040/tree/2025spring/project_03_webscraping).

