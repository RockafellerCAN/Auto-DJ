"""
Unit tests for the AudioProcessor class in Phase 1.

These tests validate the core functionality of audio feature extraction
and acoustic fingerprint generation.
"""

import unittest
import numpy as np
import os
import tempfile
import soundfile as sf
from unittest.mock import patch, MagicMock

# Add the src directory to the path so we can import our modules
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from audio_processor import AudioProcessor


class TestAudioProcessor(unittest.TestCase):
    """Test cases for the AudioProcessor class."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.processor = AudioProcessor()
        self.temp_dir = tempfile.mkdtemp()
        
        # Create a test audio file
        self.test_audio_file = os.path.join(self.temp_dir, "test_audio.wav")
        self._create_test_audio_file()
    
    def tearDown(self):
        """Clean up after each test method."""
        # Clean up temporary files
        if os.path.exists(self.test_audio_file):
            os.remove(self.test_audio_file)
        os.rmdir(self.temp_dir)
    
    def _create_test_audio_file(self):
        """Create a simple test audio file."""
        # Generate a 1-second sine wave at 440 Hz
        duration = 1.0
        sample_rate = 22050
        t = np.linspace(0, duration, int(sample_rate * duration), False)
        audio = np.sin(2 * np.pi * 440 * t)  # 440 Hz sine wave
        
        # Save as WAV file
        sf.write(self.test_audio_file, audio, sample_rate)
    
    def test_initialization(self):
        """Test AudioProcessor initialization with default parameters."""
        processor = AudioProcessor()
        self.assertEqual(processor.sample_rate, 22050)
        self.assertEqual(processor.n_mfcc, 13)
        self.assertEqual(processor.hop_length, 512)
        self.assertEqual(processor.n_fft, 2048)
    
    def test_initialization_custom_params(self):
        """Test AudioProcessor initialization with custom parameters."""
        processor = AudioProcessor(
            sample_rate=44100,
            n_mfcc=20,
            hop_length=1024,
            n_fft=4096
        )
        self.assertEqual(processor.sample_rate, 44100)
        self.assertEqual(processor.n_mfcc, 20)
        self.assertEqual(processor.hop_length, 1024)
        self.assertEqual(processor.n_fft, 4096)
    
    def test_load_audio_success(self):
        """Test successful audio loading."""
        audio_data, sample_rate = self.processor.load_audio(self.test_audio_file)
        
        self.assertIsInstance(audio_data, np.ndarray)
        self.assertIsInstance(sample_rate, int)
        self.assertEqual(sample_rate, 22050)
        self.assertGreater(len(audio_data), 0)
    
    def test_load_audio_file_not_found(self):
        """Test audio loading with non-existent file."""
        with self.assertRaises(FileNotFoundError):
            self.processor.load_audio("nonexistent_file.wav")
    
    def test_extract_mfcc_features(self):
        """Test MFCC feature extraction."""
        audio_data, _ = self.processor.load_audio(self.test_audio_file)
        mfccs = self.processor.extract_mfcc_features(audio_data)
        
        self.assertIsInstance(mfccs, np.ndarray)
        self.assertEqual(mfccs.shape[0], self.processor.n_mfcc)
        self.assertGreater(mfccs.shape[1], 0)  # Should have multiple time frames
    
    def test_generate_acoustic_fingerprint(self):
        """Test acoustic fingerprint generation."""
        # Create mock MFCC data
        n_mfcc = 13
        n_frames = 100
        mock_mfccs = np.random.randn(n_mfcc, n_frames)
        
        fingerprint = self.processor.generate_acoustic_fingerprint(mock_mfccs)
        
        self.assertIsInstance(fingerprint, np.ndarray)
        self.assertEqual(len(fingerprint), n_mfcc)
        self.assertEqual(fingerprint.shape, (n_mfcc,))
    
    def test_process_audio_file_complete_pipeline(self):
        """Test the complete audio processing pipeline."""
        audio_data, mfccs, fingerprint = self.processor.process_audio_file(self.test_audio_file)
        
        # Check audio data
        self.assertIsInstance(audio_data, np.ndarray)
        self.assertGreater(len(audio_data), 0)
        
        # Check MFCC features
        self.assertIsInstance(mfccs, np.ndarray)
        self.assertEqual(mfccs.shape[0], self.processor.n_mfcc)
        
        # Check fingerprint
        self.assertIsInstance(fingerprint, np.ndarray)
        self.assertEqual(len(fingerprint), self.processor.n_mfcc)
    
    def test_get_audio_info(self):
        """Test audio file information retrieval."""
        info = self.processor.get_audio_info(self.test_audio_file)
        
        self.assertIsInstance(info, dict)
        self.assertIn('file_path', info)
        self.assertIn('sample_rate', info)
        self.assertIn('duration_seconds', info)
        self.assertIn('duration_minutes', info)
        self.assertIn('num_samples', info)
        self.assertIn('channels', info)
        
        self.assertEqual(info['file_path'], self.test_audio_file)
        self.assertEqual(info['sample_rate'], 22050)
        self.assertGreater(info['duration_seconds'], 0)
        self.assertGreater(info['num_samples'], 0)
        self.assertEqual(info['channels'], 1)
    
    def test_fingerprint_consistency(self):
        """Test that the same audio file produces consistent fingerprints."""
        # Process the same file twice
        _, _, fingerprint1 = self.processor.process_audio_file(self.test_audio_file)
        _, _, fingerprint2 = self.processor.process_audio_file(self.test_audio_file)
        
        # Fingerprints should be identical
        np.testing.assert_array_almost_equal(fingerprint1, fingerprint2, decimal=10)
    
    def test_fingerprint_different_audio(self):
        """Test that different audio files produce different fingerprints."""
        # Create a second test audio file with different frequency
        test_audio_file2 = os.path.join(self.temp_dir, "test_audio2.wav")
        duration = 1.0
        sample_rate = 22050
        t = np.linspace(0, duration, int(sample_rate * duration), False)
        audio = np.sin(2 * np.pi * 880 * t)  # 880 Hz sine wave (different frequency)
        sf.write(test_audio_file2, audio, sample_rate)
        
        try:
            # Process both files
            _, _, fingerprint1 = self.processor.process_audio_file(self.test_audio_file)
            _, _, fingerprint2 = self.processor.process_audio_file(test_audio_file2)
            
            # Fingerprints should be different
            self.assertFalse(np.allclose(fingerprint1, fingerprint2, atol=1e-6))
            
        finally:
            # Clean up
            if os.path.exists(test_audio_file2):
                os.remove(test_audio_file2)
    
    def test_error_handling_invalid_file(self):
        """Test error handling with invalid audio file."""
        # Create an invalid audio file (empty file)
        invalid_file = os.path.join(self.temp_dir, "invalid.wav")
        with open(invalid_file, 'w') as f:
            f.write("not audio data")
        
        try:
            with self.assertRaises(Exception):
                self.processor.process_audio_file(invalid_file)
        finally:
            if os.path.exists(invalid_file):
                os.remove(invalid_file)


class TestAudioProcessorIntegration(unittest.TestCase):
    """Integration tests for the AudioProcessor class."""
    
    def setUp(self):
        """Set up test fixtures for integration tests."""
        self.processor = AudioProcessor()
    
    def test_phase1_workflow(self):
        """Test the complete Phase 1 workflow as described in the project plan."""
        # This test validates that Phase 1 works as intended:
        # 1. Ingestion: Load audio file
        # 2. Analysis: Extract MFCC features from segments
        # 3. Fingerprinting: Generate acoustic fingerprint
        
        # Create a more complex test audio file
        temp_dir = tempfile.mkdtemp()
        test_file = os.path.join(temp_dir, "complex_test.wav")
        
        try:
            # Generate a complex audio signal with multiple frequencies
            duration = 2.0
            sample_rate = 22050
            t = np.linspace(0, duration, int(sample_rate * duration), False)
            
            # Create a complex tone with multiple harmonics
            audio = (np.sin(2 * np.pi * 220 * t) +  # A3
                    0.7 * np.sin(2 * np.pi * 440 * t) +  # A4
                    0.5 * np.sin(2 * np.pi * 660 * t) +  # E5
                    0.3 * np.sin(2 * np.pi * 880 * t))   # A5
            
            # Add some amplitude modulation
            audio *= (1 + 0.3 * np.sin(2 * np.pi * 2 * t))
            
            # Normalize
            audio = audio / np.max(np.abs(audio))
            
            # Save the file
            sf.write(test_file, audio, sample_rate)
            
            # Test the complete Phase 1 workflow
            audio_data, mfccs, fingerprint = self.processor.process_audio_file(test_file)
            
            # Validate results
            self.assertIsInstance(audio_data, np.ndarray)
            self.assertIsInstance(mfccs, np.ndarray)
            self.assertIsInstance(fingerprint, np.ndarray)
            
            # Check that we have the expected number of MFCC coefficients
            self.assertEqual(len(fingerprint), 13)
            
            # Check that the fingerprint is reasonable (not all zeros or NaNs)
            self.assertFalse(np.all(fingerprint == 0))
            self.assertFalse(np.any(np.isnan(fingerprint)))
            self.assertFalse(np.any(np.isinf(fingerprint)))
            
            print(f"\nPhase 1 Integration Test Results:")
            print(f"Audio duration: {len(audio_data) / sample_rate:.2f} seconds")
            print(f"MFCC shape: {mfccs.shape}")
            print(f"Fingerprint: {fingerprint}")
            
        finally:
            # Clean up
            if os.path.exists(test_file):
                os.remove(test_file)
            os.rmdir(temp_dir)


if __name__ == '__main__':
    # Run the tests
    unittest.main(verbosity=2)

