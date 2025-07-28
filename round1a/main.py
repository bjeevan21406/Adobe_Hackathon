import fitz  # PyMuPDF
import json
import os
import re
from collections import Counter

# Directory for input PDFs and output JSONs
INPUT_DIR = "input"
OUTPUT_DIR = "output"

def get_most_common_font_size(doc):
    """
    Finds the most common font size to identify the document's body text size.
    """
    sizes = Counter()
    page_limit = min(10, doc.page_count)
    for page in doc.pages(0, page_limit):
        blocks = page.get_text("dict").get("blocks", [])
        for block in blocks:
            if block.get("type") == 0:  # Text block
                for line in block.get("lines", []):
                    for span in line.get("spans", []):
                        sizes[round(span.get("size", 0))] += 1
    
    if not sizes:
        return 12  # Return a default size
    
    return sizes.most_common(1)[0][0]

def get_block_properties(block):
    """
    Extracts aggregated properties from a text block.
    """
    if block.get("type") != 0:
        return None

    full_text_lines = []
    span_sizes = []
    font_flags = []

    for line in block.get("lines", []):
        full_text_lines.append("".join(span.get("text", "") for span in line.get("spans", [])))
        for span in line.get("spans", []):
            span_sizes.append(round(span.get("size", 0)))
            font_flags.append(span.get("flags", 0))

    if not full_text_lines or not span_sizes:
        return None
        
    is_bold = (sum(1 for flag in font_flags if flag & 16) / len(font_flags)) > 0.5
    dominant_size = Counter(span_sizes).most_common(1)[0][0]

    return {
        "text": " ".join(full_text_lines).strip(),
        "size": dominant_size,
        "bold": is_bold
    }

def extract_outline(pdf_path):
    """
    Extracts a structured title and outline from a PDF by analyzing text blocks.
    (IMPROVED VERSION 4)
    """
    doc = fitz.open(pdf_path)
    title = ""
    outline = []
    
    # --- 1. Title Extraction ---
    if doc.page_count > 0:
        first_page = doc[0]
        page_width = first_page.rect.width
        page_height = first_page.rect.height
        blocks = first_page.get_text("dict").get("blocks", [])
        
        potential_titles = []
        for block in blocks:
            props = get_block_properties(block)
            if not props: continue
            if block['bbox'][3] > page_height / 2: continue
            block_width = block['bbox'][2] - block['bbox'][0]
            horizontal_center = block['bbox'][0] + block_width / 2
            if not (page_width * 0.1 < horizontal_center < page_width * 0.9): continue
            potential_titles.append(props)

        if potential_titles:
            max_size = max(p['size'] for p in potential_titles)
            title_texts = [p['text'] for p in potential_titles if p['size'] == max_size]
            title = " ".join(title_texts)

    # --- 2. Identify Heading Blocks ---
    body_size = get_most_common_font_size(doc)
    all_headings = []
    
    # MODIFIED: Start searching for headings from page 2 (index 1) onwards.
    for page_num, page in enumerate(doc):
        if page_num == 0:
            continue
            
        blocks = page.get_text("dict").get("blocks", [])
        for block in blocks:
            props = get_block_properties(block)
            if not props or not props.get("text"): continue

            text = props["text"]
            
            is_significant_font = (props["size"] > body_size * 1.15) or \
                                  (props["bold"] and props["size"] > body_size * 1.05)
            is_reasonable_length = 3 < len(text) < 250
            if re.match(r"^\s*\d+\s*/\s*\d+\s*$", text): continue
            
            if is_significant_font and is_reasonable_length:
                all_headings.append({
                    "text": text,
                    "page": page_num,
                    "size": props["size"]
                })

    # --- 3. Filter, Rank, and Format Headings ---
    if all_headings:
        heading_text_counts = Counter(h['text'] for h in all_headings)
        unique_headings = [h for h in all_headings if heading_text_counts[h['text']] < 3]

        for h in unique_headings:
            # MODIFIED: Simplified leveling and kept original text
            match = re.match(r"^\s*([A-Z0-9]+([.\-][A-Z0-9]+)*)\.?\s+", h["text"])
            
            if match:
                # Level is based on the number of dots (e.g., 2.1 is H2)
                level_num = min(match.group(1).count('.') + match.group(1).count('-') + 1, 6)
                level = f"H{level_num}"
            else:
                # Un-numbered headings are now assumed to be H1
                level = "H1"
            
            # MODIFIED: Keep the original heading text, including the number
            text_to_append = h["text"].strip()
            if text_to_append:
                outline.append({"level": level, "text": text_to_append, "page": h["page"]})

    # Sort the final outline by page number
    outline.sort(key=lambda x: x['page'])

    return {"title": title.strip(), "outline": outline}

def main():
    """Processes all PDFs in the input directory."""
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    if not os.path.exists(INPUT_DIR):
        print(f"Error: Input directory '{INPUT_DIR}' not found. Please create it and add PDF files.")
        return

    for filename in os.listdir(INPUT_DIR):
        if filename.lower().endswith(".pdf"):
            pdf_path = os.path.join(INPUT_DIR, filename)
            json_filename = os.path.splitext(filename)[0] + ".json"
            output_path = os.path.join(OUTPUT_DIR, json_filename)
            
            print(f"Processing {filename}...")
            try:
                result = extract_outline(pdf_path)
                with open(output_path, "w", encoding="utf-8") as f:
                    json.dump(result, f, indent=2) 
                print(f"-> Successfully created {json_filename}")
            except Exception as e:
                print(f"-> Error processing {filename}: {e}")

if __name__ == "__main__":
    main()