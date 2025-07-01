#!/usr/bin/env python3
"""
Dynamic Portrait Slideshow Application
Continuously loops portrait images from left to right with smooth transitions
Features real-time folder synchronization and configurable animation parameters
"""

import tkinter as tk
from tkinter import messagebox
import os
import time
import threading
from PIL import Image, ImageTk
import glob
from pathlib import Path

class PortraitSlideshow:
    def __init__(self):
        # Configuration parameters - modify these to adjust behavior
        self.WINDOW_WIDTH = 1366
        self.WINDOW_HEIGHT = 768
        self.BACKGROUND_PATH = "/home/graahand/Documents/background_slide.jpg"
        self.SLIDESHOW_FOLDER = "slideshow"
        
        # Animation parameters
        self.ANIMATION_SPEED = 2  # pixels per frame (higher = faster movement)
        self.FRAME_DELAY = 16     # milliseconds between frames (60 FPS ≈ 16ms)
        self.IMAGE_SPACING = 400  # pixels between consecutive images
        self.PORTRAIT_HEIGHT = 400  # standardized portrait height
        self.VERTICAL_OFFSET = 100  # pixels below center (1-2cm equivalent)
        
        # Folder monitoring parameters
        self.FOLDER_CHECK_INTERVAL = 2.0  # seconds between folder scans
        
        # Initialize application state
        self.root = None
        self.canvas = None
        self.background_image = None
        self.image_objects = []
        self.image_paths = []
        self.animation_running = False
        self.folder_monitor_thread = None
        self.stop_monitoring = False
        
        self.setup_window()
        self.load_background()
        self.initialize_slideshow()
        
    def setup_window(self):
        """Initialize the main window with specified dimensions and properties"""
        self.root = tk.Tk()
        self.root.title("Dynamic Portrait Slideshow")
        self.root.geometry(f"{self.WINDOW_WIDTH}x{self.WINDOW_HEIGHT}")
        self.root.resizable(False, False)
        
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
        self.canvas.pack()
        
        # Bind window close event
        self.root.protocol("WM_DELETE_WINDOW", self.cleanup_and_exit)
        
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
        """Load and resize a portrait image maintaining aspect ratio"""
        try:
            image = Image.open(image_path)
            
            # Calculate dimensions maintaining aspect ratio
            original_width, original_height = image.size
            aspect_ratio = original_width / original_height
            
            # Resize based on target height
            new_width = int(self.PORTRAIT_HEIGHT * aspect_ratio)
            new_height = self.PORTRAIT_HEIGHT
            
            # Resize image with high-quality resampling
            resized_image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            return ImageTk.PhotoImage(resized_image)
            
        except Exception as e:
            print(f"Error loading image {image_path}: {e}")
            return None
            
    def initialize_slideshow(self):
        """Initialize the slideshow with current images in folder"""
        self.image_paths = self.scan_slideshow_folder()
        
        if not self.image_paths:
            messagebox.showwarning("No Images", f"No images found in '{self.SLIDESHOW_FOLDER}' folder")
            return
            
        print(f"Loaded {len(self.image_paths)} images from slideshow folder")
        
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
                    self.image_paths = current_images
                    
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
        
        # Load image
        photo_image = self.load_portrait_image(image_path)
        if photo_image is None:
            return
            
        # Calculate spawn position
        spawn_x = -photo_image.width()  # Start completely off-screen left
        spawn_y = (self.WINDOW_HEIGHT // 2) + self.VERTICAL_OFFSET
        
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
            # Check if image is completely off-screen to the right
            if image_obj['x'] - (image_obj['width'] // 2) > self.WINDOW_WIDTH:
                images_to_remove.append(i)
                
        # Remove images in reverse order to maintain indices
        for i in reversed(images_to_remove):
            image_obj = self.image_objects[i]
            self.canvas.delete(image_obj['canvas_id'])
            del self.image_objects[i]
            
    def cleanup_and_exit(self):
        """Clean up resources and exit application"""
        self.animation_running = False
        self.stop_monitoring = True
        
        # Wait for monitoring thread to finish
        if self.folder_monitor_thread and self.folder_monitor_thread.is_alive():
            self.folder_monitor_thread.join(timeout=1.0)
            
        self.root.destroy()
        
    def run(self):
        """Start the application main loop"""
        try:
            print("Starting Dynamic Portrait Slideshow...")
            print(f"Window Resolution: {self.WINDOW_WIDTH}x{self.WINDOW_HEIGHT}")
            print(f"Animation Speed: {self.ANIMATION_SPEED} pixels/frame")
            print(f"Frame Rate: {1000//self.FRAME_DELAY} FPS")
            print(f"Image Spacing: {self.IMAGE_SPACING} pixels")
            print(f"Slideshow Folder: {os.path.abspath(self.SLIDESHOW_FOLDER)}")
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
        # Create slideshow folder if it doesn't exist
        os.makedirs("slideshow", exist_ok=True)
        
        # Initialize and run application
        app = PortraitSlideshow()
        app.run()
        
    except Exception as e:
        print(f"Failed to start application: {e}")
        return 1
        
    return 0

if __name__ == "__main__":
    exit(main())