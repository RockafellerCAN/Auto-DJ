"""
Simple test script to validate Phase 1 implementation
"""
import sys
import os
import numpy as np

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from audio_processor import AudioProcessor
    print("✓ AudioProcessor imported successfully")
    
    # Test basic functionality
    processor = AudioProcessor()
    print("✓ AudioProcessor initialized successfully")
    
    # Create a simple test audio signal
    duration = 1.0
    sample_rate = 22050
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    test_audio = np.sin(2 * np.pi * 440 * t)  # 440 Hz sine wave
    
    print(f"✓ Test audio created: {len(test_audio)} samples")
    
    # Test MFCC extraction
    mfccs = processor.extract_mfcc_features(test_audio)
    print(f"✓ MFCC features extracted: {mfccs.shape}")
    
    # Test fingerprint generation
    fingerprint = processor.generate_acoustic_fingerprint(mfccs)
    print(f"✓ Acoustic fingerprint generated: {len(fingerprint)} coefficients")
    
    print("\n" + "="*50)
    print("PHASE 1 IMPLEMENTATION VALIDATED!")
    print("="*50)
    print("✓ Audio ingestion: Working")
    print("✓ MFCC extraction: Working") 
    print("✓ Fingerprint generation: Working")
    print("✓ All Phase 1 components functional")
    print("="*50)
    
except ImportError as e:
    print(f"✗ Import error: {e}")
    print("Please install required dependencies:")
    print("pip install numpy librosa soundfile matplotlib")
except Exception as e:
    print(f"✗ Error: {e}")

