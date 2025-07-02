#!/usr/bin/env python3
"""
Dynamic Portrait Slideshow Application with Image Standardization
Continuously loops portrait images from left to right with smooth transitions
Features real-time folder synchronization, configurable animation parameters,
and automatic image resizing to standardized dimensions (3024x4032) with vertical orientation enforcement
"""

import tkinter as tk
from tkinter import messagebox
import os
import time
import threading
from PIL import Image, ImageTk, ImageOps
import glob
from pathlib import Path
import hashlib

class PortraitSlideshow:
    def __init__(self):
        # Configuration parameters - modify these to adjust behavior
        self.WINDOW_WIDTH = 1366
        self.WINDOW_HEIGHT = 768
        self.BACKGROUND_PATH = "/home/graahand/Documents/background.jpg"
        self.SLIDESHOW_FOLDER = "/home/graahand/Documents/slideshow"
        self.PROCESSED_CACHE_FOLDER = "slideshow_cache"  # Cache for processed images
        
        # Image standardization parameters
        self.TARGET_WIDTH = 3024   # Target image width (pixels)
        self.TARGET_HEIGHT = 4032  # Target image height (pixels)
        self.FORCE_VERTICAL = True # Enforce vertical orientation
        
        # Animation parameters
        self.ANIMATION_SPEED = 2  # pixels per frame (higher = faster movement)
        self.FRAME_DELAY = 16     # milliseconds between frames (60 FPS ≈ 16ms)
        self.IMAGE_SPACING = 180  # pixels between consecutive images
        self.PORTRAIT_HEIGHT = 400  # standardized portrait height for display
        self.VERTICAL_OFFSET = 100  # pixels below center (1-2cm equivalent)
        
        # Folder monitoring parameters
        self.FOLDER_CHECK_INTERVAL = 2.0  # seconds between folder scans
        
        # Initialize application state
        self.root = None
        self.canvas = None
        self.background_image = None
        self.image_objects = []
        self.image_paths = []
        self.processed_images_cache = {}  # Cache for processed PIL Images
        self.animation_running = False
        self.folder_monitor_thread = None
        self.stop_monitoring = False
        
        # Fullscreen state management
        self.is_fullscreen = False
        self.windowed_geometry = None
        self.current_screen_width = self.WINDOW_WIDTH
        self.current_screen_height = self.WINDOW_HEIGHT
        
        self.setup_directories()
        self.setup_window()
        self.load_background()
        self.initialize_slideshow()
        
    def setup_directories(self):
        """Create necessary directories for slideshow and cache"""
        os.makedirs(self.SLIDESHOW_FOLDER, exist_ok=True)
        os.makedirs(self.PROCESSED_CACHE_FOLDER, exist_ok=True)
        
    def setup_window(self):
        """Initialize the main window with specified dimensions and properties"""
        self.root = tk.Tk()
        self.root.title("Dynamic Portrait Slideshow - Enhanced")
        self.root.geometry(f"{self.WINDOW_WIDTH}x{self.WINDOW_HEIGHT}")
        self.root.resizable(False, False)
        
        # Initialize fullscreen state tracking
        self.is_fullscreen = False
        self.windowed_geometry = f"{self.WINDOW_WIDTH}x{self.WINDOW_HEIGHT}"
        
        # Center window on screen
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - self.WINDOW_WIDTH) // 2
        y = (screen_height - self.WINDOW_HEIGHT) // 2
        self.root.geometry(f"{self.WINDOW_WIDTH}x{self.WINDOW_HEIGHT}+{x}+{y}")
        
        # Create canvas for drawing
        self.canvas = tk.Canvas(
            self.root, 
            width=self.WINDOW_WIDTH, 
            height=self.WINDOW_HEIGHT,
            highlightthickness=0
        )
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Bind window close event
        self.root.protocol("WM_DELETE_WINDOW", self.cleanup_and_exit)
        
        # Bind F11 key for fullscreen toggle
        self.root.bind("<F11>", self.toggle_fullscreen)
        self.root.bind("<Escape>", self.exit_fullscreen)
        
        # Ensure window can receive focus for key events
        self.root.focus_set()
        
    def load_background(self):
        """Load and display the background image"""
        try:
            if os.path.exists(self.BACKGROUND_PATH):
                bg_image = Image.open(self.BACKGROUND_PATH)
                bg_image = bg_image.resize((self.WINDOW_WIDTH, self.WINDOW_HEIGHT), Image.Resampling.LANCZOS)
                self.background_image = ImageTk.PhotoImage(bg_image)
                self.canvas.create_image(0, 0, anchor=tk.NW, image=self.background_image)
            else:
                # Create solid color background if image not found
                self.canvas.configure(bg='#2c3e50')
                print(f"Background image not found at: {self.BACKGROUND_PATH}")
                print("Using solid color background instead")
        except Exception as e:
            print(f"Error loading background: {e}")
            self.canvas.configure(bg='#2c3e50')
            
    def cleanup_and_exit(self):
        """Clean up resources and exit application"""
        self.animation_running = False
        self.stop_monitoring = False
        
        # Clear image caches
        self.processed_images_cache.clear()
        
        # Wait for monitoring thread to finish
        if self.folder_monitor_thread and self.folder_monitor_thread.is_alive():
            self.folder_monitor_thread.join(timeout=1.0)
            
        self.root.destroy()
        
    def get_image_hash(self, image_path):
        """Generate unique hash for image file based on path and modification time"""
        try:
            stat = os.stat(image_path)
            hash_input = f"{image_path}_{stat.st_mtime}_{stat.st_size}"
            return hashlib.md5(hash_input.encode()).hexdigest()
        except Exception:
            return None
            
    def get_cached_image_path(self, image_hash):
        """Get path for cached processed image"""
        return os.path.join(self.PROCESSED_CACHE_FOLDER, f"{image_hash}.jpg")
        
    def is_image_vertical(self, image):
        """Check if image has vertical orientation (height > width)"""
        width, height = image.size
        return height > width
        
    def enforce_vertical_orientation(self, image):
        """Rotate image to ensure vertical orientation if needed"""
        if not self.is_image_vertical(image):
            print("  Converting horizontal image to vertical orientation")
            # Rotate 90 degrees counter-clockwise to make it vertical
            image = image.rotate(90, expand=True)
        return image
        
    def resize_image_to_target(self, image):
        """
        Resize image to exact target dimensions (3024x4032) using intelligent scaling
        
        Algorithm:
        1. Calculate aspect ratios for source and target
        2. Determine optimal scaling method (crop vs pad)
        3. Apply high-quality resampling with LANCZOS filter
        4. Center the result within target dimensions
        """
        source_width, source_height = image.size
        target_width, target_height = self.TARGET_WIDTH, self.TARGET_HEIGHT
        
        # Calculate aspect ratios
        source_aspect = source_width / source_height
        target_aspect = target_width / target_height
        
        print(f"  Source: {source_width}x{source_height} (aspect: {source_aspect:.3f})")
        print(f"  Target: {target_width}x{target_height} (aspect: {target_aspect:.3f})")
        
        if source_aspect > target_aspect:
            # Source is wider relative to height - fit by height and crop width
            scale_factor = target_height / source_height
            new_width = int(source_width * scale_factor)
            new_height = target_height
            
            # Resize with high-quality resampling
            resized = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # Center crop to target width
            left = (new_width - target_width) // 2
            right = left + target_width
            final_image = resized.crop((left, 0, right, target_height))
            
            print(f"  Applied height-fit scaling (factor: {scale_factor:.3f}) with center crop")
            
        else:
            # Source is taller relative to width - fit by width and crop height
            scale_factor = target_width / source_width
            new_width = target_width
            new_height = int(source_height * scale_factor)
            
            # Resize with high-quality resampling
            resized = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # Center crop to target height
            top = (new_height - target_height) // 2
            bottom = top + target_height
            final_image = resized.crop((0, top, target_width, bottom))
            
            print(f"  Applied width-fit scaling (factor: {scale_factor:.3f}) with center crop")
        
        return final_image
        
    def process_image_to_standard(self, image_path):
        """
        Process image to standardized format: 3024x4032 vertical orientation
        
        Processing pipeline:
        1. Load original image with EXIF orientation correction
        2. Enforce vertical orientation (rotate if needed)
        3. Resize to exact target dimensions using intelligent scaling
        4. Cache processed result for performance optimization
        """
        print(f"Processing image: {os.path.basename(image_path)}")
        
        try:
            # Generate cache hash for this image
            image_hash = self.get_image_hash(image_path)
            if not image_hash:
                raise Exception("Could not generate image hash")
                
            cached_path = self.get_cached_image_path(image_hash)
            
            # Check if processed version exists in cache
            if os.path.exists(cached_path):
                print("  Loading from cache")
                return Image.open(cached_path)
            
            # Load original image with EXIF orientation correction
            print("  Loading and processing original image")
            original_image = Image.open(image_path)
            
            # Apply EXIF orientation correction
            corrected_image = ImageOps.exif_transpose(original_image)
            
            # Enforce vertical orientation if required
            if self.FORCE_VERTICAL:
                corrected_image = self.enforce_vertical_orientation(corrected_image)
            
            # Resize to target dimensions
            processed_image = self.resize_image_to_target(corrected_image)
            
            # Verify final dimensions
            final_width, final_height = processed_image.size
            if final_width != self.TARGET_WIDTH or final_height != self.TARGET_HEIGHT:
                raise Exception(f"Failed to achieve target dimensions: got {final_width}x{final_height}")
            
            print(f"  Successfully processed to {final_width}x{final_height}")
            
            # Cache the processed image
            try:
                processed_image.save(cached_path, "JPEG", quality=95, optimize=True)
                print("  Cached processed image")
            except Exception as cache_error:
                print(f"  Warning: Could not cache image: {cache_error}")
            
            return processed_image
            
        except Exception as e:
            print(f"  Error processing image {image_path}: {e}")
            return None
            
    def scan_slideshow_folder(self):
        """Scan the slideshow folder and return list of valid image paths"""
        if not os.path.exists(self.SLIDESHOW_FOLDER):
            return []
            
        # Supported image formats with case variations
        image_extensions = ['*.jpg', '*.jpeg', '*.png', '*.bmp', '*.gif', '*.tiff',
                           '*.JPG', '*.JPEG', '*.PNG', '*.BMP', '*.GIF', '*.TIFF']
        
        # Use set to eliminate duplicates on case-insensitive filesystems
        image_files_set = set()
        
        for extension in image_extensions:
            pattern = os.path.join(self.SLIDESHOW_FOLDER, extension)
            matched_files = glob.glob(pattern, recursive=False)
            
            # Convert to absolute paths for reliable deduplication
            for file_path in matched_files:
                absolute_path = os.path.abspath(file_path)
                image_files_set.add(absolute_path)
            
        # Convert set back to sorted list for consistent ordering
        return sorted(list(image_files_set))
        
    def load_portrait_image(self, image_path):
        """
        Load and prepare portrait image for display
        
        Process:
        1. Check memory cache for processed image
        2. If not cached, process image to standard format
        3. Resize processed image for display (maintaining aspect ratio)
        4. Convert to Tkinter-compatible PhotoImage
        """
        try:
            # Check if we have this image cached in memory
            if image_path in self.processed_images_cache:
                processed_image = self.processed_images_cache[image_path]
            else:
                # Process image to standard format
                processed_image = self.process_image_to_standard(image_path)
                if processed_image is None:
                    return None
                    
                # Cache in memory for faster subsequent access
                self.processed_images_cache[image_path] = processed_image
            
            # Resize processed image for display
            # The processed image is already standardized to 3024x4032
            display_aspect_ratio = processed_image.width / processed_image.height
            display_width = int(self.PORTRAIT_HEIGHT * display_aspect_ratio)
            display_height = self.PORTRAIT_HEIGHT
            
            # Resize with high-quality resampling for display
            display_image = processed_image.resize(
                (display_width, display_height), 
                Image.Resampling.LANCZOS
            )
            
            return ImageTk.PhotoImage(display_image)
            
        except Exception as e:
            print(f"Error loading image {image_path}: {e}")
            return None
            
    def initialize_slideshow(self):
        """Initialize the slideshow with current images in folder"""
        self.image_paths = self.scan_slideshow_folder()
        
        if not self.image_paths:
            messagebox.showwarning("No Images", f"No images found in '{self.SLIDESHOW_FOLDER}' folder")
            return
            
        print(f"Found {len(self.image_paths)} images in slideshow folder")
        print("Pre-processing images to standard format...")
        
        # Pre-process all images to build cache
        processed_count = 0
        for image_path in self.image_paths:
            processed_image = self.process_image_to_standard(image_path)
            if processed_image is not None:
                self.processed_images_cache[image_path] = processed_image
                processed_count += 1
                
        print(f"Successfully processed {processed_count}/{len(self.image_paths)} images")
        
        # Start folder monitoring in separate thread
        self.start_folder_monitoring()
        
        # Start animation
        self.start_animation()
        
    def start_folder_monitoring(self):
        """Start monitoring the slideshow folder for changes"""
        self.stop_monitoring = False
        self.folder_monitor_thread = threading.Thread(target=self._monitor_folder, daemon=True)
        self.folder_monitor_thread.start()
        
    def _monitor_folder(self):
        """Monitor folder for new images (runs in separate thread)"""
        while not self.stop_monitoring:
            try:
                current_images = self.scan_slideshow_folder()
                
                # Check if folder contents changed
                if current_images != self.image_paths:
                    print(f"Folder change detected: {len(current_images)} images")
                    
                    # Clear cache for removed images
                    removed_images = set(self.image_paths) - set(current_images)
                    for removed_image in removed_images:
                        if removed_image in self.processed_images_cache:
                            del self.processed_images_cache[removed_image]
                    
                    # Update image list
                    self.image_paths = current_images
                    
                    # Pre-process new images
                    new_images = set(current_images) - set(self.processed_images_cache.keys())
                    for new_image in new_images:
                        processed_image = self.process_image_to_standard(new_image)
                        if processed_image is not None:
                            self.processed_images_cache[new_image] = processed_image
                    
                time.sleep(self.FOLDER_CHECK_INTERVAL)
                
            except Exception as e:
                print(f"Error monitoring folder: {e}")
                time.sleep(self.FOLDER_CHECK_INTERVAL)
                
    def start_animation(self):
        """Start the continuous animation loop"""
        if not self.image_paths:
            return
            
        self.animation_running = True
        self.current_image_index = 0
        self.next_image_spawn_x = 0
        
        # Schedule first animation frame
        self.root.after(self.FRAME_DELAY, self.animate_frame)
        
    def animate_frame(self):
        """Execute single animation frame"""
        if not self.animation_running or not self.image_paths:
            return
            
        # Clean up images that have moved off screen
        self.cleanup_offscreen_images()
        
        # Spawn new image if needed
        if self.should_spawn_new_image():
            self.spawn_new_image()
            
        # Update positions of all active images
        self.update_image_positions()
        
        # Schedule next frame
        self.root.after(self.FRAME_DELAY, self.animate_frame)
        
    def should_spawn_new_image(self):
        """Determine if a new image should be spawned"""
        if not self.image_objects:
            return True
            
        # Check if last spawned image has moved far enough
        last_image = self.image_objects[-1]
        return last_image['x'] >= self.IMAGE_SPACING
        
    def spawn_new_image(self):
        """Spawn a new image at the left edge of screen"""
        if not self.image_paths:
            return
            
        # Get next image path
        image_path = self.image_paths[self.current_image_index]
        self.current_image_index = (self.current_image_index + 1) % len(self.image_paths)
        
        # Load image (already processed to standard format)
        photo_image = self.load_portrait_image(image_path)
        if photo_image is None:
            return
            
        # Calculate spawn position (adapt to current screen dimensions)
        spawn_x = -photo_image.width()  # Start completely off-screen left
        spawn_y = (self.current_screen_height // 2) + self.VERTICAL_OFFSET
        
        # Create canvas image object
        canvas_id = self.canvas.create_image(spawn_x, spawn_y, anchor=tk.CENTER, image=photo_image)
        
        # Store image object data
        image_obj = {
            'canvas_id': canvas_id,
            'photo_image': photo_image,  # Keep reference to prevent garbage collection
            'x': spawn_x,
            'y': spawn_y,
            'width': photo_image.width(),
            'height': photo_image.height()
        }
        
        self.image_objects.append(image_obj)
        
    def update_image_positions(self):
        """Update positions of all active images"""
        for image_obj in self.image_objects:
            # Move image to the right
            image_obj['x'] += self.ANIMATION_SPEED
            
            # Update canvas position
            self.canvas.coords(image_obj['canvas_id'], image_obj['x'], image_obj['y'])
            
    def cleanup_offscreen_images(self):
        """Remove images that have moved completely off the right edge"""
        images_to_remove = []
        
        for i, image_obj in enumerate(self.image_objects):
            # Check if image is completely off-screen to the right (adapt to current screen width)
            if image_obj['x'] - (image_obj['width'] // 2) > self.current_screen_width:
                images_to_remove.append(i)
                
        # Remove images in reverse order to maintain indices
        for i in reversed(images_to_remove):
            image_obj = self.image_objects[i]
            self.canvas.delete(image_obj['canvas_id'])
            del self.image_objects[i]
            
    def toggle_fullscreen(self, event=None):
        """
        Toggle between fullscreen and windowed mode
        
        Fullscreen Implementation:
        - Captures current window geometry before entering fullscreen
        - Adapts canvas dimensions to actual screen resolution
        - Updates animation parameters for proper scaling
        - Maintains aspect ratios and positioning logic
        """
        self.is_fullscreen = not self.is_fullscreen
        
        if self.is_fullscreen:
            # Store current windowed geometry
            self.windowed_geometry = self.root.geometry()
            
            # Get actual screen dimensions
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            
            # Update current dimensions for animation calculations
            self.current_screen_width = screen_width
            self.current_screen_height = screen_height
            
            # Enter fullscreen mode
            self.root.attributes('-fullscreen', True)
            self.root.configure(cursor='none')  # Hide cursor in fullscreen
            
            # Reconfigure canvas for fullscreen dimensions
            self.canvas.configure(width=screen_width, height=screen_height)
            
            # Reload background for new dimensions
            self.load_background_for_current_size()
            
            print(f"Entered fullscreen mode: {screen_width}x{screen_height}")
            
        else:
            # Exit fullscreen mode
            self.root.attributes('-fullscreen', False)
            self.root.configure(cursor='')  # Restore cursor
            
            # Restore windowed geometry
            if self.windowed_geometry:
                self.root.geometry(self.windowed_geometry)
            
            # Reset dimensions to windowed values
            self.current_screen_width = self.WINDOW_WIDTH
            self.current_screen_height = self.WINDOW_HEIGHT
            
            # Reconfigure canvas for windowed dimensions
            self.canvas.configure(width=self.WINDOW_WIDTH, height=self.WINDOW_HEIGHT)
            
            # Reload background for windowed dimensions
            self.load_background_for_current_size()
            
            print(f"Exited fullscreen mode: {self.WINDOW_WIDTH}x{self.WINDOW_HEIGHT}")
    
    def exit_fullscreen(self, event=None):
        """Exit fullscreen mode when Escape key is pressed"""
        if self.is_fullscreen:
            self.toggle_fullscreen()
    
    def load_background_for_current_size(self):
        """Load and scale background image for current screen dimensions"""
        try:
            # Clear existing background
            self.canvas.delete("background")
            
            if os.path.exists(self.BACKGROUND_PATH):
                bg_image = Image.open(self.BACKGROUND_PATH)
                bg_image = bg_image.resize(
                    (self.current_screen_width, self.current_screen_height), 
                    Image.Resampling.LANCZOS
                )
                self.background_image = ImageTk.PhotoImage(bg_image)
                self.canvas.create_image(
                    0, 0, 
                    anchor=tk.NW, 
                    image=self.background_image, 
                    tags="background"
                )
            else:
                # Set background color for current canvas size
                self.canvas.configure(bg='#2c3e50')
                
        except Exception as e:
            print(f"Error loading background for current size: {e}")
            self.canvas.configure(bg='#2c3e50')


        # """Clean up resources and exit application"""
        # self.animation_running = False
        # self.stop_monitoring = True
        
        # # Clear image caches
        # self.processed_images_cache.clear()
        
        # # Wait for monitoring thread to finish
        # if self.folder_monitor_thread and self.folder_monitor_thread.is_alive():
        #     self.folder_monitor_thread.join(timeout=1.0)
            
        # self.root.destroy()
        
    def run(self):
        """Start the application main loop"""
        try:
            print("Starting Enhanced Dynamic Portrait Slideshow...")
            print(f"Window Resolution: {self.WINDOW_WIDTH}x{self.WINDOW_HEIGHT}")
            print(f"Target Image Dimensions: {self.TARGET_WIDTH}x{self.TARGET_HEIGHT}")
            print(f"Vertical Orientation Enforcement: {self.FORCE_VERTICAL}")
            print(f"Animation Speed: {self.ANIMATION_SPEED} pixels/frame")
            print(f"Frame Rate: {1000//self.FRAME_DELAY} FPS")
            print(f"Image Spacing: {self.IMAGE_SPACING} pixels")
            print(f"Slideshow Folder: {os.path.abspath(self.SLIDESHOW_FOLDER)}")
            print(f"Cache Folder: {os.path.abspath(self.PROCESSED_CACHE_FOLDER)}")
            print("Press Ctrl+C or close window to exit")
            
            self.root.mainloop()
            
        except KeyboardInterrupt:
            print("\nApplication terminated by user")
            self.cleanup_and_exit()
        except Exception as e:
            print(f"Application error: {e}")
            self.cleanup_and_exit()

def main():
    """Main entry point"""
    try:
        # Initialize and run application
        app = PortraitSlideshow()
        app.run()
        
    except Exception as e:
        print(f"Failed to start application: {e}")
        return 1
        
    return 0

if __name__ == "__main__":
    exit(main())