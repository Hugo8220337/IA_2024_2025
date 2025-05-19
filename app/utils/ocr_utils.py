import numpy as np
import easyocr

"""
This module provides a singleton class for the OCR reader and a function to read text
from a specified square in an image using the EasyOCR library.
The OCR reader is initialized only once and reused for subsequent calls to improve performance.
The `read_text_in_square` function extracts a square region from the image based on the provided coordinates
and uses the OCR reader to read the text within that region.
"""
class OCRReaderSingleton:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = easyocr.Reader(['en'], gpu=True)
        return cls._instance
    
def read_text_in_square(
    image: np.ndarray,
    coords: list[int],
    languages: list[str] = ['en'],
    enable_gpu: bool = True
) -> str:
    """
    Reads the text present inside a square in an image.

    Parameters:
    image (numpy.array): Image loaded with cv2.
    coords (list[int]): Coordinates of the square in the format [x1, y1, x2, y2].
    languages (list[str]): List of languages for OCR.
    enable_gpu (bool): Whether to enable GPU for OCR.

    Returns:
    str: Text read within the region.
    """
    x1, y1, x2, y2 = coords

    # Ensures the coordinates are within the image bounds
    height, width = image.shape[:2]
    x1 = max(0, min(x1, width))
    x2 = max(0, min(x2, width))
    y1 = max(0, min(y1, height))
    y2 = max(0, min(y2, height))

    # Extracting the region of interest (ROI) from the image
    roi = image[y1:y2, x1:x2]

    # If the ROI is empty, return an empty string
    if roi.size == 0:
        return ""
    
    # gets the OCR reader instance
    reader = OCRReaderSingleton.get_instance()
    
    # Reads the text in the ROI without additional details (only the text)
    results = reader.readtext(roi, detail=0)
    
    # Joins all the read texts into a single string
    text = ' '.join(results)
    
    return text

