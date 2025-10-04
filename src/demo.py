"""
Demo script for Auto-DJ Phase 1: Audio Feature Extraction

This script demonstrates the audio processing capabilities implemented in Phase 1.
It shows how to load audio files, extract MFCC features, and generate acoustic fingerprints.
"""

import os
import sys
import numpy as np
from audio_processor import AudioProcessor
import matplotlib.pyplot as plt

def create_sample_audio():
    """
    Create a sample audio file for demonstration purposes.
    This generates a simple sine wave with some harmonics.
    """
    try:
        import librosa
        import soundfile as sf
        
        # Generate a sample audio signal (2 seconds of a 440Hz tone with harmonics)
        duration = 2.0
        sample_rate = 22050
        t = np.linspace(0, duration, int(sample_rate * duration), False)
        
        # Create a complex tone with fundamental and harmonics
        frequency = 440.0  # A4 note
        audio = (np.sin(2 * np.pi * frequency * t) + 
                0.5 * np.sin(2 * np.pi * frequency * 2 * t) + 
                0.25 * np.sin(2 * np.pi * frequency * 3 * t))
        
        # Normalize the audio
        audio = audio / np.max(np.abs(audio))
        
        # Save as WAV file
        sample_file = "sample_audio.wav"
        sf.write(sample_file, audio, sample_rate)
        print(f"Created sample audio file: {sample_file}")
        return sample_file
        
    except ImportError:
        print("Error: Required libraries not installed. Please run: pip install -r requirements.txt")
        return None

def demonstrate_audio_processing(file_path: str):
    """
    Demonstrate the complete audio processing pipeline.
    
    Args:
        file_path: Path to the audio file to process
    """
    print("=" * 60)
    print("Auto-DJ Phase 1: Audio Feature Extraction Demo")
    print("=" * 60)
    
    # Initialize the audio processor
    processor = AudioProcessor()
    
    try:
        # Get audio file information
        print("\n1. Audio File Information:")
        print("-" * 30)
        info = processor.get_audio_info(file_path)
        for key, value in info.items():
            if key == 'file_path':
                print(f"{key}: {value}")
            elif key == 'duration_minutes':
                print(f"{key}: {value:.2f}")
            else:
                print(f"{key}: {value}")
        
        # Process the audio file
        print("\n2. Processing Audio File:")
        print("-" * 30)
        audio_data, mfccs, fingerprint = processor.process_audio_file(file_path)
        
        # Display results
        print(f"Audio data shape: {audio_data.shape}")
        print(f"MFCC features shape: {mfccs.shape}")
        print(f"Acoustic fingerprint shape: {fingerprint.shape}")
        
        # Show fingerprint values
        print("\n3. Acoustic Fingerprint:")
        print("-" * 30)
        print("MFCC Coefficients (averaged across time):")
        for i, coeff in enumerate(fingerprint):
            print(f"  MFCC[{i:2d}]: {coeff:8.4f}")
        
        # Visualize the results
        visualize_audio_analysis(audio_data, mfccs, fingerprint, file_path)
        
        print("\n4. Summary:")
        print("-" * 30)
        print("✓ Audio file successfully loaded")
        print("✓ MFCC features extracted from audio segments")
        print("✓ Acoustic fingerprint generated")
        print("✓ Phase 1 implementation working correctly!")
        
    except Exception as e:
        print(f"Error during audio processing: {str(e)}")
        return False
    
    return True

def visualize_audio_analysis(audio_data, mfccs, fingerprint, file_path):
    """
    Create visualizations of the audio analysis results.
    
    Args:
        audio_data: Raw audio data
        mfccs: MFCC features
        fingerprint: Acoustic fingerprint
        file_path: Path to the audio file
    """
    try:
        # Create audio-waveforms directory if it doesn't exist
        output_dir = "audio-waveforms"
        os.makedirs(output_dir, exist_ok=True)
        
        fig, axes = plt.subplots(2, 2, figsize=(12, 8))
        fig.suptitle(f'Audio Analysis Results: {os.path.basename(file_path)}', fontsize=14)
        
        # Plot 1: Raw audio waveform
        time_axis = np.linspace(0, len(audio_data) / 22050, len(audio_data))
        axes[0, 0].plot(time_axis, audio_data)
        axes[0, 0].set_title('Raw Audio Waveform')
        axes[0, 0].set_xlabel('Time (seconds)')
        axes[0, 0].set_ylabel('Amplitude')
        axes[0, 0].grid(True)
        
        # Plot 2: MFCC features heatmap
        im = axes[0, 1].imshow(mfccs, aspect='auto', origin='lower', cmap='viridis')
        axes[0, 1].set_title('MFCC Features Over Time')
        axes[0, 1].set_xlabel('Time Frames')
        axes[0, 1].set_ylabel('MFCC Coefficients')
        plt.colorbar(im, ax=axes[0, 1])
        
        # Plot 3: Acoustic fingerprint (bar chart)
        axes[1, 0].bar(range(len(fingerprint)), fingerprint)
        axes[1, 0].set_title('Acoustic Fingerprint')
        axes[1, 0].set_xlabel('MFCC Coefficient Index')
        axes[1, 0].set_ylabel('Average Value')
        axes[1, 0].grid(True, alpha=0.3)
        
        # Plot 4: MFCC statistics
        mfcc_std = np.std(mfccs, axis=1)
        axes[1, 1].bar(range(len(mfcc_std)), mfcc_std)
        axes[1, 1].set_title('MFCC Standard Deviation')
        axes[1, 1].set_xlabel('MFCC Coefficient Index')
        axes[1, 1].set_ylabel('Standard Deviation')
        axes[1, 1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        # Save the plot with the same name as the audio file in audio-waveforms folder
        audio_filename = os.path.splitext(os.path.basename(file_path))[0]
        output_file = os.path.join(output_dir, f"{audio_filename}.png")
        plt.savefig(output_file, dpi=150, bbox_inches='tight')
        print(f"\nVisualization saved as: {output_file}")
        
        # Show the plot
        plt.show()
        
    except Exception as e:
        print(f"Warning: Could not create visualization: {str(e)}")

def main():
    """
    Main function to run the Phase 1 demonstration.
    """
    print("Auto-DJ Phase 1: Audio Feature Extraction")
    print("This demo shows how the system processes audio files to create acoustic fingerprints.")
    print("\nUsage:")
    print("  python demo.py                    # Use sample audio file")
    print("  python demo.py <audio_file_path>  # Use your own audio file")
    print("\nSupported formats: WAV, MP3, FLAC, M4A, etc.")
    print("Generated PNG analysis files will be saved in audio-waveforms/ folder")
    
    # Check if a file path was provided as command line argument
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        if not os.path.exists(file_path):
            print(f"\nError: File '{file_path}' not found.")
            print("Please provide a valid audio file path.")
            return
        print(f"\nUsing custom audio file: {file_path}")
    else:
        # Create a sample audio file for demonstration
        print("\nNo audio file provided. Creating a sample audio file...")
        file_path = create_sample_audio()
        if not file_path:
            return
    
    # Run the demonstration
    success = demonstrate_audio_processing(file_path)
    
    if success:
        print("\n" + "=" * 60)
        print("Phase 1 implementation completed successfully!")
        print("The system can now:")
        print("• Load audio files in various formats")
        print("• Extract MFCC features from audio segments")
        print("• Generate acoustic fingerprints for songs")
        print("• Save analysis visualizations in audio-waveforms/ folder")
        print("• Ready for Phase 2: Library scanning and similarity comparison")
        print("=" * 60)
    else:
        print("\nPhase 1 demonstration failed. Please check the error messages above.")

if __name__ == "__main__":
    main()

