import os
from playwright.sync_api import sync_playwright

search_query = input("Enter what you want to search: ")

use_tavily = os.environ.get("USE_TAVILY", "").lower() in ("1", "true", "yes")
tavily_api_key = os.environ.get("TAVILY_API_KEY")

if use_tavily and tavily_api_key:
    from tavily import TavilyClient

    client = TavilyClient(api_key=tavily_api_key)
    response = client.search(query=search_query, max_results=3)

    print("\nTop Search result:\n")

    for i, result in enumerate(response["results"]):
    	print(f"{i+1}. {result['title']}")
    	print(result["url"])

    print("\n")
else:
    with sync_playwright() as p:

        browser = p.chromium.launch(headless=False)

        page = browser.new_page()

        page.goto("https://google.com")

        page.fill("textarea[name='q']", search_query)

        page.keyboard.press("Enter")

        page.wait_for_timeout(5000)

        links = page.locator("a h3")

        results = page.locator("div.yuRUbf a")

        print("\nTop Search result:\n")

        for i in range(3):
        	title = page.locator("div.yuRUbf h3").nth(i).inner_text()
        	link = results.nth(i).get_attribute("href")
        	print(f"{i+1}. {title}")
        	print(link)
        print("\n Opening the first result...\n")

        links.nth(0).click()

        input("\nPress Enter to close browser")

        browser.close()
