from playwright.sync_api import Playwright,sync_playwright

search_text = "python"
base_url = "https://www.youtube.com"
expected_limit = 10


def you_tube(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()

    page = context.new_page()
    page.goto(base_url + "/")

    search_input = page.locator('//*[@id="search-input"]/input')
    search_input.click()
    search_input.fill(search_text)
    search_input.press('Enter')

    page.wait_for_timeout(5000)

    expected_links = []
    searched_titles = page.locator('a#video-title')

    for i in searched_titles.all():
        title_text = i.get_attribute("title").lower()
        if search_text in title_text:
            expected_links.append(base_url + i.get_attribute("href"))
            if len(expected_links) == expected_limit:
                break

    print(expected_links)
    context.close()
    browser.close()

with sync_playwright() as playwright:
    you_tube(playwright)