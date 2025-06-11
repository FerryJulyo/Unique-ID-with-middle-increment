import csv
from collections import defaultdict

csv_file_path = "master_composer.csv"
output_file_path = "update_queries.txt"

code_counter = defaultdict(int)
update_cases = []

id_list = []

with open(csv_file_path, newline='', encoding='utf-8-sig') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=';')
    reader.fieldnames = [name.strip().lower() for name in reader.fieldnames]

    for row in reader:
        row_id = row['id'].strip()
        original_code = row['code'].strip()

        if len(original_code) != 16:
            print(f"Kode tidak valid: {original_code}")
            continue

        prefix = original_code[:11]
        suffix = original_code[-3:]
        key = f"{prefix}_{suffix}"

        code_counter[key] += 1
        mid = f"{code_counter[key]:02d}"
        new_code = f"{prefix}{mid}{suffix}"

        update_cases.append(f"  WHEN {row_id} THEN '{new_code}'")
        id_list.append(row_id)

# Gabungkan jadi satu query
query = (
    "UPDATE master_composer\n"
    "SET code = CASE id\n" +
    "\n".join(update_cases) +
    "\nEND\n"
    f"WHERE id IN ({', '.join(id_list)});"
)

# Simpan ke file
with open(output_file_path, 'w', encoding='utf-8') as f:
    f.write(query)

print("File berhasil dibuat:", output_file_path)
