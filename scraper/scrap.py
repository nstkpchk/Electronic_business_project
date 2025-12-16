import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import re
from urllib.parse import urljoin
import random


CATEGORY_BASE_URL = "https://sklepkoszykarski.pl/"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}


def get_categories_and_subcategories(base_url):
    categories = []

    try:
        response = requests.get(base_url, headers=HEADERS)
        if response.status_code != 200:
            print("Error loading base page")
            return categories

        soup = BeautifulSoup(response.content, 'html.parser')

        main_menu_container = soup.find('li', id='hcategory_0')
        if not main_menu_container:
            print("Main menu container not found")
            return categories

        menu = main_menu_container.find('ul', class_='level1')
        if not menu:
            print("Level1 menu not found")
            return categories

        for cat_li in menu.find_all('li', recursive=False):
            cat_h3 = cat_li.find('h3')
            cat_a = cat_h3.find('a', href=True) if cat_h3 else None
            if not cat_a:
                continue

            cat_name = cat_a.text.strip()
            cat_url = urljoin(base_url, cat_a['href'])

            subcats = []
            sub_ul = cat_li.find('ul', class_='level2')
            if sub_ul:
                for sub_li in sub_ul.find_all('li', recursive=False):
                    sub_h3 = sub_li.find('h3')
                    sub_a = sub_h3.find('a', href=True) if sub_h3 else None
                    if not sub_a:
                        continue
                    sub_name = sub_a.text.strip()
                    sub_url = urljoin(base_url, sub_a['href'])
                    subcats.append({
                        'name': sub_name,
                        'url': sub_url
                    })

            categories.append({
                'name': cat_name,
                'url': cat_url,
                'subcategories': subcats
            })

    except Exception as e:
        print(f"Error while parsing category: {e}")

    return categories

def prepare_categories_for_csv(categories_tree):
    csv_rows = []

    for cat in categories_tree:
        # Parent category
        cat_row = {
            'Aktywny (0 lub 1)': 1,
            'Nazwa': cat['name'],
            'Kategoria nadrzędna': 'Home',
            'Główna kategoria (0/1)': 0
        }
        csv_rows.append(cat_row)
        parent_name = cat['name']

        # Subcategories
        for sub in cat['subcategories']:
            sub_row = {
                'Aktywny (0 lub 1)': 1,
                'Nazwa': sub['name'],
                'Kategoria nadrzędna': parent_name,
                'Główna kategoria (0/1)': 0
            }
            csv_rows.append(sub_row)
            
    return csv_rows

def clean_price(price_str):
    if not price_str:
        return "0.00"
    clean = price_str.lower().replace('zł', '').replace(' ', '').replace(',', '.')
    clean = re.sub(r'[^0-9\.]', '', clean)
    return clean.strip() if clean else "0.00"

def get_product_links_from_page(category_url, pagesNumber, main_cat_name, subcat_name=None):
    product_links = set()
    results = []

    pages_to_scrape = [category_url]

    for page_num in range(2, pagesNumber + 1):
        pages_to_scrape.append(f"{category_url}/{page_num}")

    for page_url in pages_to_scrape:
        try:
            print(f"Parsing: {page_url}")
            response = requests.get(page_url, headers=HEADERS, timeout=15)
            if response.status_code != 200:
                print(f"Skipping {page_url} (status {response.status_code})")
                continue

            soup = BeautifulSoup(response.content, 'html.parser')
            product_elements = soup.select('a[href]:has(span.productname)')

            if not product_elements:
                print(f"Nothing was found on {page_url}")

            for prod_a in product_elements:
                full_url = urljoin(CATEGORY_BASE_URL, prod_a['href'])
                if full_url not in product_links:
                    product_links.add(full_url)
                    results.append({'url': full_url, 'category': main_cat_name, 'subcategory': subcat_name})

            time.sleep(0.4)

        except Exception as e:
            print(f"Error {page_url}: {e}")

    return results

def scrape_product_data(product_url, category_path=None):
    try:
        response = requests.get(product_url, headers=HEADERS, timeout=15)
        if response.status_code != 200:
            print(f"Can't fetch product {product_url} status {response.status_code}")
            return None

        soup = BeautifulSoup(response.content, 'html.parser')
        product_data = {'Url': product_url}

        # Name
        name_tag = soup.find('h1', class_='name', itemprop='name')
        product_data['Name'] = name_tag.text.strip() if name_tag else 'Name Not Found'

        # Price
        price_tag = soup.find('em', class_='main-price')
        product_data['Price tax included'] = clean_price(price_tag.text) if price_tag else '0.00'

        # Manufacturer/Brand
        manufacturer_tag = soup.find('a', class_='brand')
        product_data['Manufacturer/brand'] = manufacturer_tag.get('title') if manufacturer_tag else ''

        # Description
        desc_tag = soup.find('div', itemprop='description')
        product_data['Description'] = desc_tag.get_text(separator='\n').strip() if desc_tag else ''

        # Two photos (or one)
        photos = []
        gallery = soup.find('div', class_='smallgallery')
        if gallery:
            photo_tags = gallery.find_all('a', class_='gallery', href=True)
            for a in photo_tags:
                photos.append(urljoin(CATEGORY_BASE_URL, a['href']))

        if not photos:
            main_img = soup.find('div', class_='mainimg')
            if main_img:
                photo_tags = main_img.find_all('a', href=True)
                for a in photo_tags:
                    photos.append(urljoin(CATEGORY_BASE_URL, a['href']))

        if len(photos) >= 2:
            product_data['Image URLs'] = ", ".join(photos[:2])
        elif len(photos) == 1:
            product_data['Image URLs'] = photos[0]
        else:
            product_data['Image URLs'] = ''

        # Attributes
        attributes = {}
        options_container = soup.find('div', class_='stocks')
        if options_container:
            rows = options_container.find_all('div', class_='f-row')
            for row in rows:
                label_tag = row.find('label')
                select_tag = row.find('select')
                if label_tag and select_tag:
                    attr_name = label_tag.text.replace('*', '').strip().rstrip(':')
                    attr_values = [opt.text.strip() for opt in select_tag.find_all('option')]
                    attributes[attr_name] = ", ".join(attr_values)

        if desc_tag:
            description_html = str(desc_tag)
            description_text = re.sub('<br\s*/?>', '\n', description_html, flags=re.IGNORECASE)
            description_text = BeautifulSoup(description_text, 'html.parser').get_text()
            for line in description_text.split('\n'):
                line = line.strip()
                if ':' in line:
                    parts = line.split(':', 1)
                    key = parts[0].strip()
                    value = parts[1].strip()
                    if key and value and key not in attributes:
                        attributes[key] = value

        product_data['attributes'] = str(attributes)

        product_data['Quantity'] = random.randint(1, 10)
        product_data['Weight'] = 1.0
        product_data['Width'] = 30
        product_data['Height'] = product_data['Width']
        product_data['Depth'] = product_data['Width']

        product_data['Active (0/1)'] = 1
        product_data['Tax rule ID'] = 1
        product_data['Categories'] = category_path if category_path else ''

        return product_data

    except Exception as e:
        print(f"Error while parsing product {product_url}: {e}")
        return None



all_products_data = []
if __name__ == '__main__':
    site_categories = get_categories_and_subcategories(CATEGORY_BASE_URL)
    print("Found categories:")
    for c in site_categories:
        print(f"- {c['name']} (subcategories: {len(c['subcategories'])})")


    print("\n--- Saving Categories CSV ---")
    cat_csv_data = prepare_categories_for_csv(site_categories)
    df_cats = pd.DataFrame(cat_csv_data)
    
    cat_columns_order = [
        'Aktywny (0 lub 1)', 'Nazwa', 'Kategoria nadrzędna', 'Główna kategoria (0/1)'
    ]       
    df_cats = df_cats[cat_columns_order]
    
    df_cats.to_csv("scraped_categories.csv", index=False, encoding='utf-8', sep=';')
    print("Categories saved to 'scraped_categories.csv'")


    print("\n--- Starting scraping ---")
    all_product_links = []  # list of dicts: {'url','category','subcategory'}

    for cat in site_categories:
        main_name = cat['name']

        if cat['subcategories']:
            for sub in cat['subcategories']:
                sub_name = sub['name']
                sub_url = sub['url']
                try:
                    page_response = requests.get(sub_url, headers=HEADERS, timeout=15)
                    if page_response.status_code != 200:
                        print(f"Can't open {sub_url}")
                        continue

                    category_soup = BeautifulSoup(page_response.content, 'html.parser')
                    pagesNumber = 1
                    paginator_block = category_soup.find_all('ul', class_='paginator')
                    if paginator_block:
                        allLi = paginator_block[0].find_all('li')
                        try:
                            pagesNumber = int((len(allLi)-1)/2)
                        except Exception:
                            pagesNumber = 1

                    links = get_product_links_from_page(sub_url, pagesNumber, main_name, sub_name)
                    all_product_links.extend(links)

                except Exception as e:
                    print(f"Error processing subcategory {sub_url}: {e}")
        else:
            cat_url = cat['url']
            try:
                page_response = requests.get(cat_url, headers=HEADERS, timeout=15)
                if page_response.status_code != 200:
                    print(f"Can't open {cat_url}")
                    continue

                category_soup = BeautifulSoup(page_response.content, 'html.parser')
                pagesNumber = 1
                paginator_block = category_soup.find_all('ul', class_='paginator')
                if paginator_block:
                    allLi = paginator_block[0].find_all('li')
                    try:
                        pagesNumber = int((len(allLi)-1)/2)
                    except Exception:
                        pagesNumber = 1

                links = get_product_links_from_page(cat_url, pagesNumber, main_name, None)
                all_product_links.extend(links)

            except Exception as e:
                print(f"Error processing category {cat_url}: {e}")


    # Avoid duplicates
    unique = {}
    for item in all_product_links:
        unique[item['url']] = item
    all_product_links = list(unique.values())

    print(f"---\n\n--- Found {len(all_product_links)} unique product links ---")


    print(f"\n--- Processing all {len(all_product_links)} products ---")

    for i, item in enumerate(all_product_links):
        link = item['url']
        cat = item['category']
        sub = item['subcategory']
        category_path = f"{cat},{sub}" if sub else cat
        print(f"  Processing product {i+1}/{len(all_product_links)}: {link}")
        data = scrape_product_data(link, category_path=category_path)
        if data:
            all_products_data.append(data)
        time.sleep(0.3)
        #break #DON'T FORGET TO REMOVE DAT


    # --- Saving to CSV ---
    df = pd.DataFrame(all_products_data)

    columns_order = ['Categories', 'Active (0/1)', 'Name', 'Manufacturer/brand', 'Price tax included', 'Tax rule ID', 'Image URLs', 'Description', 'Quantity', 'Weight', 'Height', 'Width', 'Depth']

    for col in columns_order:
        if col not in df.columns:
            df[col] = None

    df = df[columns_order]

    output_file = "scraped_products.csv"
    df.to_csv(output_file, index=False, encoding='utf-8', sep=';')
    # --- Saving to CSV ---


    print(f"\n--- All done! ---")
    print(f"{len(all_products_data)} products saved here: {output_file}")