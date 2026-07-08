from pypdf import PdfReader

def extract_text(file_input):

    # Check if input is UploadFile
    if hasattr(file_input, "filename"):
        filename = file_input.filename.lower()
        file = file_input.file
    else:
        # Local file object
        filename = file_input.name.lower()
        file = file_input

    # Move pointer to beginning
    file.seek(0)

    # TXT files
    if filename.endswith(".txt"):
        content = file.read()

        if isinstance(content, bytes):
            return content.decode("utf-8", errors="ignore")

        return str(content)

    # PDF files
    elif filename.endswith(".pdf"):

        reader = PdfReader(file)
        text = ""

        for page in reader.pages:
            page_text = page.extract_text()

            if page_text:
                text += page_text + " "

        return text.strip()

    else:
        raise ValueError("Only TXT and PDF files are supported.")