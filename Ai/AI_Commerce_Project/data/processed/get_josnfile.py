import json

def extract_and_restructure_requests(input_file_path, output_file_path):
    try:
        with open(input_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        cleaned_requests = []

        for entry in data:
            if entry.get('type') == 'request':
                raw_content = entry.get('content')

                # Convert stringified JSON to dict
                if isinstance(raw_content, str):
                    try:
                        content = json.loads(raw_content)
                    except json.JSONDecodeError:
                        content = {}
                else:
                    content = raw_content or {}

                # Extract fields
                ip_address = content.pop("ip_address", None)
                uri = content.pop("uri", None)
                inner_method = content.pop("method", None)
                headers = content.get("headers", {})

                # Build full URL
                host = headers.get("host")
                full_url = f"http://{host}{uri}" if host and uri else entry.get("url")

                cleaned_entry = {
                    "type": "request",
                    "ip_address": ip_address,
                    "url": full_url,
                    "method": inner_method or entry.get('method'),
                    "content": content
                }

                cleaned_requests.append(cleaned_entry)

        with open(output_file_path, 'w', encoding='utf-8') as f_out:
            json.dump(cleaned_requests, f_out, indent=2, ensure_ascii=False)

        print(f"Saved {len(cleaned_requests)} cleaned requests to: {output_file_path}")

    except Exception as e:
        print(f"Error: {e}")

# Paths
input_file_path = r'E:\CSIC 2010 Web Application Attacks\CSIC-2010-Web-Application-Attacks\Ai\telescope_entries1.json'
output_file_path = r'E:\CSIC 2010 Web Application Attacks\CSIC-2010-Web-Application-Attacks\Ai\cleaned_requests.json'

extract_and_restructure_requests(input_file_path, output_file_path)
