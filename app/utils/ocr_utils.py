import easyocr

def read_text_in_square(
        image,
        coords: list,
        languages: list = ['en'],
        enable_gpu: bool = True
) -> str:
    """
    Reads the text present inside a square in an image.

    Parameters:
        image (numpy.array): Image loaded with cv2.
        coords (list): Coordinates of the square in the format [x1, y1, x2, y2].

    Returns:
        str: Text read within the region.
    """
    x1, y1, x2, y2 = coords
    # Extracting the region of interest (ROI) from the image
    roi = image[y1:y2, x1:x2]
    
    # Initializes the EasyOCR reader (in this example, configured for Portuguese)
    reader = easyocr.Reader(languages, gpu=enable_gpu)
    
    # Reads the text in the ROI without additional details (only the text)
    results = reader.readtext(roi, detail=0)
    
    # Joins all the read texts into a single string
    text = ' '.join(results)
    
    return text

