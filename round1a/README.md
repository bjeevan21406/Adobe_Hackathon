# Adobe India Hackathon 2025: Connecting the Dots (Round 1A)

This repository contains the solution for Round 1A of the hackathon, which focuses on extracting a structured outline from PDF documents.

### My Approach

The core of this solution is a multi-step heuristic process designed to robustly identify titles and headings within a PDF without relying on a fixed structure.

1.  *Title Extraction*: The title is identified by analyzing text blocks in the top half of the first page. It prioritizes text with the largest font size that is also horizontally centered, which is a common characteristic of titles.

2.  *Body Text Analysis*: To differentiate headings from normal text, the script first determines the most common font size in the document, which is assumed to be the body text size.

3.  *Heading Identification*: The script then iterates through every text block in the document. A block is classified as a potential heading if its font size is significantly larger than the body text or if it is both bold and slightly larger. This dual condition helps catch a wider variety of heading styles. Common headers and footers are filtered out by ignoring text that repeats on many pages.

4.  *Hierarchical Leveling*: Once a heading is identified, its hierarchical level (H1, H2, H3) is determined.
    *   *Numbered Headings*: For headings that start with a number pattern (e.g., "2.1", "3.1.4"), the level is inferred from the number of dots or dashes. "2.1" becomes H2.
    *   *Un-numbered Headings*: If a heading has no number, it is assigned as an H1 by default.

5.  *Final Output*: The extracted outline is sorted by page number to ensure correct chronological order and then formatted into the required JSON structure.

### Models & Libraries Used

*   *Python 3.9*: The core programming language.
*   *PyMuPDF*: A powerful and efficient library for PDF parsing, allowing detailed access to text block properties like font size, flags (bold), and position.

### How to Build and Run the Solution

The solution is containerized with Docker for portability and must be run on an AMD64 architecture.

*1. Build the Docker Image*

From the root directory of this project, run the following command.

```sh
docker build --platform linux/amd64 -t mysolutionname:somerandomidentifier .