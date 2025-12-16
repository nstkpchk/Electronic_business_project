import requests
import pandas as pd
import xml.etree.ElementTree as ET
import time
from api_config import PRESTASHOP_URL, API_KEY, LANGUAGE_ID, HOME_CATEGORY_ID


class PrestaShopImporter:
    def __init__(self):
        self.api_url = f"{PRESTASHOP_URL}/api"
        self.auth = (API_KEY, '')
        self.headers = {'Content-Type': 'application/xml'}
        
        self.category_mapping = {}
        self.product_mapping = {}
    
    def test_connection(self):
        try:
            response = requests.get(self.api_url, auth=self.auth)
            if response.status_code == 200:
                print("API connection SUCCESSFUL!")
                return True
            else:
                print(f"API connection FAILED: {response.status_code}")
                print(response.text)
                return False
        except Exception as e:
            print(f"Error: {e}")
            return False
    
    def create_category(self, name, parent_name='Home'):
        print(f"Creating category: {name} (parent: {parent_name})")
        
        if name in self.category_mapping:
            print(f"Already exists (ID: {self.category_mapping[name]})")
            return self.category_mapping[name]
        
        try:
            if parent_name == 'Home':
                parent_id = HOME_CATEGORY_ID
            else:
                parent_id = self.category_mapping.get(parent_name, '2')
            
            # creating XML
            prestashop = ET.Element('prestashop')
            category = ET.SubElement(prestashop, 'category')
            
            active = ET.SubElement(category, 'active')
            active.text = '1'
            
            name_tag = ET.SubElement(category, 'name')
            language = ET.SubElement(name_tag, 'language', id=LANGUAGE_ID)
            language.text = name
            
            desc_tag = ET.SubElement(category, 'description')
            desc_lang = ET.SubElement(desc_tag, 'language', id=LANGUAGE_ID)
            desc_lang.text = f'<p>{name}</p>'
            
            # link rewriter
            link_rewrite = ET.SubElement(category, 'link_rewrite')
            link_lang = ET.SubElement(link_rewrite, 'language', id=LANGUAGE_ID)
            link_lang.text = name.lower().replace(' ', '-').replace('ą', 'a').replace('ć', 'c').replace('ę', 'e').replace('ł', 'l').replace('ń', 'n').replace('ó', 'o').replace('ś', 's').replace('ź', 'z').replace('ż', 'z')
            
            id_parent = ET.SubElement(category, 'id_parent')
            id_parent.text = str(parent_id)
            
            xml_str = ET.tostring(prestashop, encoding='utf-8')
            
            # sending request
            response = requests.post(
                f"{self.api_url}/categories",
                auth=self.auth,
                headers=self.headers,
                data=xml_str
            )
            
            if response.status_code == 201:
                response_root = ET.fromstring(response.content)
                new_id = response_root.find('.//id')
                if new_id is not None:
                    cat_id = new_id.text
                    self.category_mapping[name] = cat_id
                    print(f"  Created! ID: {cat_id}\n")
                    return cat_id
            else:
                print(f"  Failed: {response.status_code}")
                print(response.text[:500])
                return None
                
        except Exception as e:
            print(f"  Error: {e}")
            return None
    
    def import_categories(self, csv_file='scraped_categories.csv'):
        print("\n=== IMPORTING CATEGORIES ===\n")
        
        df = pd.read_csv(csv_file, sep=';', encoding='utf-8')
        
        # ROOT CATEGORIES
        parent_cats = df[df['Kategoria nadrzędna'] == 'Home']
        for _, row in parent_cats.iterrows():
            self.create_category(row['Nazwa'], 'Home')
            time.sleep(0.5)
        
        # OTHER CATEGORIES
        sub_cats = df[df['Kategoria nadrzędna'] != 'Home']
        for _, row in sub_cats.iterrows():
            self.create_category(row['Nazwa'], row['Kategoria nadrzędna'])
            time.sleep(0.5)
        
        print(f"\nImported {len(self.category_mapping)} categories")
        return self.category_mapping



if __name__ == '__main__':
    importer = PrestaShopImporter()
    
    if importer.test_connection():
        importer.import_categories()