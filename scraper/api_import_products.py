import requests
import pandas as pd
import xml.etree.ElementTree as ET
import time
import os
import re
from api_config import PRESTASHOP_URL, API_KEY, LANGUAGE_ID, HOME_CATEGORY_ID


class ProductImporter:
    def __init__(self):
        self.api_url = f"{PRESTASHOP_URL}/api"
        self.auth = (API_KEY, '')
        self.headers = {'Content-Type': 'application/xml'}
        self.manufacturer_mapping = {}
        self.category_mapping = {}
    
    def load_existing_categories(self):
        try:
            response = requests.get(f"{self.api_url}/categories", auth=self.auth)
            if response.status_code != 200:
                print(f"Failed to get categories: {response.status_code}")
                return
            
            root = ET.fromstring(response.content)
            category_ids = []
            
            categories_elem = root.find('categories')
            if categories_elem is not None:
                for cat in categories_elem.findall('category'):
                    cat_id = cat.get('id')
                    if cat_id:
                        category_ids.append(cat_id)
            
            print(f"Found {len(category_ids)} category IDs, loading details...")
            
            for cat_id in category_ids:
                try:
                    cat_response = requests.get(f"{self.api_url}/categories/{cat_id}", auth=self.auth)
                    if cat_response.status_code == 200:
                        cat_root = ET.fromstring(cat_response.content)
                        name_elem = cat_root.find('.//name/language[@id="' + LANGUAGE_ID + '"]')
                        if name_elem is not None and name_elem.text:
                            self.category_mapping[name_elem.text] = cat_id
                except Exception as e:
                    print(f"  - Skip category {cat_id}: {e}")
                    continue
            
            print(f"Loaded {len(self.category_mapping)} categories.\n")
        except Exception as e:
            print(f"Error loading categories: {e}")
    
    def create_manufacturer(self, manufacturer_name):
        if not manufacturer_name or manufacturer_name.strip() == '':
            return None
        
        if manufacturer_name in self.manufacturer_mapping:
            return self.manufacturer_mapping[manufacturer_name]
        
        try:
            prestashop = ET.Element('prestashop')
            manufacturer = ET.SubElement(prestashop, 'manufacturer')
            ET.SubElement(manufacturer, 'name').text = manufacturer_name
            ET.SubElement(manufacturer, 'active').text = '1'
            
            response = requests.post(
                f"{self.api_url}/manufacturers",
                auth=self.auth,
                headers=self.headers,
                data=ET.tostring(prestashop, encoding='utf-8')
            )
            
            if response.status_code == 201:
                manuf_id = ET.fromstring(response.content).find('.//id').text
                self.manufacturer_mapping[manufacturer_name] = manuf_id
                return manuf_id
        except Exception as e:
            print(f"  Manufacturer error: {e}")
        return None
    
    def upload_image(self, product_id, image_url):
        try:
            img_response = requests.get(image_url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=15)
            if img_response.status_code != 200:
                return False
            
            content_type = img_response.headers.get('Content-Type', 'image/jpeg')
            ext = 'jpg'
            if 'png' in content_type:
                ext = 'png'
            elif 'gif' in content_type:
                ext = 'gif'
            
            files = {'image': (f'product.{ext}', img_response.content, content_type)}
            
            upload_response = requests.post(
                f"{self.api_url}/images/products/{product_id}",
                auth=self.auth,
                files=files
            )
            
            return upload_response.status_code in [200, 201]
        except:
            return False
    
    def create_product(self, product_data):
        name = product_data.get('Name', 'Unnamed Product')
        print(f"Creating: {name[:50]}...")
        
        try:
            manufacturer_id = None
            if product_data.get('Manufacturer/brand'):
                manufacturer_id = self.create_manufacturer(product_data['Manufacturer/brand'])
            
            category_ids = []
            categories_str = product_data.get('Categories', '')
            if categories_str:
                for cat_name in categories_str.split(','):
                    cat_name = cat_name.strip()
                    if cat_name in self.category_mapping:
                        category_ids.append(self.category_mapping[cat_name])
            
            if not category_ids:
                category_ids = [HOME_CATEGORY_ID]
            
            # creating XML
            prestashop = ET.Element('prestashop')
            product = ET.SubElement(prestashop, 'product')
            
            ET.SubElement(product, 'active').text = str(product_data.get('Active (0/1)', 1))

            ET.SubElement(product, 'available_for_order').text = '1'
            ET.SubElement(product, 'show_price').text = '1'
            ET.SubElement(product, 'visibility').text = 'both'

            ET.SubElement(product, 'minimal_quantity').text = '1'
            
            name_tag = ET.SubElement(product, 'name')
            ET.SubElement(name_tag, 'language', id=LANGUAGE_ID).text = name
            
            description = product_data.get('Description', '')
            desc_html = '<p>' + description.replace('\n', '</p><p>') + '</p>' if description else '<p></p>'
            desc_tag = ET.SubElement(product, 'description')
            ET.SubElement(desc_tag, 'language', id=LANGUAGE_ID).text = desc_html
            
            short_desc = description[:400] + '...' if len(description) > 400 else description
            short_tag = ET.SubElement(product, 'description_short')
            ET.SubElement(short_tag, 'language', id=LANGUAGE_ID).text = '<p>' + short_desc + '</p>' if short_desc else '<p></p>'
            
            link_rewrite = ET.SubElement(product, 'link_rewrite')
            link_text = name.lower().replace(' ', '-')
            link_text = (link_text.replace('ą', 'a').replace('ć', 'c').replace('ę', 'e')
                        .replace('ł', 'l').replace('ń', 'n').replace('ó', 'o')
                        .replace('ś', 's').replace('ź', 'z').replace('ż', 'z'))
            link_text = re.sub(r'[^a-z0-9\-]', '', link_text)
            ET.SubElement(link_rewrite, 'language', id=LANGUAGE_ID).text = link_text
            
            ET.SubElement(product, 'price').text = f"{float(product_data.get('Price tax included', 0)) / 1.23:.6f}"
            ET.SubElement(product, 'id_tax_rules_group').text = str(product_data.get('Tax rule ID', 1))

            ET.SubElement(product, 'width').text = str(product_data.get('Width', 0))
            ET.SubElement(product, 'height').text = str(product_data.get('Height', 0))
            ET.SubElement(product, 'depth').text = str(product_data.get('Depth', 0))
            ET.SubElement(product, 'weight').text = str(product_data.get('Weight', 0))
            
            if manufacturer_id:
                ET.SubElement(product, 'id_manufacturer').text = str(manufacturer_id)
            
            associations = ET.SubElement(product, 'associations')
            categories_assoc = ET.SubElement(associations, 'categories')
            for cat_id in category_ids:
                category = ET.SubElement(categories_assoc, 'category')
                ET.SubElement(category, 'id').text = str(cat_id)
            
            ET.SubElement(product, 'id_category_default').text = str(category_ids[0])
            ET.SubElement(product, 'state').text = '1'
            
            # sending product
            response = requests.post(
                f"{self.api_url}/products",
                auth=self.auth,
                headers=self.headers,
                data=ET.tostring(prestashop, encoding='utf-8')
            )
            
            if response.status_code == 201:
                product_id = ET.fromstring(response.content).find('.//id').text
                print(f"  Created ID: {product_id}")
                
                # Update stock
                stock_response = requests.get(
                    f"{self.api_url}/stock_availables",
                    auth=self.auth,
                    params={'filter[id_product]': product_id}
                )
                if stock_response.status_code == 200:
                    stock_id = ET.fromstring(stock_response.content).find('.//stock_available').get('id')
                    if stock_id is not None:
                        stock_data = requests.get(f"{self.api_url}/stock_availables/{stock_id}", auth=self.auth)
                        if stock_data.status_code == 200:
                            root = ET.fromstring(stock_data.content)
                            root.find('.//quantity').text = str(product_data.get('Quantity', 10))
                            requests.put(
                                f"{self.api_url}/stock_availables/{stock_id}",
                                auth=self.auth,
                                headers=self.headers,
                                data=ET.tostring(root, encoding='utf-8')
                            )
                
                # Upload images
                image_urls = product_data.get('Image URLs', '')
                if image_urls:
                    urls = [url.strip() for url in image_urls.split(',')][:2]
                    for i, url in enumerate(urls, 1):
                        if url and self.upload_image(product_id, url):
                            print(f"  Image {i} uploaded")
                        time.sleep(0.3)
                
                return product_id
            else:
                print(f"  Failed: {response.status_code}")
                return None
        except Exception as e:
            print(f"  Error: {e}")
            return None
    
    def import_products(self, csv_file='scraped_products.csv'):
        print("\n=== IMPORTING PRODUCTS ===\n")
        
        if not os.path.exists(csv_file):
            print(f"File {csv_file} not found!")
            return
        
        self.load_existing_categories()
        
        df = pd.read_csv(csv_file, sep=';', encoding='utf-8')
        
        total = len(df)
        success = 0
        
        for idx, row in df.iterrows():
            print(f"[{idx+1}/{total}] ", end='')
            if self.create_product(row.to_dict()):
                success += 1
        
        print(f"\nTotal: {total} | Success: {success} | Failed: {total-success}")



if __name__ == '__main__':
    importer = ProductImporter()
    importer.import_products()