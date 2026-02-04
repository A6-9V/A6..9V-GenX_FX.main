import base64

def get_direct_link(sharing_url):
    encoded_url = base64.b64encode(sharing_url.encode('utf-8')).decode('utf-8')
    res_url = "u!" + encoded_url.replace('/', '_').replace('+', '-').rstrip('=')
    return f"https://api.onedrive.com/v1.0/shares/{res_url}/root/content"

url = "https://1drv.ms/u/c/8F247B1B46E82304/IQDlMaSTMyRJSLVeesO1cwjfAUihdhxgnpRyMiQB9Z1cv1s"
print(get_direct_link(url))
