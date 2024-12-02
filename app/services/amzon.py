from AmazonSmartScraper.scraper import AmazonScraper
def get_all_asins(keyword, res, all_products, loop_all_pages):
    scraper = AmazonScraper(use_selenium_headers=True)

    # Get total pages from the initial response
    total_pages = res[1]

    # Loop through all pages to get ASINs if loop_all_pages is True
    for page in range(1, total_pages + 1):
        print(page)
        res = scraper.get_asins_by_keyword(keyword, page)

        # Extract new ASINs that are not already in the list
        new_asins = [asin['asin'] for asin in res[0] if not any(product['asin'] == asin['asin'] for product in all_products)]

        if not new_asins or not loop_all_pages:
            break

        asins = ','.join(new_asins)
        product_briefs = scraper.get_products_brief(asins)
        
    return product_briefs