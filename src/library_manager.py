"""
Library Manager Module for Auto-DJ Phase 2

This module handles the library scanning, database management, and similarity calculation:
- Music library scanning and file discovery
- Database creation and management for song fingerprints
- Similarity calculation using cosine similarity
- Song ranking and recommendation system
"""

import os
import pickle
import json
import numpy as np
from typing import List, Dict, Tuple, Optional
from pathlib import Path
import logging
from sklearn.metrics.pairwise import cosine_similarity

from .audio_processor import AudioProcessor

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LibraryManager:
    """
    Main class for managing music library and similarity calculations.
    
    This class implements the Phase 2 functionality of the Auto-DJ project:
    1. Library Scan: Scan directories for music files
    2. Database Creation: Process songs and store fingerprints
    3. Similarity Calculation: Compare fingerprints using cosine similarity
    4. Ranking: Generate similarity-based recommendations
    """
    
    # Supported audio file extensions
    SUPPORTED_EXTENSIONS = {'.mp3', '.wav', '.flac', '.m4a', '.aac', '.ogg', '.wma'}
    
    def __init__(self, 
                 audio_processor: Optional[AudioProcessor] = None,
                 database_path: str = "music_library.db"):
        """
        Initialize the LibraryManager.
        
        Args:
            audio_processor: AudioProcessor instance for fingerprinting
            database_path: Path to store the music library database
        """
        self.audio_processor = audio_processor or AudioProcessor()
        self.database_path = database_path
        self.library_data = {}  # {file_path: {'fingerprint': np.array, 'metadata': dict}}
        
    def scan_directory(self, directory_path: str, recursive: bool = True) -> List[str]:
        """
        Scan a directory for music files.
        
        Args:
            directory_path: Path to the directory to scan
            recursive: Whether to scan subdirectories recursively
            
        Returns:
            List of file paths to music files
        """
        try:
            logger.info(f"Scanning directory: {directory_path}")
            
            if not os.path.exists(directory_path):
                raise FileNotFoundError(f"Directory not found: {directory_path}")
            
            music_files = []
            path_obj = Path(directory_path)
            
            if recursive:
                # Recursive scan
                for file_path in path_obj.rglob('*'):
                    if file_path.is_file() and file_path.suffix.lower() in self.SUPPORTED_EXTENSIONS:
                        music_files.append(str(file_path))
            else:
                # Non-recursive scan
                for file_path in path_obj.iterdir():
                    if file_path.is_file() and file_path.suffix.lower() in self.SUPPORTED_EXTENSIONS:
                        music_files.append(str(file_path))
            
            logger.info(f"Found {len(music_files)} music files")
            return music_files
            
        except Exception as e:
            logger.error(f"Error scanning directory {directory_path}: {str(e)}")
            raise
    
    def process_song(self, file_path: str) -> Dict:
        """
        Process a single song and extract its fingerprint.
        
        Args:
            file_path: Path to the audio file
            
        Returns:
            Dictionary containing fingerprint and metadata
        """
        try:
            logger.info(f"Processing song: {file_path}")
            
            # Get audio information
            audio_info = self.audio_processor.get_audio_info(file_path)
            
            # Process audio file to get fingerprint
            audio_data, mfccs, fingerprint = self.audio_processor.process_audio_file(file_path)
            
            # Create song data
            song_data = {
                'fingerprint': fingerprint,
                'metadata': {
                    'file_path': file_path,
                    'filename': os.path.basename(file_path),
                    'duration_seconds': audio_info['duration_seconds'],
                    'duration_minutes': audio_info['duration_minutes'],
                    'sample_rate': audio_info['sample_rate'],
                    'num_samples': audio_info['num_samples']
                }
            }
            
            logger.info(f"Successfully processed: {os.path.basename(file_path)}")
            return song_data
            
        except Exception as e:
            logger.error(f"Error processing song {file_path}: {str(e)}")
            raise
    
    def build_library(self, directory_path: str, recursive: bool = True, 
                     force_rebuild: bool = False) -> Dict:
        """
        Build the music library database by processing all songs in a directory.
        
        Args:
            directory_path: Path to the directory containing music files
            recursive: Whether to scan subdirectories recursively
            force_rebuild: Whether to rebuild even if database exists
            
        Returns:
            Dictionary containing library statistics
        """
        try:
            # Check if database already exists
            if os.path.exists(self.database_path) and not force_rebuild:
                logger.info("Loading existing library database...")
                self.load_library()
                return self.get_library_stats()
            
            logger.info("Building music library database...")
            
            # Scan for music files
            music_files = self.scan_directory(directory_path, recursive)
            
            if not music_files:
                logger.warning("No music files found in directory")
                return {'total_songs': 0, 'processed_songs': 0, 'failed_songs': 0}
            
            # Process each song
            processed_count = 0
            failed_count = 0
            
            for i, file_path in enumerate(music_files, 1):
                try:
                    logger.info(f"Processing song {i}/{len(music_files)}: {os.path.basename(file_path)}")
                    song_data = self.process_song(file_path)
                    self.library_data[file_path] = song_data
                    processed_count += 1
                    
                except Exception as e:
                    logger.error(f"Failed to process {file_path}: {str(e)}")
                    failed_count += 1
                    continue
            
            # Save the library database
            self.save_library()
            
            stats = {
                'total_songs': len(music_files),
                'processed_songs': processed_count,
                'failed_songs': failed_count,
                'success_rate': processed_count / len(music_files) if music_files else 0
            }
            
            logger.info(f"Library build complete: {stats}")
            return stats
            
        except Exception as e:
            logger.error(f"Error building library: {str(e)}")
            raise
    
    def save_library(self) -> None:
        """
        Save the library database to disk.
        """
        try:
            logger.info(f"Saving library database to: {self.database_path}")
            
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(self.database_path), exist_ok=True)
            
            # Convert numpy arrays to lists for JSON serialization
            serializable_data = {}
            for file_path, song_data in self.library_data.items():
                serializable_data[file_path] = {
                    'fingerprint': song_data['fingerprint'].tolist(),
                    'metadata': song_data['metadata']
                }
            
            with open(self.database_path, 'w') as f:
                json.dump(serializable_data, f, indent=2)
            
            logger.info("Library database saved successfully")
            
        except Exception as e:
            logger.error(f"Error saving library database: {str(e)}")
            raise
    
    def load_library(self) -> None:
        """
        Load the library database from disk.
        """
        try:
            logger.info(f"Loading library database from: {self.database_path}")
            
            with open(self.database_path, 'r') as f:
                serializable_data = json.load(f)
            
            # Convert lists back to numpy arrays
            self.library_data = {}
            for file_path, song_data in serializable_data.items():
                self.library_data[file_path] = {
                    'fingerprint': np.array(song_data['fingerprint']),
                    'metadata': song_data['metadata']
                }
            
            logger.info(f"Loaded {len(self.library_data)} songs from database")
            
        except Exception as e:
            logger.error(f"Error loading library database: {str(e)}")
            raise
    
    def calculate_similarity(self, fingerprint1: np.ndarray, fingerprint2: np.ndarray) -> float:
        """
        Calculate similarity between two fingerprints using Euclidean distance.
        
        Args:
            fingerprint1: First acoustic fingerprint
            fingerprint2: Second acoustic fingerprint
            
        Returns:
            Similarity score between 0 and 1 (1 = identical, 0 = completely different)
        """
        try:
            # Calculate Euclidean distance
            euclidean_distance = np.linalg.norm(fingerprint1 - fingerprint2)
            
            # Convert distance to similarity score (0-1)
            # Using exponential decay: similarity = exp(-distance/scale_factor)
            # Scale factor determines sensitivity - smaller values = more sensitive
            scale_factor = 50.0  # Adjust this to control sensitivity
            similarity = np.exp(-euclidean_distance / scale_factor)
            
            return float(similarity)
            
        except Exception as e:
            logger.error(f"Error calculating similarity: {str(e)}")
            raise
    
    def find_similar_songs(self, seed_file_path: str, top_n: int = 10, include_seed: bool = False) -> List[Tuple[str, float, Dict]]:
        """
        Find songs similar to a seed song.
        
        Args:
            seed_file_path: Path to the seed song
            top_n: Number of similar songs to return
            include_seed: Whether to include the seed song itself in results
            
        Returns:
            List of tuples: (file_path, similarity_score, metadata)
        """
        try:
            if not self.library_data:
                logger.warning("Library database is empty. Loading from disk...")
                self.load_library()
            
            if seed_file_path not in self.library_data:
                raise ValueError(f"Seed song not found in library: {seed_file_path}")
            
            logger.info(f"Finding songs similar to: {os.path.basename(seed_file_path)}")
            
            seed_fingerprint = self.library_data[seed_file_path]['fingerprint']
            similarities = []
            
            # Calculate similarity to all songs (including seed if requested)
            for file_path, song_data in self.library_data.items():
                if file_path == seed_file_path and not include_seed:
                    continue  # Skip the seed song itself unless requested
                
                similarity = self.calculate_similarity(seed_fingerprint, song_data['fingerprint'])
                similarities.append((file_path, similarity, song_data['metadata']))
            
            # Sort by similarity (highest first)
            similarities.sort(key=lambda x: x[1], reverse=True)
            
            # Return top N results
            top_results = similarities[:top_n]
            
            logger.info(f"Found {len(top_results)} similar songs")
            return top_results
            
        except Exception as e:
            logger.error(f"Error finding similar songs: {str(e)}")
            raise
    
    def get_library_stats(self) -> Dict:
        """
        Get statistics about the current library.
        
        Returns:
            Dictionary containing library statistics
        """
        if not self.library_data:
            return {'total_songs': 0, 'total_duration_minutes': 0}
        
        total_duration = sum(song_data['metadata']['duration_minutes'] 
                           for song_data in self.library_data.values())
        
        return {
            'total_songs': len(self.library_data),
            'total_duration_minutes': total_duration,
            'total_duration_hours': total_duration / 60,
            'average_duration_minutes': total_duration / len(self.library_data)
        }
    
    def get_song_list(self) -> List[Tuple[str, Dict]]:
        """
        Get a list of all songs in the library with their metadata.
        
        Returns:
            List of tuples: (file_path, metadata)
        """
        if not self.library_data:
            return []
        
        return [(file_path, song_data['metadata']) 
                for file_path, song_data in self.library_data.items()]
    
    def add_song_to_library(self, file_path: str) -> bool:
        """
        Add a single song to the library database.
        
        Args:
            file_path: Path to the audio file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if file_path in self.library_data:
                logger.info(f"Song already in library: {file_path}")
                return True
            
            song_data = self.process_song(file_path)
            self.library_data[file_path] = song_data
            
            # Save updated library
            self.save_library()
            
            logger.info(f"Successfully added song to library: {os.path.basename(file_path)}")
            return True
            
        except Exception as e:
            logger.error(f"Error adding song to library: {str(e)}")
            return False
