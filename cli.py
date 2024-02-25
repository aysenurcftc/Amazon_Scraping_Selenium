import argparse

from amazon_scraping import AmazonItem


def main():
    parser = argparse.ArgumentParser(description="Amazon Products Web Scraping Using Selenium")
    parser.add_argument("search_name", help="product to search")
    parser.add_argument("save_path", help="path to output xlsx file")
    parser.add_argument("max_page", help="max page number", type=int)
    args = parser.parse_args()
    
    item = AmazonItem()
    items = item.searchAmazonItemInformation(args.search_name)
    search_items = item.getAmzonItemInformation(items, args.max_page)
    save_items = item.saveResult(items, args.max_page, args.save_path)
    print(save_items)
    
    
if __name__ == "__main__":
    main()
    
    
    