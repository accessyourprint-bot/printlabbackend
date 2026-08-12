import io

path = "app/api/v1/endpoints/files.py"
with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

idx1 = content.find("Could not retrieve file")
print("--- around 'Could not retrieve file' ---")
print(repr(content[idx1-50:idx1+400]))

idx2 = content.find("No files found for this order")
print("--- around 'No files found for this order' ---")
print(repr(content[idx2-50:idx2+300]))
