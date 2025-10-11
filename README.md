# Auto-DJ: AI-Powered Music Playlist Generator

An intelligent music playlist generator that analyzes your personal music library and creates playlists based on acoustic similarity. This project implements advanced audio signal processing techniques to understand music at a fundamental level and provides comprehensive library management with similarity analysis.

## Phase 1: Audio Feature Extraction ✅ COMPLETE

This phase implements the core audio processing functionality that teaches the computer to "listen" to music by extracting acoustic features and creating unique fingerprints for each song.

## Phase 2: Library Management and Similarity Engine ✅ COMPLETE

This phase builds upon Phase 1 to create a complete music library management system with intelligent similarity analysis, waveform generation, and comprehensive music discovery capabilities.

### What Phase 2 Accomplishes

1. **Library Scanning**: Discovers and catalogs music files from any directory with recursive scanning support
2. **Database Management**: Creates persistent JSON databases storing acoustic fingerprints and metadata
3. **Similarity Analysis**: Uses Euclidean distance-based similarity calculation for accurate music comparison
4. **Waveform Generation**: Creates high-quality visual waveform representations for all processed songs
5. **Similarity Matrix**: Generates complete pairwise similarity analysis in JSON and CSV formats
6. **Organized Output**: Maintains structured folder organization keeping analysis with music collections
7. **Command-Line Interface**: Flexible CLI for processing any music directory
8. **Comprehensive Testing**: Full validation suite for all Phase 2 components

### Features

**Phase 1 Features:**
- **Multi-format Support**: Handles common audio formats (WAV, MP3, FLAC, M4A, etc.)
- **MFCC Feature Extraction**: Uses industry-standard audio analysis techniques with configurable parameters
- **Acoustic Fingerprinting**: Creates compact, meaningful representations of songs using averaged MFCC coefficients
- **Audio Visualization**: Generates comprehensive visualizations including waveform plots, MFCC heatmaps, and fingerprint charts
- **Robust Error Handling**: Graceful handling of invalid files and processing errors with detailed logging
- **Comprehensive Testing**: Full test suite with unit tests, integration tests, and validation scripts
- **Demo Script**: Interactive demonstration script with sample audio generation

**Phase 2 Features:**
- **Command-Line Interface**: Process any music directory with flexible CLI options
- **Library Management**: Complete music library scanning and database management
- **Similarity Engine**: Advanced Euclidean distance-based similarity calculation
- **Waveform Generation**: High-quality PNG waveform visualizations for all songs
- **Similarity Matrix**: Complete pairwise similarity analysis in multiple formats
- **Organized Output**: Structured folder organization keeping analysis with music collections
- **Persistent Storage**: JSON-based database system for fast loading and reuse
- **Recursive Scanning**: Optional subdirectory scanning for comprehensive library coverage

### Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
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

#### Phase 2: Library Management and Similarity Analysis

Process entire music libraries with comprehensive analysis:

```bash
# Process a music directory
python test_phase2.py audio-library

# Process with recursive scanning (default)
python test_phase2.py "C:\Music Collection"

# Non-recursive scanning
python test_phase2.py audio-library --no-recursive

# Get help
python test_phase2.py --help
```

This will create an organized analysis in your music directory:

```
<music_folder>/
├── auto-dj/
│   ├── music_library.db          # Main database
│   ├── similarity_matrix.json     # Detailed similarity data
│   ├── similarity_matrix.csv      # Matrix view
│   └── waveforms-library/         # Waveform images
│       ├── song1_waveform.png
│       ├── song2_waveform.png
│       └── ...
```

#### Using the Library Manager Programmatically

```python
from src.library_manager import LibraryManager
from src.audio_processor import AudioProcessor

# Initialize components
audio_processor = AudioProcessor()
library_manager = LibraryManager(audio_processor)

# Build library from directory
stats = library_manager.build_library("/path/to/music", recursive=True)
print(f"Processed {stats['processed_songs']} songs")

# Find similar songs
recommendations = library_manager.find_similar_songs(
    "path/to/seed_song.mp3", 
    top_n=10
)

for file_path, similarity, metadata in recommendations:
    print(f"{metadata['filename']}: {similarity:.3f}")
```

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
│   ├── audio_processor.py   # Phase 1: Audio processing class
│   └── library_manager.py   # Phase 2: Library management and similarity
├── tests/
│   ├── __init__.py
│   └── test_audio_processor.py  # Unit and integration tests
├── audio-samples/           # Sample audio files for testing
│   └── deep-abstract-ambient_snowcap.mp3
├── audio-library/           # Example music library with analysis
│   └── auto-dj/            # Generated analysis files
│       ├── music_library.db
│       ├── similarity_matrix.json
│       ├── similarity_matrix.csv
│       └── waveforms-library/
├── audio-waveforms/         # Generated visualization files
├── test_phase1.py          # Phase 1 validation script
├── test_phase2.py          # Phase 2 validation script
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
- **scikit-learn** (≥1.3.0): Machine learning and similarity calculations

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
```

### Next Steps

Phase 1 and Phase 2 are now complete! The system can successfully:

**Phase 1 Capabilities:**
- ✅ Load audio files from various formats (MP3, WAV, FLAC, M4A, etc.)
- ✅ Extract meaningful acoustic features (MFCCs) with configurable parameters
- ✅ Generate unique acoustic fingerprints for songs using averaged coefficients
- ✅ Create comprehensive audio analysis visualizations
- ✅ Handle errors gracefully with detailed logging
- ✅ Provide comprehensive testing with unit and integration tests

**Phase 2 Capabilities:**
- ✅ Scan and catalog entire music libraries from any directory
- ✅ Create persistent databases with acoustic fingerprints and metadata
- ✅ Calculate accurate similarity scores using Euclidean distance
- ✅ Generate high-quality waveform visualizations for all songs
- ✅ Create comprehensive similarity matrices in multiple formats
- ✅ Organize analysis files in structured folder hierarchies
- ✅ Provide flexible command-line interface for any music directory
- ✅ Support recursive scanning of subdirectories

**Ready for Phase 3**: User interface and playlist generation engine.

### Project Status

- **Phase 1**: ✅ **COMPLETE** - Audio feature extraction and fingerprinting
- **Phase 2**: ✅ **COMPLETE** - Library management and similarity engine
- **Phase 3**: 🔄 **PLANNED** - User interface and playlist generation

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

*This project implements Phase 1 and Phase 2 of the Auto-DJ system as described in the project plan. The complete library management and similarity analysis system is now ready for Phase 3: user interface and playlist generation.*