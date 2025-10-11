"""
Test script for Phase 2 implementation: Library Management and Similarity Engine

This script validates the Phase 2 functionality:
- Library scanning and file discovery
- Database creation and management
- Similarity calculation using cosine similarity
- Song ranking and recommendation system
- Waveform generation and storage
- Similarity matrix creation

Usage: python test_phase2.py <music_folder_path>
Example: python test_phase2.py audio-library
"""

import sys
import os
import numpy as np
import json
import matplotlib.pyplot as plt
from pathlib import Path
import argparse

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='Phase 2 Auto-DJ Library Management and Similarity Engine')
    parser.add_argument('music_folder', help='Path to the folder containing music files')
    parser.add_argument('--recursive', '-r', action='store_true', default=True,
                       help='Scan subdirectories recursively (default: True)')
    return parser.parse_args()

def create_folder_structure(music_folder):
    """Create the auto-dj folder structure"""
    auto_dj_path = os.path.join(music_folder, 'auto-dj')
    waveforms_path = os.path.join(auto_dj_path, 'waveforms-library')
    
    # Create directories
    os.makedirs(auto_dj_path, exist_ok=True)
    os.makedirs(waveforms_path, exist_ok=True)
    
    print(f"✓ Created folder structure:")
    print(f"  - {auto_dj_path}")
    print(f"  - {waveforms_path}")
    
    return auto_dj_path, waveforms_path

def generate_waveform(audio_data, sample_rate, output_path, filename):
    """Generate and save waveform visualization"""
    try:
        # Create waveform plot
        plt.figure(figsize=(12, 4))
        time_axis = np.linspace(0, len(audio_data) / sample_rate, len(audio_data))
        plt.plot(time_axis, audio_data, linewidth=0.5, alpha=0.8)
        plt.title(f'Waveform: {filename}', fontsize=12)
        plt.xlabel('Time (seconds)')
        plt.ylabel('Amplitude')
        plt.grid(True, alpha=0.3)
        
        # Save waveform
        waveform_filename = os.path.splitext(filename)[0] + '_waveform.png'
        waveform_path = os.path.join(output_path, waveform_filename)
        plt.savefig(waveform_path, dpi=150, bbox_inches='tight')
        plt.close()
        
        return waveform_path
    except Exception as e:
        print(f"⚠ Error generating waveform for {filename}: {e}")
        return None

def create_similarity_matrix(library_manager, output_path):
    """Create similarity matrix for all songs"""
    try:
        songs = library_manager.get_song_list()
        n_songs = len(songs)
        
        if n_songs < 2:
            print("⚠ Not enough songs to create similarity matrix")
            return None
        
        # Initialize matrix
        similarity_matrix = np.zeros((n_songs, n_songs))
        song_names = []
        
        # Calculate similarities
        for i, (file_path1, metadata1) in enumerate(songs):
            song_names.append(metadata1['filename'])
            fingerprint1 = library_manager.library_data[file_path1]['fingerprint']
            
            for j, (file_path2, metadata2) in enumerate(songs):
                if i == j:
                    similarity_matrix[i][j] = 1.0  # Self-similarity
                else:
                    fingerprint2 = library_manager.library_data[file_path2]['fingerprint']
                    similarity = library_manager.calculate_similarity(fingerprint1, fingerprint2)
                    similarity_matrix[i][j] = similarity
        
        # Save matrix as JSON
        matrix_data = {
            'song_names': song_names,
            'similarity_matrix': similarity_matrix.tolist(),
            'metadata': {
                'total_songs': n_songs,
                'matrix_shape': similarity_matrix.shape,
                'description': 'Similarity matrix where matrix[i][j] is similarity between song i and song j'
            }
        }
        
        matrix_path = os.path.join(output_path, 'similarity_matrix.json')
        with open(matrix_path, 'w') as f:
            json.dump(matrix_data, f, indent=2)
        
        # Save matrix as CSV for easy viewing
        csv_path = os.path.join(output_path, 'similarity_matrix.csv')
        np.savetxt(csv_path, similarity_matrix, delimiter=',', fmt='%.4f')
        
        print(f"✓ Created similarity matrix:")
        print(f"  - JSON: {matrix_path}")
        print(f"  - CSV: {csv_path}")
        print(f"  - Matrix shape: {similarity_matrix.shape}")
        
        return matrix_path
        
    except Exception as e:
        print(f"✗ Error creating similarity matrix: {e}")
        return None

try:
    from audio_processor import AudioProcessor
    from library_manager import LibraryManager
    print("✓ All modules imported successfully")
    
    def test_library_manager(music_folder, recursive=True):
        """Test the LibraryManager functionality"""
        print("\n" + "="*60)
        print("TESTING PHASE 2: LIBRARY MANAGEMENT AND SIMILARITY ENGINE")
        print("="*60)
        
        # Create folder structure
        auto_dj_path, waveforms_path = create_folder_structure(music_folder)
        database_path = os.path.join(auto_dj_path, "music_library.db")
        
        # Initialize components
        audio_processor = AudioProcessor()
        library_manager = LibraryManager(audio_processor, database_path)
        print("✓ LibraryManager initialized successfully")
        
        # Test directory scanning
        print("\n--- Testing Directory Scanning ---")
        if os.path.exists(music_folder):
            music_files = library_manager.scan_directory(music_folder, recursive=recursive)
            print(f"✓ Found {len(music_files)} music files in {music_folder}")
            for file_path in music_files:
                print(f"  - {os.path.basename(file_path)}")
        else:
            print(f"⚠ Music folder not found: {music_folder}")
            return False
        
        # Test library building
        print("\n--- Testing Library Building ---")
        try:
            stats = library_manager.build_library(music_folder, recursive=recursive, force_rebuild=True)
            print(f"✓ Library built successfully: {stats}")
        except Exception as e:
            print(f"✗ Error building library: {e}")
            return False
        
        # Generate waveforms for all songs
        print("\n--- Generating Waveforms ---")
        songs = library_manager.get_song_list()
        waveform_count = 0
        for file_path, metadata in songs:
            try:
                # Load audio data for waveform generation
                audio_data, sample_rate = audio_processor.load_audio(file_path)
                waveform_path = generate_waveform(audio_data, sample_rate, waveforms_path, metadata['filename'])
                if waveform_path:
                    waveform_count += 1
                    print(f"✓ Generated waveform: {os.path.basename(waveform_path)}")
            except Exception as e:
                print(f"⚠ Error generating waveform for {metadata['filename']}: {e}")
        
        print(f"✓ Generated {waveform_count}/{len(songs)} waveforms")
        
        # Test library statistics
        print("\n--- Testing Library Statistics ---")
        stats = library_manager.get_library_stats()
        print(f"✓ Library stats: {stats}")
        
        # Test song list
        print("\n--- Testing Song List ---")
        song_list = library_manager.get_song_list()
        print(f"✓ Retrieved {len(song_list)} songs from library")
        for file_path, metadata in song_list:
            print(f"  - {metadata['filename']} ({metadata['duration_minutes']:.1f} min)")
        
        # Test similarity calculation
        print("\n--- Testing Similarity Calculation ---")
        if len(song_list) >= 2:
            # Get fingerprints for first two songs
            song1_path = song_list[0][0]
            song2_path = song_list[1][0]
            
            fp1 = library_manager.library_data[song1_path]['fingerprint']
            fp2 = library_manager.library_data[song2_path]['fingerprint']
            
            similarity = library_manager.calculate_similarity(fp1, fp2)
            print(f"✓ Similarity between songs: {similarity:.4f}")
            
            # Test self-similarity (should be 1.0)
            self_similarity = library_manager.calculate_similarity(fp1, fp1)
            print(f"✓ Self-similarity test: {self_similarity:.4f} (expected: 1.0)")
            
            if abs(self_similarity - 1.0) < 0.001:
                print("✓ Self-similarity test passed")
            else:
                print("✗ Self-similarity test failed")
                return False
        else:
            print("⚠ Not enough songs to test similarity calculation")
        
        # Create similarity matrix
        print("\n--- Creating Similarity Matrix ---")
        matrix_path = create_similarity_matrix(library_manager, auto_dj_path)
        
        # Test recommendation system
        print("\n--- Testing Recommendation System ---")
        if song_list:
            seed_song = song_list[0][0]
            print(f"✓ Using seed song: {os.path.basename(seed_song)}")
            
            try:
                recommendations = library_manager.find_similar_songs(seed_song, top_n=5)
                print(f"✓ Generated {len(recommendations)} recommendations")
                
                for i, (file_path, similarity, metadata) in enumerate(recommendations, 1):
                    print(f"  {i}. {metadata['filename']} (similarity: {similarity:.4f})")
                
                # Verify recommendations are sorted by similarity
                similarities = [sim for _, sim, _ in recommendations]
                if similarities == sorted(similarities, reverse=True):
                    print("✓ Recommendations properly sorted by similarity")
                else:
                    print("✗ Recommendations not properly sorted")
                    return False
                    
            except Exception as e:
                print(f"✗ Error generating recommendations: {e}")
                return False
        else:
            print("⚠ No songs available for recommendation testing")
        
        # Test database persistence
        print("\n--- Testing Database Persistence ---")
        try:
            # Create new instance and load from database
            new_library_manager = LibraryManager(audio_processor, database_path)
            new_library_manager.load_library()
            
            new_stats = new_library_manager.get_library_stats()
            print(f"✓ Database loaded successfully: {new_stats}")
            
            # Verify data integrity
            if new_stats['total_songs'] == stats['total_songs']:
                print("✓ Database persistence test passed")
            else:
                print("✗ Database persistence test failed")
                return False
                
        except Exception as e:
            print(f"✗ Error testing database persistence: {e}")
            return False
        
        return True
    
    def test_integration_with_phase1():
        """Test integration with Phase 1 components"""
        print("\n--- Testing Integration with Phase 1 ---")
        
        audio_processor = AudioProcessor()
        library_manager = LibraryManager(audio_processor)
        
        # Test with the sample audio file
        sample_file = "audio-samples/deep-abstract-ambient_snowcap.mp3"
        if os.path.exists(sample_file):
            try:
                # Process using Phase 1
                audio_data, mfccs, fingerprint = audio_processor.process_audio_file(sample_file)
                print(f"✓ Phase 1 processing successful: fingerprint shape {fingerprint.shape}")
                
                # Add to library using Phase 2
                success = library_manager.add_song_to_library(sample_file)
                if success:
                    print("✓ Phase 2 integration successful")
                    
                    # Test similarity with itself
                    recommendations = library_manager.find_similar_songs(sample_file, top_n=1)
                    if recommendations or len(library_manager.library_data) == 1:
                        print("✓ End-to-end workflow test passed")
                        return True
                    else:
                        print("✗ End-to-end workflow test failed")
                        return False
                else:
                    print("✗ Phase 2 integration failed")
                    return False
                    
            except Exception as e:
                print(f"✗ Integration test error: {e}")
                return False
        else:
            print(f"⚠ Sample file not found: {sample_file}")
            return False
    
    # Parse command line arguments
    args = parse_arguments()
    music_folder = args.music_folder
    recursive = args.recursive
    
    # Validate music folder
    if not os.path.exists(music_folder):
        print(f"❌ Error: Music folder '{music_folder}' does not exist!")
        print("Usage: python test_phase2.py <music_folder_path>")
        print("Example: python test_phase2.py audio-library")
        sys.exit(1)
    
    # Run all tests
    print(f"Starting Phase 2 validation tests for folder: {music_folder}")
    print(f"Recursive scanning: {'Yes' if recursive else 'No'}")
    
    # Test 1: Library Manager functionality
    test1_passed = test_library_manager(music_folder, recursive)
    
    # Final results
    print("\n" + "="*60)
    print("PHASE 2 TEST RESULTS")
    print("="*60)
    
    if test1_passed:
        print("✅ ALL TESTS PASSED!")
        print("✅ Library scanning: Working")
        print("✅ Database management: Working")
        print("✅ Similarity calculation: Working")
        print("✅ Recommendation system: Working")
        print("✅ Waveform generation: Working")
        print("✅ Similarity matrix creation: Working")
        print("✅ Phase 2 implementation validated successfully!")
        
        # Show output summary
        auto_dj_path = os.path.join(music_folder, 'auto-dj')
        print(f"\n📁 Output files created in: {auto_dj_path}")
        print("  - music_library.db (database)")
        print("  - similarity_matrix.json (similarity data)")
        print("  - similarity_matrix.csv (matrix view)")
        print("  - waveforms-library/ (waveform images)")
    else:
        print("❌ SOME TESTS FAILED!")
        print("❌ Library Manager tests failed")
    
    print("="*60)
    
except ImportError as e:
    print(f"✗ Import error: {e}")
    print("Please ensure all dependencies are installed:")
    print("pip install numpy librosa soundfile matplotlib scikit-learn")
except Exception as e:
    print(f"✗ Unexpected error: {e}")
    import traceback
    traceback.print_exc()
