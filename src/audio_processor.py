"""
Audio Processing Module for Auto-DJ Phase 1

This module handles the core audio feature extraction functionality:
- Audio file ingestion and loading
- MFCC feature extraction
- Acoustic fingerprint generation
"""

import librosa
import numpy as np
import soundfile as sf
from typing import Tuple, Optional, List
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AudioProcessor:
    """
    Main class for processing audio files and extracting acoustic features.
    
    This class implements the Phase 1 functionality of the Auto-DJ project:
    1. Ingestion: Load audio files from various formats
    2. Analysis: Extract MFCC features from audio segments
    3. Fingerprinting: Generate acoustic fingerprints by averaging MFCCs
    """
    
    def __init__(self, 
                 sample_rate: int = 22050,
                 n_mfcc: int = 13,
                 hop_length: int = 512,
                 n_fft: int = 2048):
        """
        Initialize the AudioProcessor with audio processing parameters.
        
        Args:
            sample_rate: Target sample rate for audio processing (Hz)
            n_mfcc: Number of MFCC coefficients to extract
            hop_length: Number of samples between successive frames
            n_fft: Length of the windowed signal for FFT
        """
        self.sample_rate = sample_rate
        self.n_mfcc = n_mfcc
        self.hop_length = hop_length
        self.n_fft = n_fft
        
    def load_audio(self, file_path: str) -> Tuple[np.ndarray, int]:
        """
        Load an audio file and return the audio data and sample rate.
        
        Args:
            file_path: Path to the audio file
            
        Returns:
            Tuple of (audio_data, sample_rate)
            
        Raises:
            FileNotFoundError: If the audio file doesn't exist
            Exception: If there's an error loading the audio file
        """
        try:
            logger.info(f"Loading audio file: {file_path}")
            audio_data, sr = librosa.load(file_path, sr=self.sample_rate)
            logger.info(f"Successfully loaded audio: {len(audio_data)} samples at {sr} Hz")
            return audio_data, sr
        except FileNotFoundError:
            logger.error(f"Audio file not found: {file_path}")
            raise
        except Exception as e:
            logger.error(f"Error loading audio file {file_path}: {str(e)}")
            raise
    
    def extract_mfcc_features(self, audio_data: np.ndarray) -> np.ndarray:
        """
        Extract MFCC features from audio data.
        
        This method analyzes the audio in short, overlapping segments and extracts
        Mel-Frequency Cepstral Coefficients (MFCCs) for each segment. MFCCs are
        particularly effective for music analysis as they model human auditory perception.
        
        Args:
            audio_data: Audio signal as a numpy array
            
        Returns:
            MFCC features as a numpy array of shape (n_mfcc, n_frames)
        """
        try:
            logger.info("Extracting MFCC features...")
            
            # Extract MFCC features
            mfccs = librosa.feature.mfcc(
                y=audio_data,
                sr=self.sample_rate,
                n_mfcc=self.n_mfcc,
                hop_length=self.hop_length,
                n_fft=self.n_fft
            )
            
            logger.info(f"Extracted MFCC features: {mfccs.shape}")
            return mfccs
            
        except Exception as e:
            logger.error(f"Error extracting MFCC features: {str(e)}")
            raise
    
    def generate_acoustic_fingerprint(self, mfccs: np.ndarray) -> np.ndarray:
        """
        Generate an acoustic fingerprint by averaging MFCC coefficients.
        
        This method takes the MFCC features extracted from all segments of a song
        and creates a single, compact representation by averaging across time.
        This creates a unique "fingerprint" that summarizes the song's overall
        acoustic characteristics.
        
        Args:
            mfccs: MFCC features as a numpy array of shape (n_mfcc, n_frames)
            
        Returns:
            Acoustic fingerprint as a numpy array of length n_mfcc
        """
        try:
            logger.info("Generating acoustic fingerprint...")
            
            # Average MFCC coefficients across time to create fingerprint
            fingerprint = np.mean(mfccs, axis=1)
            
            logger.info(f"Generated fingerprint with {len(fingerprint)} coefficients")
            return fingerprint
            
        except Exception as e:
            logger.error(f"Error generating acoustic fingerprint: {str(e)}")
            raise
    
    def process_audio_file(self, file_path: str) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Complete audio processing pipeline for a single file.
        
        This method combines all Phase 1 steps:
        1. Load the audio file
        2. Extract MFCC features
        3. Generate acoustic fingerprint
        
        Args:
            file_path: Path to the audio file
            
        Returns:
            Tuple of (audio_data, mfcc_features, acoustic_fingerprint)
        """
        try:
            logger.info(f"Processing audio file: {file_path}")
            
            # Step 1: Ingestion
            audio_data, sample_rate = self.load_audio(file_path)
            
            # Step 2: Analysis - Extract MFCC features
            mfccs = self.extract_mfcc_features(audio_data)
            
            # Step 3: Fingerprinting - Generate acoustic fingerprint
            fingerprint = self.generate_acoustic_fingerprint(mfccs)
            
            logger.info("Audio processing completed successfully")
            return audio_data, mfccs, fingerprint
            
        except Exception as e:
            logger.error(f"Error processing audio file {file_path}: {str(e)}")
            raise
    
    def get_audio_info(self, file_path: str) -> dict:
        """
        Get basic information about an audio file.
        
        Args:
            file_path: Path to the audio file
            
        Returns:
            Dictionary containing audio file information
        """
        try:
            audio_data, sr = self.load_audio(file_path)
            duration = len(audio_data) / sr
            
            info = {
                'file_path': file_path,
                'sample_rate': sr,
                'duration_seconds': duration,
                'duration_minutes': duration / 60,
                'num_samples': len(audio_data),
                'channels': 1  # librosa loads as mono
            }
            
            return info
            
        except Exception as e:
            logger.error(f"Error getting audio info for {file_path}: {str(e)}")
            raise

