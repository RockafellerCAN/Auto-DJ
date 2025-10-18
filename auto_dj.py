#!/usr/bin/env python3
"""
Auto-DJ: Simple Command-Line Interface

Usage: python auto_dj.py <music_library_path>

This script provides a clean, step-by-step interface for creating AI-powered playlists.
"""

import sys
import os
import argparse
from pathlib import Path

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.playlist_generator import PlaylistGenerator
from src.audio_processor import AudioProcessor

def print_header():
    """Print a clean header for the application."""
    print("\n" + "="*60)
    print("AUTO-DJ: AI-Powered Music Playlist Generator")
    print("="*60)
    print("Create intelligent playlists based on acoustic similarity")
    print("="*60)

def print_step(step_num, title):
    """Print a formatted step header."""
    print(f"\nSTEP {step_num}: {title}")
    print("-" * 40)

def get_user_choice(prompt, valid_choices):
    """Get user input with validation."""
    while True:
        try:
            choice = input(f"\n{prompt}: ").strip()
            if choice in valid_choices:
                return choice
            else:
                print(f"ERROR: Invalid choice. Please enter one of: {', '.join(valid_choices)}")
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            sys.exit(0)
        except EOFError:
            print("\n\nGoodbye!")
            sys.exit(0)

def get_number_input(prompt, min_val=1, max_val=100):
    """Get a number input with validation."""
    while True:
        try:
            choice = input(f"\n{prompt}: ").strip()
            num = int(choice)
            if min_val <= num <= max_val:
                return num
            else:
                print(f"ERROR: Please enter a number between {min_val} and {max_val}")
        except ValueError:
            print("ERROR: Please enter a valid number")
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            sys.exit(0)
        except EOFError:
            print("\n\nGoodbye!")
            sys.exit(0)

def display_songs(songs, max_display=10):
    """Display a list of songs in a clean format."""
    print(f"\nFound {len(songs)} songs in your library:")
    print("-" * 40)
    
    for i, (index, filename, metadata) in enumerate(songs[:max_display]):
        duration_min = int(metadata['duration_seconds']) // 60
        duration_sec = int(metadata['duration_seconds']) % 60
        print(f"  {index:2d}. {filename}")
        print(f"      Duration: {duration_min}:{duration_sec:02d}")
    
    if len(songs) > max_display:
        print(f"  ... and {len(songs) - max_display} more songs")

def main():
    """Main application function."""
    parser = argparse.ArgumentParser(
        description="Auto-DJ: AI-Powered Music Playlist Generator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python auto_dj.py audio-library
  python auto_dj.py "C:/Users/Username/Music"
  python auto_dj.py /home/user/music
        """
    )
    
    parser.add_argument(
        'music_path',
        help='Path to your music library folder'
    )
    
    parser.add_argument(
        '--playlist-length', '-l',
        type=int,
        default=10,
        help='Number of songs in the playlist (default: 10)'
    )
    
    parser.add_argument(
        '--playlist-name', '-n',
        default='my_playlist',
        help='Name for the playlist file (default: my_playlist)'
    )
    
    args = parser.parse_args()
    
    # Validate music path
    music_path = Path(args.music_path)
    if not music_path.exists():
        print(f"ERROR: Music library path does not exist: {music_path}")
        sys.exit(1)
    
    if not music_path.is_dir():
        print(f"ERROR: Path is not a directory: {music_path}")
        sys.exit(1)
    
    print_header()
    
    try:
        # Step 1: Load Library
        print_step(1, "Loading Music Library")
        print(f"Scanning: {music_path}")
        
        playlist_generator = PlaylistGenerator()
        success = playlist_generator.load_library_from_path(str(music_path))
        
        if not success:
            print("ERROR: Failed to load music library. Please check your path and try again.")
            sys.exit(1)
        
        print("SUCCESS: Library loaded successfully!")
        
        # Step 2: Show Library Info
        print_step(2, "Library Information")
        songs = playlist_generator.get_song_list_for_selection()
        display_songs(songs)
        
        # Step 3: Select Seed Song
        print_step(3, "Select Seed Song")
        print("Choose a song to base your playlist on:")
        
        valid_choices = [str(i) for i in range(1, len(songs) + 1)]
        seed_choice = get_user_choice(
            f"Enter song number (1-{len(songs)})",
            valid_choices
        )
        
        seed_index = int(seed_choice)  # Keep 1-based index for generate_playlist
        seed_song = songs[seed_index - 1]  # Convert to 0-based for list access
        
        print(f"\nSelected: {seed_song[1]}")
        
        # Step 4: Set Playlist Length
        print_step(4, "Playlist Settings")
        
        # Ask if user wants to customize settings
        customize = get_user_choice(
            "Customize playlist settings? (y/n)",
            ['y', 'n', 'yes', 'no']
        )
        
        if customize.lower() in ['y', 'yes']:
            playlist_length = get_number_input(
                f"How many songs in the playlist? (1-{len(songs)})",
                min_val=1,
                max_val=len(songs)
            )
            
            playlist_name = input("\nEnter playlist name: ").strip()
            if not playlist_name:
                playlist_name = 'my_playlist'
        else:
            playlist_length = args.playlist_length
            playlist_name = args.playlist_name
        
        print(f"\nPlaylist will contain {playlist_length} songs")
        print(f"Playlist name: {playlist_name}")
        
        # Step 5: Generate Playlist
        print_step(5, "Generating Playlist")
        print("Analyzing acoustic similarity...")
        
        playlist = playlist_generator.generate_playlist(
            seed_index, 
            playlist_length, 
            exclude_seed=True
        )
        
        if not playlist:
            print("ERROR: Failed to generate playlist. Please try again.")
            sys.exit(1)
        
        print(f"SUCCESS: Generated playlist with {len(playlist)} songs!")
        
        # Step 6: Preview Playlist
        print_step(6, "Playlist Preview")
        print("Your AI-generated playlist:")
        print("-" * 40)
        
        for i, (file_path, similarity, metadata) in enumerate(playlist, 1):
            filename = metadata['filename']
            duration_min = int(metadata['duration_seconds']) // 60
            duration_sec = int(metadata['duration_seconds']) % 60
            print(f"  {i:2d}. {filename}")
            print(f"      Similarity: {similarity:.3f} | Duration: {duration_min}:{duration_sec:02d}")
        
        # Step 7: Save Playlist
        print_step(7, "Save Playlist")
        
        save_choice = get_user_choice(
            "Save this playlist? (y/n)",
            ['y', 'n', 'yes', 'no']
        )
        
        if save_choice.lower() in ['y', 'yes']:
            print("Saving playlist files...")
            
            # Create playlist files directly in the music library folder
            result = playlist_generator.create_playlist_with_metadata(
                playlist, 
                str(music_path), 
                playlist_name
            )
            
            print(f"SUCCESS: Playlist saved successfully!")
            print(f"M3U file: {result['m3u_path']}")
            print(f"Metadata: {result['metadata_path']}")
            
            print(f"\nYour playlist is ready!")
            print(f"You can now open '{playlist_name}.m3u' in your music player")
        else:
            print("Playlist not saved. Goodbye!")
        
    except KeyboardInterrupt:
        print("\n\nGoodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\nERROR: An error occurred: {str(e)}")
        print("Please check your music library path and try again.")
        sys.exit(1)

if __name__ == "__main__":
    main()
