import json
import re
import os
import csv
from tqdm import tqdm
import numpy as np

def clean_text(text):
    """Clean text by removing HTML, special chars, and normalizing whitespace"""
    text = re.sub(r'<.*?>', '', text)
    text = re.sub(r'[^\w\s.,;:!?\'"-]', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def chunk_text(text, max_words=400, min_words=150, overlap=50):
    """Split text into chunks with overlap, ensuring quality"""
    words = text.split()
    if len(words) <= max_words:
        return [' '.join(words)] if len(words) >= min_words else []
    
    chunks = []
    start = 0
    while start < len(words):
        end = min(start + max_words, len(words))
        chunk = words[start:end]
        if len(chunk) >= min_words:
            chunks.append(' '.join(chunk))
        start += (max_words - overlap)
    return chunks

def process_raw_to_chunks(input_json='data/raw/gfg_ai_raw.json', 
                         output_dir='data/processed',
                         max_chunks=300,
                         max_words=400,
                         min_words=150):
    """
    Process raw data into chunks with limit of 300 total chunks
    Prioritizes content with highest topic relevance
    """
    os.makedirs(output_dir, exist_ok=True)
    base_name = os.path.splitext(os.path.basename(input_json))[0]
    output_txt = os.path.join(output_dir, f'{base_name}_300chunks.txt')
    output_csv = os.path.join(output_dir, f'{base_name}_300chunks.csv')

    with open(input_json, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Score pages by topic relevance (number of topics matched)
    for page in data:
        page['topic_score'] = len(page.get('matched_topics', []))

    # Sort pages by relevance (highest first)
    data.sort(key=lambda x: x['topic_score'], reverse=True)

    all_chunks = []
    current_chunks = 0
    
    with tqdm(total=max_chunks, desc="Generating chunks") as pbar:
        for entry in data:
            if current_chunks >= max_chunks:
                break
                
            cleaned = clean_text(entry['content'])
            chunks = chunk_text(cleaned, max_words, min_words)
            
            for chunk in chunks:
                if current_chunks >= max_chunks:
                    break
                    
                all_chunks.append({
                    'source': 'GeeksforGeeks',
                    'title': entry.get('title', ''),
                    'url': entry.get('url', ''),
                    'topics': entry.get('matched_topics', []),
                    'chunk': chunk,
                    'word_count': len(chunk.split())
                })
                current_chunks += 1
                pbar.update(1)

    # Save to TXT
    with open(output_txt, 'w', encoding='utf-8') as f:
        for item in all_chunks:
            f.write(item['chunk'] + '\n\n')

    # Save to CSV
    with open(output_csv, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['source', 'title', 'url', 'topics', 'chunk', 'word_count'])
        writer.writeheader()
        writer.writerows(all_chunks)

    print(f"\nSuccessfully generated {len(all_chunks)} chunks")
    print(f" - Source pages used: {len(set(ch['url'] for ch in all_chunks))}")
    print(f" - Avg words per chunk: {np.mean([ch['word_count'] for ch in all_chunks]):.1f}")
    print(f"Files saved to:\n- {output_txt}\n- {output_csv}")

if __name__ == "__main__":
    process_raw_to_chunks(
        input_json='data/raw/gfg_ai_raw.json',
        output_dir='data/processed',
        max_chunks=300,
        max_words=400,
        min_words=150
    )