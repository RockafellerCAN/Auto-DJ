# Auto-DJ: AI-Powered Music Playlist Generator

An intelligent music playlist generator that analyzes your personal music library and creates playlists based on acoustic similarity. This project implements advanced audio signal processing techniques to understand music at a fundamental level and provides comprehensive library management with similarity analysis.

## Phase 1: Audio Feature Extraction ✅ COMPLETE

This phase implements the core audio processing functionality that teaches the computer to "listen" to music by extracting acoustic features and creating unique fingerprints for each song.

## Phase 2: Library Management and Similarity Engine ✅ COMPLETE

This phase builds upon Phase 1 to create a complete music library management system with intelligent similarity analysis, waveform generation, and comprehensive music discovery capabilities.

## Phase 3: User Interface and Playlist Generation ✅ COMPLETE

This phase creates a complete user-friendly application that transforms the underlying technology into a practical tool for creating intelligent playlists. It provides a clean command-line interface and generates standard M3U playlist files ready for any music player.

### What Phase 3 Accomplishes

1. **User-Friendly Interface**: Clean command-line application with step-by-step guidance
2. **Playlist Generation**: Intelligent playlist creation based on acoustic similarity analysis
3. **M3U File Creation**: Generates standard playlist files compatible with all major music players
4. **Metadata Generation**: Creates detailed JSON metadata files with playlist information
5. **Flexible Configuration**: Customizable playlist length, names, and seed song selection
6. **Direct Integration**: Seamlessly integrates with Phase 1 and Phase 2 systems
7. **Error Handling**: Robust error handling with graceful fallbacks and user guidance
8. **Cross-Platform Compatibility**: Works on Windows, macOS, and Linux systems

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

**Phase 3 Features:**
- **Interactive CLI**: Step-by-step user interface with clear guidance and validation
- **Playlist Generation**: AI-powered playlist creation based on acoustic similarity
- **M3U Playlist Files**: Standard playlist format compatible with all music players
- **Metadata Files**: Detailed JSON metadata with song information and similarity scores
- **Flexible Configuration**: Customizable playlist length, names, and seed song selection
- **Error Recovery**: Robust error handling with graceful fallbacks and user guidance
- **Cross-Platform**: Works seamlessly on Windows, macOS, and Linux systems
- **Direct Integration**: Seamless integration with Phase 1 and Phase 2 systems

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

#### Phase 3: User Interface and Playlist Generation

Create intelligent playlists with a user-friendly interface:

```bash
# Basic usage - specify your music library folder
python auto_dj.py audio-library

# Custom playlist settings
python auto_dj.py audio-library --playlist-length 10 --playlist-name my_mix

# Get help
python auto_dj.py --help
```

The application will guide you through:
1. **Loading your music library** - Scans and processes all audio files
2. **Selecting a seed song** - Choose the song to base your playlist on
3. **Customizing settings** - Set playlist length and name
4. **Generating playlist** - AI analyzes acoustic similarity
5. **Previewing results** - See your generated playlist with similarity scores
6. **Saving files** - Creates M3U playlist and metadata files

Generated files are saved directly in your music library folder:
```
<music_folder>/
├── your_playlist.m3u              # M3U playlist file
├── your_playlist_metadata.json    # Detailed metadata
├── song1.mp3
├── song2.mp3
└── ...
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
│   ├── library_manager.py   # Phase 2: Library management and similarity
│   ├── playlist_generator.py # Phase 3: Playlist generation and M3U creation
│   └── user_interface.py    # Phase 3: Interactive user interface
├── tests/
│   ├── __init__.py
│   └── test_audio_processor.py  # Unit and integration tests
├── temp/
│   ├── PHASE1_SUMMARY.md    # Phase 1 completion documentation
│   ├── PHASE2_SUMMARY.md    # Phase 2 completion documentation
│   ├── PHASE3_SUMMARY.md    # Phase 3 completion documentation
│   ├── project-plan.md      # Original project plan
│   └── prompts.md          # Development prompts and documentation
├── audio-samples/           # Sample audio files for testing
│   └── deep-abstract-ambient_snowcap.mp3
├── audio-library/           # Example music library with analysis
│   ├── auto-dj/            # Generated analysis files
│   │   ├── music_library.db
│   │   ├── similarity_matrix.json
│   │   ├── similarity_matrix.csv
│   │   └── waveforms-library/
│   ├── *.m3u              # Generated playlist files
│   └── *_metadata.json   # Generated metadata files
├── audio-waveforms/         # Generated visualization files
├── auto_dj.py              # Phase 3: Main user application
├── test_phase1.py          # Phase 1 validation script
├── test_phase2.py          # Phase 2 validation script
├── test_phase3.py          # Phase 3 validation script
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
<img width="1784" height="1181" alt="deep-abstract-ambient_snowcap" src="https://github.com/soroush-thr/Auto-DJ/blob/main/audio-waveforms/deep-abstract-ambient_snowcap.png" />

### Project Completion Status

All three phases are now complete! The Auto-DJ system provides a comprehensive solution for intelligent music playlist generation:

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

**Phase 3 Capabilities:**
- ✅ Interactive command-line interface with step-by-step guidance
- ✅ Intelligent playlist generation based on acoustic similarity analysis
- ✅ M3U playlist file creation compatible with all major music players
- ✅ Detailed metadata generation with song information and similarity scores
- ✅ Flexible configuration options for playlist length and naming
- ✅ Robust error handling with graceful fallbacks and user guidance
- ✅ Cross-platform compatibility (Windows, macOS, Linux)
- ✅ Seamless integration with Phase 1 and Phase 2 systems

**Complete System Ready**: The Auto-DJ system is now a fully functional, production-ready application for intelligent music playlist generation.

### Project Status

- **Phase 1**: ✅ **COMPLETE** - Audio feature extraction and fingerprinting
- **Phase 2**: ✅ **COMPLETE** - Library management and similarity engine
- **Phase 3**: ✅ **COMPLETE** - User interface and playlist generation

**🎉 PROJECT COMPLETE**: All phases successfully implemented and integrated!

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

*This project implements the complete Auto-DJ system as described in the project plan. All three phases are now complete, providing a fully functional intelligent music playlist generator that analyzes acoustic similarity and creates playlists ready for any music player.*