"""
Test script for Phase 3 implementation: User Interface and Playlist Generation

This script validates the Phase 3 functionality:
- PlaylistGenerator class for playlist creation
- M3U playlist file generation
- User interface components
- Integration with Phase 1 and Phase 2
- End-to-end playlist generation workflow

Usage: python test_phase3.py <music_folder_path>
Example: python test_phase3.py audio-library
"""

import sys
import os
import json
import tempfile
from pathlib import Path
import argparse

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='Phase 3 Auto-DJ User Interface and Playlist Generation')
    parser.add_argument('music_folder', help='Path to the folder containing music files')
    parser.add_argument('--interactive', '-i', action='store_true',
                       help='Run interactive mode after tests')
    parser.add_argument('--playlist-length', '-l', type=int, default=10,
                       help='Number of songs in test playlists (default: 10)')
    return parser.parse_args()

def test_playlist_generator(music_folder):
    """Test the PlaylistGenerator class functionality"""
    print("\n" + "="*60)
    print("TESTING PHASE 3: PLAYLIST GENERATOR")
    print("="*60)
    
    try:
        from playlist_generator import PlaylistGenerator
        from library_manager import LibraryManager
        from audio_processor import AudioProcessor
        
        print("SUCCESS: All Phase 3 modules imported successfully")
        
        # Initialize components
        audio_processor = AudioProcessor()
        library_manager = LibraryManager(audio_processor)
        playlist_generator = PlaylistGenerator(library_manager, audio_processor)
        
        print("SUCCESS: PlaylistGenerator initialized successfully")
        
        # Test library loading
        print("\n--- Testing Library Loading ---")
        success = playlist_generator.load_library_from_path(music_folder)
        
        if not success:
            print("ERROR: Failed to load library")
            return False
        
        print("SUCCESS: Library loaded successfully")
        
        # Test library info
        print("\n--- Testing Library Information ---")
        library_info = playlist_generator.get_library_info()
        print(f"SUCCESS: Library info retrieved: {library_info['total_songs']} songs")
        
        # Test song list for selection
        print("\n--- Testing Song Selection List ---")
        songs = playlist_generator.get_song_list_for_selection()
        print(f"SUCCESS: Retrieved {len(songs)} songs for selection")
        
        if not songs:
            print("ERROR: No songs available for testing")
            return False
        
        # Display first few songs
        print("Sample songs:")
        for i, (song_num, filename, metadata) in enumerate(songs[:5], 1):
            print(f"  {song_num}. {filename} ({metadata['duration_minutes']:.1f} min)")
        
        return True
        
    except ImportError as e:
        print(f"ERROR: Import error: {e}")
        return False
    except Exception as e:
        print(f"ERROR: Error testing PlaylistGenerator: {e}")
        return False

def test_playlist_generation(music_folder, playlist_length=10):
    """Test playlist generation functionality"""
    print("\n--- Testing Playlist Generation ---")
    
    try:
        from playlist_generator import PlaylistGenerator
        
        # Initialize playlist generator
        playlist_generator = PlaylistGenerator()
        playlist_generator.load_library_from_path(music_folder)
        
        # Get songs for testing
        songs = playlist_generator.get_song_list_for_selection()
        if len(songs) < 2:
            print("ERROR: Not enough songs for playlist generation testing")
            return False
        
        # Test playlist generation with first song as seed
        seed_song_index = 1
        print(f"SUCCESS: Generating playlist with seed song: {songs[0][1]}")
        
        playlist = playlist_generator.generate_playlist(
            seed_song_index, playlist_length, exclude_seed=True
        )
        
        if not playlist:
            print("ERROR: No playlist generated")
            return False
        
        print(f"SUCCESS: Generated playlist with {len(playlist)} songs")
        
        # Display playlist preview
        print("Playlist preview:")
        for i, (file_path, similarity, metadata) in enumerate(playlist[:5], 1):
            print(f"  {i}. {metadata['filename']} (similarity: {similarity:.3f})")
        
        if len(playlist) > 5:
            print(f"  ... and {len(playlist) - 5} more songs")
        
        return playlist
        
    except Exception as e:
        print(f"ERROR: Error testing playlist generation: {e}")
        return False

def test_m3u_creation(playlist, music_folder):
    """Test M3U playlist file creation"""
    print("\n--- Testing M3U Playlist Creation ---")
    
    try:
        from playlist_generator import PlaylistGenerator
        
        # Initialize playlist generator
        playlist_generator = PlaylistGenerator()
        playlist_generator.load_library_from_path(music_folder)
        
        # Create output directory
        output_dir = os.path.join(music_folder, 'auto-dj', 'playlists')
        os.makedirs(output_dir, exist_ok=True)
        
        # Test M3U creation
        playlist_name = "test_playlist"
        result = playlist_generator.create_playlist_with_metadata(
            playlist, output_dir, playlist_name
        )
        
        print(f"SUCCESS: Created M3U playlist: {result['m3u_path']}")
        print(f"SUCCESS: Created metadata file: {result['metadata_path']}")
        
        # Verify M3U file exists and has content
        if os.path.exists(result['m3u_path']):
            with open(result['m3u_path'], 'r', encoding='utf-8') as f:
                m3u_content = f.read()
            
            if "#EXTM3U" in m3u_content and len(playlist) > 0:
                print("SUCCESS: M3U file format is correct")
            else:
                print("ERROR: M3U file format is incorrect")
                return False
        else:
            print("ERROR: M3U file was not created")
            return False
        
        # Verify metadata file exists and has content
        if os.path.exists(result['metadata_path']):
            with open(result['metadata_path'], 'r', encoding='utf-8') as f:
                metadata = json.load(f)
            
            if metadata['total_songs'] == len(playlist):
                print("SUCCESS: Metadata file is correct")
            else:
                print("ERROR: Metadata file is incorrect")
                return False
        else:
            print("ERROR: Metadata file was not created")
            return False
        
        # Test file validation
        print("\n--- Testing File Validation ---")
        validation = playlist_generator.validate_playlist_files(playlist)
        print(f"SUCCESS: File validation completed: {validation['valid_files']}/{validation['total_files']} files valid")
        
        return result
        
    except Exception as e:
        print(f"ERROR: Error testing M3U creation: {e}")
        return False

def test_user_interface_components():
    """Test user interface components"""
    print("\n--- Testing User Interface Components ---")
    
    try:
        from user_interface import AutoDJInterface
        
        # Initialize interface
        interface = AutoDJInterface()
        print("SUCCESS: AutoDJInterface initialized successfully")
        
        # Test interface methods exist
        methods_to_test = [
            'display_welcome',
            'get_library_path',
            'load_library',
            'display_library_info',
            'display_song_selection_menu',
            'get_playlist_length',
            'get_playlist_name',
            'display_playlist_preview',
            'save_playlist'
        ]
        
        for method_name in methods_to_test:
            if hasattr(interface, method_name):
                print(f"SUCCESS: Method {method_name} exists")
            else:
                print(f"ERROR: Method {method_name} missing")
                return False
        
        print("SUCCESS: All user interface components available")
        return True
        
    except Exception as e:
        print(f"ERROR: Error testing user interface: {e}")
        return False

def test_integration_with_phases_1_and_2(music_folder):
    """Test integration with Phase 1 and Phase 2"""
    print("\n--- Testing Integration with Phases 1 & 2 ---")
    
    try:
        from playlist_generator import PlaylistGenerator
        from library_manager import LibraryManager
        from audio_processor import AudioProcessor
        
        # Test end-to-end workflow
        print("SUCCESS: Testing end-to-end workflow...")
        
        # Initialize all components
        audio_processor = AudioProcessor()
        library_manager = LibraryManager(audio_processor)
        playlist_generator = PlaylistGenerator(library_manager, audio_processor)
        
        # Load library (Phase 2)
        success = playlist_generator.load_library_from_path(music_folder)
        if not success:
            print("ERROR: Failed to load library in integration test")
            return False
        
        print("SUCCESS: Phase 2 integration: Library loaded")
        
        # Generate playlist (Phase 3)
        songs = playlist_generator.get_song_list_for_selection()
        if not songs:
            print("ERROR: No songs available for integration test")
            return False
        
        playlist = playlist_generator.generate_playlist(1, 5, exclude_seed=True)
        if not playlist:
            print("ERROR: Failed to generate playlist in integration test")
            return False
        
        print("SUCCESS: Phase 3 integration: Playlist generated")
        
        # Test similarity scores are reasonable
        similarities = [sim for _, sim, _ in playlist]
        if all(0 <= sim <= 1 for sim in similarities):
            print("SUCCESS: Similarity scores are in valid range (0-1)")
        else:
            print("ERROR: Invalid similarity scores")
            return False
        
        print("SUCCESS: End-to-end integration test passed")
        return True
        
    except Exception as e:
        print(f"ERROR: Error in integration test: {e}")
        return False

def test_playlist_file_formats(music_folder):
    """Test different playlist file formats and validation"""
    print("\n--- Testing Playlist File Formats ---")
    
    try:
        from playlist_generator import PlaylistGenerator
        
        playlist_generator = PlaylistGenerator()
        playlist_generator.load_library_from_path(music_folder)
        
        # Generate a test playlist
        songs = playlist_generator.get_song_list_for_selection()
        if not songs:
            print("ERROR: No songs available for format testing")
            return False
        
        playlist = playlist_generator.generate_playlist(1, 5, exclude_seed=True)
        if not playlist:
            print("ERROR: Failed to generate test playlist")
            return False
        
        # Test M3U creation
        output_dir = os.path.join(music_folder, 'auto-dj', 'playlists')
        os.makedirs(output_dir, exist_ok=True)
        
        # Test different playlist names
        test_names = ["test_playlist", "my_music_mix", "similarity_test"]
        
        for name in test_names:
            result = playlist_generator.create_playlist_with_metadata(
                playlist, output_dir, name
            )
            
            if os.path.exists(result['m3u_path']) and os.path.exists(result['metadata_path']):
                print(f"SUCCESS: Created playlist: {name}")
            else:
                print(f"ERROR: Failed to create playlist: {name}")
                return False
        
        print("SUCCESS: All playlist file formats tested successfully")
        return True
        
    except Exception as e:
        print(f"ERROR: Error testing playlist formats: {e}")
        return False

def run_interactive_demo(music_folder):
    """Run interactive demo of the user interface"""
    print("\n" + "="*60)
    print("INTERACTIVE DEMO MODE")
    print("="*60)
    print("Starting interactive Auto-DJ interface...")
    print("You can now test the full user experience!")
    print("="*60)
    
    try:
        from user_interface import AutoDJInterface
        
        interface = AutoDJInterface()
        interface.run_interactive_session()
        
    except KeyboardInterrupt:
        print("\n\n👋 Demo ended by user")
    except Exception as e:
        print(f"ERROR: Error in interactive demo: {e}")

def main():
    """Main test function"""
    # Parse command line arguments
    args = parse_arguments()
    music_folder = args.music_folder
    interactive_mode = args.interactive
    playlist_length = args.playlist_length
    
    # Validate music folder
    if not os.path.exists(music_folder):
        print(f"ERROR: Error: Music folder '{music_folder}' does not exist!")
        print("Usage: python test_phase3.py <music_folder_path>")
        print("Example: python test_phase3.py audio-library")
        sys.exit(1)
    
    print(f"Starting Phase 3 validation tests for folder: {music_folder}")
    print(f"Test playlist length: {playlist_length} songs")
    
    # Run all tests
    test_results = []
    
    # Test 1: PlaylistGenerator basic functionality
    test1_passed = test_playlist_generator(music_folder)
    test_results.append(("PlaylistGenerator", test1_passed))
    
    if test1_passed:
        # Test 2: Playlist generation
        playlist = test_playlist_generation(music_folder, playlist_length)
        test2_passed = playlist is not False
        test_results.append(("Playlist Generation", test2_passed))
        
        if test2_passed:
            # Test 3: M3U creation
            m3u_result = test_m3u_creation(playlist, music_folder)
            test3_passed = m3u_result is not False
            test_results.append(("M3U Creation", test3_passed))
        
        # Test 4: User interface components
        test4_passed = test_user_interface_components()
        test_results.append(("User Interface", test4_passed))
        
        # Test 5: Integration with Phases 1 & 2
        test5_passed = test_integration_with_phases_1_and_2(music_folder)
        test_results.append(("Phase Integration", test5_passed))
        
        # Test 6: Playlist file formats
        test6_passed = test_playlist_file_formats(music_folder)
        test_results.append(("File Formats", test6_passed))
    
    # Display final results
    print("\n" + "="*60)
    print("PHASE 3 TEST RESULTS")
    print("="*60)
    
    all_passed = all(result for _, result in test_results)
    
    for test_name, passed in test_results:
        status = "SUCCESS: PASSED" if passed else "ERROR: FAILED"
        print(f"{status}: {test_name}")
    
    if all_passed:
        print("\n*** ALL TESTS PASSED! ***")
        print("SUCCESS: PlaylistGenerator: Working")
        print("SUCCESS: Playlist Generation: Working")
        print("SUCCESS: M3U Creation: Working")
        print("SUCCESS: User Interface: Working")
        print("SUCCESS: Phase Integration: Working")
        print("SUCCESS: File Formats: Working")
        print("SUCCESS: Phase 3 implementation validated successfully!")
        
        # Show output summary
        auto_dj_path = os.path.join(music_folder, 'auto-dj')
        playlists_path = os.path.join(auto_dj_path, 'playlists')
        print(f"\nOutput files created in: {playlists_path}")
        print("  - *.m3u (playlist files)")
        print("  - *_metadata.json (playlist metadata)")
        
        # Run interactive demo if requested
        if interactive_mode:
            run_interactive_demo(music_folder)
        
    else:
        print("\nERROR: SOME TESTS FAILED!")
        print("ERROR: Phase 3 implementation needs fixes")
    
    print("="*60)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user")
    except Exception as e:
        print(f"ERROR: Unexpected error: {e}")
        import traceback
        traceback.print_exc()
