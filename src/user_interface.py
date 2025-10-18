"""
User Interface Module for Auto-DJ Phase 3

This module provides interactive user interfaces for playlist generation:
- Text-based menu system for song selection
- Interactive playlist generation workflow
- User-friendly prompts and validation
- Display of library information and recommendations
"""

import os
import sys
from typing import List, Dict, Tuple, Optional
import logging

from .playlist_generator import PlaylistGenerator
from .library_manager import LibraryManager
from .audio_processor import AudioProcessor

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AutoDJInterface:
    """
    Interactive user interface for Auto-DJ playlist generation.
    
    This class provides a text-based interface for:
    1. Loading music libraries
    2. Selecting seed songs
    3. Generating playlists
    4. Creating M3U files
    """
    
    def __init__(self):
        """Initialize the Auto-DJ interface."""
        self.playlist_generator = None
        self.current_library_info = None
        
    def display_welcome(self):
        """Display welcome message and instructions."""
        print("\n" + "="*60)
        print("AUTO-DJ: AI-Powered Music Playlist Generator")
        print("="*60)
        print("Phase 3: User Interface and Playlist Creation")
        print("\nThis tool will help you create intelligent playlists based on")
        print("acoustic similarity analysis of your music library.")
        print("\nFeatures:")
        print("- Load existing music libraries")
        print("- Select seed songs for playlist generation")
        print("- Generate M3U playlist files")
        print("- Create detailed playlist metadata")
        print("="*60)
    
    def get_library_path(self) -> str:
        """
        Get music library path from user.
        
        Returns:
            Path to the music library directory
        """
        while True:
            print("\nLIBRARY SELECTION")
            print("-" * 30)
            
            # Suggest common paths
            suggested_paths = [
                "audio-library",  # Default test library
                "C:\\Music",
                "C:\\Users\\Music",
                "/home/user/Music",
                "/Users/username/Music"
            ]
            
            print("Suggested library paths:")
            for i, path in enumerate(suggested_paths, 1):
                if os.path.exists(path):
                    print(f"  {i}. {path} SUCCESS:")
                else:
                    print(f"  {i}. {path}")
            
            print(f"  {len(suggested_paths) + 1}. Enter custom path")
            
            try:
                choice = input(f"\nSelect library path (1-{len(suggested_paths) + 1}): ").strip()
                
                if choice.isdigit():
                    choice_num = int(choice)
                    if 1 <= choice_num <= len(suggested_paths):
                        library_path = suggested_paths[choice_num - 1]
                    elif choice_num == len(suggested_paths) + 1:
                        library_path = input("Enter custom library path: ").strip()
                    else:
                        print("ERROR: Invalid choice. Please try again.")
                        continue
                else:
                    library_path = choice
                
                # Validate path
                if not os.path.exists(library_path):
                    print(f"ERROR: Path does not exist: {library_path}")
                    continue
                
                if not os.path.isdir(library_path):
                    print(f"ERROR: Path is not a directory: {library_path}")
                    continue
                
                return library_path
                
            except KeyboardInterrupt:
                print("\n\nGoodbye!")
                sys.exit(0)
            except Exception as e:
                print(f"ERROR: Error: {e}")
                continue
    
    def load_library(self, library_path: str) -> bool:
        """
        Load music library and display information.
        
        Args:
            library_path: Path to the music library
            
        Returns:
            True if library loaded successfully, False otherwise
        """
        print(f"\nLoading library from: {library_path}")
        
        try:
            # Initialize playlist generator
            self.playlist_generator = PlaylistGenerator()
            
            # Load library
            success = self.playlist_generator.load_library_from_path(library_path)
            
            if success:
                # Get library information
                self.current_library_info = self.playlist_generator.get_library_info()
                
                print("SUCCESS: Library loaded successfully!")
                self.display_library_info()
                return True
            else:
                print("ERROR: Failed to load library")
                return False
                
        except Exception as e:
            print(f"ERROR: Error loading library: {e}")
            return False
    
    def display_library_info(self):
        """Display information about the loaded library."""
        if not self.current_library_info:
            return
        
        info = self.current_library_info
        print(f"\nLIBRARY INFORMATION")
        print("-" * 30)
        print(f"Path: {info['library_path']}")
        print(f"Total Songs: {info['total_songs']}")
        print(f"Total Duration: {info['total_duration_hours']:.1f} hours")
        print(f"Average Song Length: {info['average_duration_minutes']:.1f} minutes")
        
        # Show first few songs as preview
        if info['songs']:
            print(f"\nSong Preview (showing first 5 songs):")
            for i, song in enumerate(info['songs'][:5], 1):
                print(f"  {i}. {song['filename']} ({song['duration_minutes']:.1f} min)")
            
            if len(info['songs']) > 5:
                print(f"  ... and {len(info['songs']) - 5} more songs")
    
    def display_song_selection_menu(self) -> Optional[int]:
        """
        Display song selection menu and get user choice.
        
        Returns:
            Selected song index (1-based) or None if cancelled
        """
        if not self.playlist_generator:
            print("ERROR: No library loaded")
            return None
        
        songs = self.playlist_generator.get_song_list_for_selection()
        
        if not songs:
            print("ERROR: No songs available in library")
            return None
        
        print(f"\nSONG SELECTION")
        print("-" * 30)
        print("Select a seed song for playlist generation:")
        print()
        
        # Display songs with pagination
        songs_per_page = 10
        total_pages = (len(songs) + songs_per_page - 1) // songs_per_page
        
        for page in range(total_pages):
            start_idx = page * songs_per_page
            end_idx = min(start_idx + songs_per_page, len(songs))
            
            print(f"Page {page + 1}/{total_pages}:")
            for i in range(start_idx, end_idx):
                song_num, filename, metadata = songs[i]
                duration = metadata['duration_minutes']
                print(f"  {song_num:2d}. {filename} ({duration:.1f} min)")
            
            if page < total_pages - 1:
                print("  ...")
                continue
        
        print(f"\nOptions:")
        print(f"  Enter song number (1-{len(songs)})")
        print(f"  'q' or 'quit' to exit")
        print(f"  'r' or 'refresh' to reload library")
        
        while True:
            try:
                choice = input(f"\nSelect song (1-{len(songs)}): ").strip().lower()
                
                if choice in ['q', 'quit']:
                    return None
                elif choice in ['r', 'refresh']:
                    return 'refresh'
                elif choice.isdigit():
                    song_num = int(choice)
                    if 1 <= song_num <= len(songs):
                        return song_num
                    else:
                        print(f"ERROR: Invalid song number. Please enter 1-{len(songs)}")
                else:
                    print("ERROR: Invalid input. Please enter a song number, 'q' to quit, or 'r' to refresh")
                    
            except KeyboardInterrupt:
                print("\n\nGoodbye!")
                sys.exit(0)
            except Exception as e:
                print(f"ERROR: Error: {e}")
    
    def get_playlist_length(self) -> int:
        """
        Get desired playlist length from user.
        
        Returns:
            Number of songs in the playlist
        """
        print(f"\nPLAYLIST LENGTH")
        print("-" * 30)
        print("How many songs would you like in your playlist?")
        print("Suggested lengths:")
        print("  - 10 songs (~30-40 minutes)")
        print("  - 20 songs (~60-80 minutes)")
        print("  - 30 songs (~90-120 minutes)")
        print("  - 50 songs (~150-200 minutes)")
        
        while True:
            try:
                choice = input("\nEnter playlist length (default: 20): ").strip()
                
                if not choice:
                    return 20
                
                length = int(choice)
                
                if length < 1:
                    print("ERROR: Playlist must have at least 1 song")
                    continue
                elif length > 100:
                    print("ERROR: Playlist length limited to 100 songs")
                    continue
                
                return length
                
            except ValueError:
                print("ERROR: Please enter a valid number")
            except KeyboardInterrupt:
                print("\n\nGoodbye!")
                sys.exit(0)
    
    def get_playlist_name(self) -> str:
        """
        Get playlist name from user.
        
        Returns:
            Name for the playlist
        """
        print(f"\nPLAYLIST NAME")
        print("-" * 30)
        print("Enter a name for your playlist:")
        print("(This will be used for the M3U file name)")
        
        while True:
            try:
                name = input("Playlist name (default: auto_dj_playlist): ").strip()
                
                if not name:
                    return "auto_dj_playlist"
                
                # Clean name for filename
                import re
                clean_name = re.sub(r'[^\w\-_\.]', '_', name)
                clean_name = clean_name.strip('_')
                
                if not clean_name:
                    print("ERROR: Invalid playlist name")
                    continue
                
                return clean_name
                
            except KeyboardInterrupt:
                print("\n\nGoodbye!")
                sys.exit(0)
    
    def display_playlist_preview(self, playlist: List[Tuple[str, float, Dict]], 
                               seed_song_name: str):
        """
        Display preview of the generated playlist.
        
        Args:
            playlist: Generated playlist
            seed_song_name: Name of the seed song
        """
        print(f"\nPLAYLIST PREVIEW")
        print("-" * 30)
        print(f"Seed song: {seed_song_name}")
        print(f"Generated playlist with {len(playlist)} songs:")
        print()
        
        total_duration = 0
        for i, (file_path, similarity, metadata) in enumerate(playlist, 1):
            duration = metadata['duration_minutes']
            total_duration += duration
            print(f"  {i:2d}. {metadata['filename']} ({duration:.1f} min) [similarity: {similarity:.3f}]")
        
        print(f"\nTotal duration: {total_duration:.1f} minutes ({total_duration/60:.1f} hours)")
    
    def save_playlist(self, playlist: List[Tuple[str, float, Dict]], 
                     playlist_name: str) -> bool:
        """
        Save playlist to M3U and metadata files.
        
        Args:
            playlist: Generated playlist
            playlist_name: Name for the playlist files
            
        Returns:
            True if saved successfully, False otherwise
        """
        print(f"\nSAVING PLAYLIST")
        print("-" * 30)
        
        try:
            # Determine output directory
            if self.current_library_info and self.current_library_info['library_path']:
                output_dir = os.path.join(self.current_library_info['library_path'], 'auto-dj', 'playlists')
            else:
                output_dir = "playlists"
            
            # Create playlist files
            result = self.playlist_generator.create_playlist_with_metadata(
                playlist, output_dir, playlist_name
            )
            
            print("SUCCESS: Playlist saved successfully!")
            print(f"M3U file: {result['m3u_path']}")
            print(f"Metadata: {result['metadata_path']}")
            
            # Validate files
            validation = self.playlist_generator.validate_playlist_files(playlist)
            if validation['all_files_valid']:
                print("SUCCESS: All playlist files are valid and accessible")
            else:
                print(f"Warning: {validation['invalid_files']} files may not be accessible")
            
            return True
            
        except Exception as e:
            print(f"ERROR: Error saving playlist: {e}")
            return False
    
    def run_interactive_session(self):
        """Run the main interactive session."""
        self.display_welcome()
        
        while True:
            try:
                # Get library path
                library_path = self.get_library_path()
                
                # Load library
                if not self.load_library(library_path):
                    print("ERROR: Failed to load library. Please try again.")
                    continue
                
                # Main playlist generation loop
                while True:
                    # Select seed song
                    song_choice = self.display_song_selection_menu()
                    
                    if song_choice is None:
                        print("\n👋 Goodbye!")
                        return
                    elif song_choice == 'refresh':
                        if not self.load_library(library_path):
                            print("ERROR: Failed to reload library")
                            break
                        continue
                    
                    # Get playlist length
                    playlist_length = self.get_playlist_length()
                    
                    # Generate playlist
                    print(f"\nGenerating playlist...")
                    try:
                        playlist = self.playlist_generator.generate_playlist(
                            song_choice, playlist_length, exclude_seed=True
                        )
                        
                        if not playlist:
                            print("ERROR: No similar songs found")
                            continue
                        
                        # Get seed song name for display
                        songs = self.playlist_generator.get_song_list_for_selection()
                        seed_song_name = songs[song_choice - 1][1]
                        
                        # Display preview
                        self.display_playlist_preview(playlist, seed_song_name)
                        
                        # Ask if user wants to save
                        save_choice = input("\nSave this playlist? (y/n): ").strip().lower()
                        if save_choice in ['y', 'yes']:
                            playlist_name = self.get_playlist_name()
                            if self.save_playlist(playlist, playlist_name):
                                print("SUCCESS: Playlist saved successfully!")
                            else:
                                print("ERROR: Failed to save playlist")
                        
                        # Ask if user wants to create another playlist
                        another_choice = input("\nCreate another playlist? (y/n): ").strip().lower()
                        if another_choice not in ['y', 'yes']:
                            break
                        
                    except Exception as e:
                        print(f"ERROR: Error generating playlist: {e}")
                        continue
                
                # Ask if user wants to load a different library
                new_library_choice = input("\nLoad a different library? (y/n): ").strip().lower()
                if new_library_choice not in ['y', 'yes']:
                    break
                
            except KeyboardInterrupt:
                print("\n\nGoodbye!")
                break
            except Exception as e:
                print(f"ERROR: Unexpected error: {e}")
                continue
        
        print("\nThank you for using Auto-DJ!")


def main():
    """Main entry point for the Auto-DJ interface."""
    interface = AutoDJInterface()
    interface.run_interactive_session()


if __name__ == "__main__":
    main()
