from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseExtractor(ABC):
    """
    Abstract base class for data extractors.
    Defines the common interface for all extractor implementations.
    """
    def __init__(self):
        """
        Initializes the extractor with basic metadata.
        """
        self.metadata = {
            "extractor_type": self.__class__.__name__, # Store the name of the concrete class
            "created_at": datetime.datetime.now().isoformat()
        }
        
    @abstractmethod
    def extract_data(self, file_path: str) -> Dict[str, Any]:
        """
        Abstract method to extract data from a file.
        Concrete implementations must override this method.
        
        Args:
            file_path (str): The path to the file to extract data from.
            
        Returns:
            Dict[str, Any]: A dictionary containing the extracted data in a standardized format.
            
        Raises:
            NotImplementedError: If the method is not implemented by a subclass.
            FileNotFoundError: If the file does not exist.
            ValueError: If the file format is invalid or other extraction errors occur.
        """
        pass
        
    def get_metadata(self) -> Dict[str, Any]:
        """
        Returns the metadata collected during the extraction process.
        
        Returns:
            Dict[str, Any]: A dictionary containing metadata about the extraction.
        """
        return self.metadata

# Note: Need to import datetime for the timestamp in __init__
import datetime 