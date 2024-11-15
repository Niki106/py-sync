import json
import argparse
import requests

STORE_HASH = "5byitdbjtb"
API_TOKEN = "t4iu0pxpzxck0h5azrwmy8u3w9994q2"

productPath = "D:\\Work\\Python\\Abdulrahman\\Data\\BigBuy"

def filter_product_info():
    new_data = []
    count = 0
    for i in range(6):
        file_path = f"{productPath}\\ProductsInfo_{i}.json"
        with open(file_path, 'r') as f:
            data = json.load(f)
            filtered_data = []
            for item in data:
                filtered_item = {"id": item['id'], "sku": item['sku'], "name": item['name'], "index": count}
                filtered_data.append(filtered_item)
                count = count + 1
            new_data.extend(filtered_data)
        
    file_path = f"{productPath}\\ProductsInfo.json"
    with open(file_path, 'w') as f:
        json.dump(new_data, f, indent=4)

def filter_product():
    merged_data = []
    for i in range(6):
        file_path = f"{productPath}\\Products_{i}.json"
        with open(file_path, 'r') as f:
            data = json.load(f)
            filtered_data = []
            for item in data:
                filtered_item = {"id": item['id'], "weight": item['weight'], "retailPrice": item['retailPrice']}
                filtered_data.append(filtered_item)
            merged_data.extend(filtered_data)
        
    file_path = f"{productPath}\\Products.json"
    with open(file_path, 'w') as f:
        json.dump(merged_data, f, indent=4)

def merge_images():
    merged_data = []
    for i in range(6):
        file_path = f"{productPath}\\Images_{i}.json"
        with open(file_path, 'r') as f:
            data = json.load(f)
            merged_data.extend(data)
        
    file_path = f"{productPath}\\Images.json"
    with open(file_path, 'w') as f:
        json.dump(merged_data, f, indent=4)

def get_sku(n):
    file_path = f"ProductsInfo.json"
    with open(file_path, 'r') as f:
        data = json.load(f)
        count = 0
        for item in data:
            count = count + 1
            if count == n:
                print(item['sku'])
                break

def get_new_product_id(pinfo_file, image_file):
    base_url = f"https://api.bigcommerce.com/stores/{STORE_HASH}/v3/catalog/"
    headers = {
        "X-Auth-Token": f"{API_TOKEN}"
    }

    id_mapping = []
    with open(pinfo_file, 'r') as f:
        pinfo_data = json.load(f)
        
        for product_info in pinfo_data[190000:200001]:
            old_product_id = product_info['id']
            product_sku = product_info['sku']
            
            # Get new product id by sku
            url = f"{base_url}products?keyword={product_sku}"
            response = requests.get(url, headers=headers)
            try:
                product_data = response.json()
            except (json.JSONDecodeError, requests.exceptions.RequestException) as e:
                continue
            
            if len(product_data['data']) == 0: 
                continue

            new_product_id = product_data['data'][0]['id']

            id_mapping.append({"old_id": old_product_id, "new_id": new_product_id})
            print(old_product_id, new_product_id)


    file_path = f"ID_Mapping119.json"
    with open(file_path, 'w') as f:
        json.dump(id_mapping, f, indent=4)

def main():
    # filter_product_info()
    # get_sku(args.number)  

    productInfoFile = "ProductsInfo.json"
    imageFile = "Image.json"
    get_new_product_id(productInfoFile, imageFile)

if __name__ == "__main__":
    # parser = argparse.ArgumentParser(description='A simple argument parser')
    # parser.add_argument('-n', '--number', type=int, required=True, help='Number')
    # args = parser.parse_args()
    # main(args)
    main()