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
    
def read_texts_in_squares(
    images: list[np.ndarray],
    coords_list: list[list[int]],
    batch_size: int = 8,
) -> list[str]:
    """
    Reads the text present inside squares in multiple images.

    Parameters:
    images (list[numpy.array]): List of images loaded with cv2.
    coords_list (list[list[int]]): List of coordinates for each image in the format [x1, y1, x2, y2].
    batch_size (int): Batch size for OCR.
    enable_gpu (bool): Whether to enable GPU for OCR.

    Returns:
    list[str]: List of texts read within each region.
    """
    reader = OCRReaderSingleton.get_instance()
    texts = []

    for image, coords in zip(images, coords_list):
        x1, y1, x2, y2 = coords
        height, width = image.shape[:2]

        # Ensure coordinates are within the image bounds
        x1 = max(0, min(x1, width))
        x2 = max(0, min(x2, width))
        y1 = max(0, min(y1, height))
        y2 = max(0, min(y2, height))

        roi = image[y1:y2, x1:x2] # Region of interest

        # Check if the region of interest is empty
        if roi.size == 0:
            texts.append("")
            continue

        # Check if the region of interest is too small
        results = reader.readtext(
            roi, detail=0,
            batch_size=batch_size,
        )

        # If no text is detected, append an empty string
        text = ' '.join(results)
        texts.append(text)

    return texts

