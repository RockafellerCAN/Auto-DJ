# Auto-DJ: AI-Powered Music Playlist Generator

An intelligent music playlist generator that analyzes your personal music library and creates playlists based on acoustic similarity. This project implements advanced audio signal processing techniques to understand music at a fundamental level.

## Phase 1: Audio Feature Extraction ✅ COMPLETE

This phase implements the core audio processing functionality that teaches the computer to "listen" to music by extracting acoustic features and creating unique fingerprints for each song. The system can now process audio files, extract meaningful features, and generate acoustic fingerprints that represent the unique characteristics of each piece of music.

### What Phase 1 Accomplishes

1. **Ingestion**: Loads audio files in various formats (MP3, WAV, FLAC, M4A, etc.)
2. **Analysis**: Extracts Mel-Frequency Cepstral Coefficients (MFCCs) from audio segments using industry-standard techniques
3. **Fingerprinting**: Creates acoustic fingerprints by averaging MFCC coefficients across time
4. **Visualization**: Generates comprehensive audio analysis visualizations and saves them as PNG files
5. **Testing**: Comprehensive test suite with unit tests, integration tests, and validation scripts

### Features

- **Multi-format Support**: Handles common audio formats (WAV, MP3, FLAC, M4A, etc.)
- **MFCC Feature Extraction**: Uses industry-standard audio analysis techniques with configurable parameters
- **Acoustic Fingerprinting**: Creates compact, meaningful representations of songs using averaged MFCC coefficients
- **Audio Visualization**: Generates comprehensive visualizations including waveform plots, MFCC heatmaps, and fingerprint charts
- **Robust Error Handling**: Graceful handling of invalid files and processing errors with detailed logging
- **Comprehensive Testing**: Full test suite with unit tests, integration tests, and validation scripts
- **Demo Script**: Interactive demonstration script with sample audio generation
- **Modular Design**: Clean, well-documented code structure ready for Phase 2 integration

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/soroush-thr/Auto-DJ.git
   cd Auto-DJ
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

### Usage

#### Basic Usage

```python
from src.audio_processor import AudioProcessor

# Initialize the processor
processor = AudioProcessor()

# Process an audio file
audio_data, mfccs, fingerprint = processor.process_audio_file("path/to/your/song.mp3")

print(f"Acoustic fingerprint: {fingerprint}")
```

#### Demo Script

Run the demonstration script to see Phase 1 in action:

```bash
# With a sample audio file (creates one automatically)
python src/demo.py

# With your own audio file
python src/demo.py "path/to/your/song.mp3"
```

The demo will:
- Load and analyze the audio file
- Extract MFCC features
- Generate an acoustic fingerprint
- Create visualizations of the analysis
- Display detailed information about the process

#### Running Tests

```bash
# Run all tests
python -m pytest tests/

# Run with verbose output
python -m pytest tests/ -v

# Run specific test file
python tests/test_audio_processor.py
```

### Technical Details

#### Audio Processing Pipeline

1. **Audio Loading**: Uses `librosa` to load audio files and normalize sample rates
2. **MFCC Extraction**: Analyzes audio in short, overlapping segments using FFT
3. **Feature Averaging**: Creates fingerprints by averaging MFCC coefficients across time

#### Key Parameters

- **Sample Rate**: 22,050 Hz (standard for music analysis)
- **MFCC Coefficients**: 13 (standard for speech/music analysis)
- **Hop Length**: 512 samples (overlap between analysis windows)
- **FFT Size**: 2048 samples (frequency resolution)

#### File Structure

```
Auto-DJ/
├── src/
│   ├── __init__.py
│   ├── audio_processor.py    # Main audio processing class
│   └── demo.py              # Demonstration script with visualization
├── tests/
│   ├── __init__.py
│   └── test_audio_processor.py  # Unit and integration tests
├── audio-samples/           # Sample audio files for testing
│   └── deep-abstract-ambient_snowcap.mp3
├── audio-waveforms/         # Generated visualization files
│   ├── deep-abstract-ambient_snowcap.png
│   └── README.md
├── temp/                    # Temporary files and project planning
│   ├── project-plan.md
│   └── prompts.md
├── test_phase1.py          # Phase 1 validation script
├── requirements.txt        # Python dependencies
├── .gitignore             # Git ignore patterns
└── README.md              # This file
```

### Dependencies

- **librosa** (≥0.10.1): Audio and music signal analysis
- **numpy** (≥1.24.0): Numerical computing
- **scipy** (≥1.10.0): Scientific computing
- **soundfile** (≥0.12.1): Audio file I/O
- **matplotlib** (≥3.7.0): Visualization and plotting

### Example Output

When processing an audio file, you'll see output like:

```
Audio File Information:
file_path: sample_audio.wav
sample_rate: 22050
duration_seconds: 2.00
duration_minutes: 0.03
num_samples: 44100
channels: 1

Acoustic Fingerprint:
MFCC Coefficients (averaged across time):
  MFCC[ 0]:  -12.3456
  MFCC[ 1]:    8.2341
  MFCC[ 2]:   -3.4567
  ... (13 coefficients total)

<img width="1784" height="1181" alt="deep-abstract-ambient_snowcap" src="https://github.com/soroush-thr/Auto-DJ/blob/main/audio-waveforms/deep-abstract-ambient_snowcap.png" />

```

### Next Steps

Phase 1 is now complete! The system can successfully:
- ✅ Load audio files from various formats (MP3, WAV, FLAC, M4A, etc.)
- ✅ Extract meaningful acoustic features (MFCCs) with configurable parameters
- ✅ Generate unique acoustic fingerprints for songs using averaged coefficients
- ✅ Create comprehensive audio analysis visualizations
- ✅ Handle errors gracefully with detailed logging
- ✅ Provide comprehensive testing with unit and integration tests
- ✅ Generate sample audio files for demonstration
- ✅ Save analysis results as PNG visualizations

**Ready for Phase 2**: Library scanning and similarity comparison engine.

### Project Status

- **Phase 1**: ✅ **COMPLETE** - Audio feature extraction and fingerprinting
- **Phase 2**: 🔄 **PLANNED** - Music library scanning and similarity comparison
- **Phase 3**: 🔄 **PLANNED** - Playlist generation and recommendation engine

### Troubleshooting

**Common Issues**:

1. **ImportError**: Make sure all dependencies are installed (`pip install -r requirements.txt`)
2. **FileNotFoundError**: Check that the audio file path is correct
3. **Audio loading errors**: Ensure the file is a valid audio format

**Getting Help**:

- Check the test files for usage examples
- Run the demo script to see the system in action
- Review the detailed docstrings in `audio_processor.py`

---

*This project implements Phase 1 of the Auto-DJ system as described in the project plan. The acoustic fingerprinting system is now ready to be integrated with a music library scanner and similarity engine in Phase 2.*
