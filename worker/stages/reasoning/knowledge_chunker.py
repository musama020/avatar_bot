from dataclasses import dataclass


@dataclass
class KnowledgeChunk:
    chunk_id: int
    section: str
    heading: str
    text: str

    def text_for_embedding(self):
        """The heading path goes in front so a chunk still makes sense on its own."""
        return f"{self.section} > {self.heading}\n{self.text}"


class MarkdownSectionChunker:
    """One chunk per '###' heading, labelled with its '##' section. Text before the first '##' is a file note and skipped."""

    def split(self, markdown_text):
        chunks = []
        current_section = ""
        current_heading = ""
        current_lines = []

        for line in markdown_text.splitlines():
            if line.startswith("### "):
                self.append_chunk(chunks, current_section, current_heading, current_lines)
                current_heading = line[4:].strip()
                current_lines = []
            elif line.startswith("## "):
                self.append_chunk(chunks, current_section, current_heading, current_lines)
                current_section = line[3:].strip()
                current_heading = ""
                current_lines = []
            elif current_heading:
                current_lines.append(line)

        self.append_chunk(chunks, current_section, current_heading, current_lines)
        return chunks

    def append_chunk(self, chunks, section, heading, lines):
        body = "\n".join(lines).strip()
        if not heading or not body:
            return
        chunks.append(KnowledgeChunk(chunk_id=len(chunks) + 1, section=section, heading=heading, text=body))
