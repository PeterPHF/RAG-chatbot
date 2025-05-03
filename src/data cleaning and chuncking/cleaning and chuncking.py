import json
import re
import os
import csv

# --- Clean function ---
def clean_text(text):
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'<.*?>', '', text)
    return text.strip()

# --- Chunk function ---
def chunk_text(text, max_words=500, min_words=200):
    words = text.split()
    chunks = []
    for i in range(0, len(words), max_words):
        chunk = words[i:i+max_words]
        if len(chunk) >= min_words:
            chunks.append(' '.join(chunk))
    return chunks

# --- Process JSON to chunks ---
def process_raw_to_chunks(input_json='data/raw/gfg_raw.json', output_txt='data/processed/gfg_chunks.txt', output_csv='data/processed/gfg_chunks.csv'):
    with open(input_json, 'r', encoding='utf-8') as f:
        data = json.load(f)

    all_chunks = []

    for entry in data:
        cleaned = clean_text(entry['content'])
        chunks = chunk_text(cleaned)
        for chunk in chunks:
            all_chunks.append({
                'title': entry.get('title', ''),
                'url': entry.get('url', ''),
                'chunk': chunk
            })

    os.makedirs(os.path.dirname(output_txt), exist_ok=True)

    # Save to TXT
    with open(output_txt, 'w', encoding='utf-8') as f:
        for item in all_chunks:
            f.write(item['chunk'] + '\n\n')

    # Save to CSV
    with open(output_csv, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['title', 'url', 'chunk'])
        writer.writeheader()
        writer.writerows(all_chunks)

    print(f" Saved {len(all_chunks)} chunks to:\n- {output_txt}\n- {output_csv}")

if __name__ == "__main__":
    process_raw_to_chunks()
