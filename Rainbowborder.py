"""
Rainbow Border Animation for CustomTkinter

This module creates an animated rainbow border that continuously cycles colors
around the perimeter of a window. The rainbow effect moves smoothly in a clockwise
direction, creating a vibrant and dynamic visual effect.

Author: Your Name
Date: September 2025
"""

import customtkinter as ctk
from PIL import Image, ImageTk


class RainbowBorder(ctk.CTkCanvas):
    """
    A CustomTkinter Canvas widget that displays an animated rainbow border.
    
    The rainbow cycles through the full color spectrum (Red → Yellow → Green → 
    Cyan → Blue → Magenta → Red) and continuously moves around the border perimeter.
    """

    def __init__(self, master, border_width=5, corner_radius=10, fps=20, color="dark gray", **kwargs):
        """
        Initialize the RainbowBorder widget.
        
        Args:
            master: Parent widget
            border_width: Width of the border in pixels (default: 5)
            corner_radius: Radius of rounded corners in pixels (default: 15)
            fps: Animation frame rate (default: 20)
            **kwargs: Additional arguments passed to CTkCanvas
        """
        # Set canvas properties to eliminate gaps and rounded corners
        kwargs.setdefault('highlightthickness', 0)  # Remove focus border
        kwargs.setdefault('bd', 0)  # Remove border
        kwargs.setdefault('relief', 'flat')  # Flat relief


        super().__init__(master, bg=color, **kwargs)
        self._border_width = border_width
        self._corner_radius = corner_radius
        self.position = 0
        self.fps = fps
        self.background_image_id = None  # Store background image ID
        self.persistent_items = set()  # Store IDs of items that shouldn't be deleted
        
        # Bind window resize event to redraw the border
        self.bind("<Configure>", self._on_configure)
        
        self.lift("all")
        
        # Pack the widget to fill the entire window with no padding
        self.pack(fill="both", expand=True, padx=0, pady=0)
        
        # Start the animation loop
        self._animate()

    def _on_configure(self, event):
        """Handle window resize events by redrawing the border."""
        self._draw_gradient()

    def _animate(self):
        """
        Main animation loop that continuously updates the rainbow position.
        
        This method calls itself repeatedly using the 'after' method to create
        smooth animation at approximately 20 FPS (50ms intervals).
        """
        self._draw_gradient()
        self.position += 3  # Animation speed (higher = faster movement)
        self.lower("all")
        self.after(1000 // self.fps, self._animate)  # Schedule next frame

    def set_background_image(self, image):
        """Set a background image that won't be deleted during animation."""
        if self.background_image_id:
            self.delete(self.background_image_id)
            self.persistent_items.discard(self.background_image_id)
        self.background_image_id = self.create_image(0, 0, anchor="nw", image=image)
        self.persistent_items.add(self.background_image_id)

    def create_persistent_text(self, x, y, **kwargs):
        """Create text that won't be deleted during animation."""
        text_id = self.create_text(x, y, **kwargs)
        self.persistent_items.add(text_id)
        return text_id

    def create_persistent_item(self, item_type, *args, **kwargs):
        """Create any canvas item that won't be deleted during animation."""
        create_method = getattr(self, f"create_{item_type}")
        item_id = create_method(*args, **kwargs)
        self.persistent_items.add(item_id)
        return item_id

    def _draw_gradient(self):
        """Draw the complete rainbow border while preserving background image."""
        # Get current window dimensions
        self.width = self.winfo_width()
        self.height = self.winfo_height()
        border_width = self._border_width

        # Skip drawing if window is too small
        if self.width <= border_width or self.height <= border_width:
            return

        # Clear only border elements, not persistent items
        items_to_delete = []
        for item in self.find_all():
            if item not in self.persistent_items:
                items_to_delete.append(item)
        
        for item in items_to_delete:
            self.delete(item)

        # Calculate total perimeter including rounded corners
        import math
        corner_arc_length = 2 * math.pi * self._corner_radius / 4  # Quarter circle per corner
        straight_perimeter = 2 * (self.width + self.height - 4 * self._corner_radius - 2 * border_width)
        perimeter = straight_perimeter + 4 * corner_arc_length
        if perimeter <= 0:
            return

        # Draw each border segment with rainbow colors
        self._draw_top_border(perimeter)
        self._draw_top_right_corner(perimeter)
        self._draw_right_border(perimeter)
        self._draw_bottom_right_corner(perimeter)
        self._draw_bottom_border(perimeter)
        self._draw_bottom_left_corner(perimeter)
        self._draw_left_border(perimeter)
        self._draw_top_left_corner(perimeter)
        self.lower("all")

    def _get_rainbow_color(self, position, perimeter, offset=0):
        """
        Calculate rainbow color based on position around the perimeter.
        
        Args:
            position: Current position on the border perimeter
            perimeter: Total perimeter length
            offset: Animation offset for movement effect
            
        Returns:
            str: Hex color string (e.g., "#FF0000" for red)
        """
        # Apply animation offset and wrap around perimeter
        color_position = (position + offset) % perimeter
        
        # Map position to rainbow spectrum (0-6 for 6 color segments)
        hue = (color_position / perimeter) * 6
        
        # Calculate RGB values for each segment of the rainbow
        if hue < 1:  # Red → Yellow (red=255, green increases, blue=0)
            r, g, b = 255, int(255 * hue), 0
        elif hue < 2:  # Yellow → Green (red decreases, green=255, blue=0)
            r, g, b = int(255 * (2 - hue)), 255, 0
        elif hue < 3:  # Green → Cyan (red=0, green=255, blue increases)
            r, g, b = 0, 255, int(255 * (hue - 2))
        elif hue < 4:  # Cyan → Blue (red=0, green decreases, blue=255)
            r, g, b = 0, int(255 * (4 - hue)), 255
        elif hue < 5:  # Blue → Magenta (red increases, green=0, blue=255)
            r, g, b = int(255 * (hue - 4)), 0, 255
        else:  # Magenta → Red (red=255, green=0, blue decreases)
            r, g, b = 255, 0, int(255 * (6 - hue))
        
        return f"#{r:02x}{g:02x}{b:02x}"

    def _draw_top_border(self, perimeter):
        """
        Draw the top border segment with rainbow colors, excluding corners.
        
        Args:
            perimeter: Total perimeter length for color calculation
        """
        border_width = self._border_width
        corner_radius = self._corner_radius
        
        # Top border starts after top-left corner and ends before top-right corner
        start_x = corner_radius
        end_x = self.width - corner_radius
        top_length = end_x - start_x
        
        if top_length <= 0:
            return
            
        for i in range(top_length):
            # Position starts after the top-left corner arc
            current_position = i
            color = self._get_rainbow_color(current_position, perimeter, self.position)
            # Draw vertical line from top edge down to border_width
            x_pos = start_x + i
            self.create_line(x_pos, 0, x_pos, border_width, fill=color)

    def _draw_right_border(self, perimeter):
        """
        Draw the right border segment with rainbow colors, excluding corners.
        
        Args:
            perimeter: Total perimeter length for color calculation
        """
        import math
        border_width = self._border_width
        corner_radius = self._corner_radius
        
        # Right border starts after top border and top-right corner
        top_length = self.width - 2 * corner_radius
        corner_arc_length = math.pi * corner_radius / 2
        right_start = top_length + corner_arc_length
        
        # Right border length (excluding corners)
        start_y = corner_radius
        end_y = self.height - corner_radius
        right_length = end_y - start_y
        
        if right_length <= 0:
            return
            
        for i in range(right_length):
            current_position = right_start + i
            color = self._get_rainbow_color(current_position, perimeter, self.position)
            y_pos = start_y + i
            self.create_line(self.width - border_width, y_pos, self.width, y_pos, fill=color)

    def _draw_bottom_border(self, perimeter):
        """
        Draw the bottom border segment with rainbow colors, excluding corners.
        
        Args:
            perimeter: Total perimeter length for color calculation
        """
        import math
        border_width = self._border_width
        corner_radius = self._corner_radius
        
        # Bottom border starts after top, top-right corner, right, and bottom-right corner
        top_length = self.width - 2 * corner_radius
        right_length = self.height - 2 * corner_radius
        corner_arc_length = math.pi * corner_radius / 2
        bottom_start = top_length + corner_arc_length + right_length + corner_arc_length
        
        # Bottom border length (excluding corners)
        start_x = self.width - corner_radius
        end_x = corner_radius
        bottom_length = start_x - end_x
        
        if bottom_length <= 0:
            return
            
        for i in range(bottom_length):
            current_position = bottom_start + i
            color = self._get_rainbow_color(current_position, perimeter, self.position)
            # Draw from right to left (clockwise direction)
            x_pos = start_x - i
            self.create_line(x_pos, self.height - border_width, x_pos, self.height, fill=color)

    def _draw_left_border(self, perimeter):
        """
        Draw the left border segment with rainbow colors, excluding corners.
        
        Args:
            perimeter: Total perimeter length for color calculation
        """
        import math
        border_width = self._border_width
        corner_radius = self._corner_radius
        
        # Left border starts after top, top-right corner, right, bottom-right corner, bottom, and bottom-left corner
        top_length = self.width - 2 * corner_radius
        right_length = self.height - 2 * corner_radius
        bottom_length = self.width - 2 * corner_radius
        corner_arc_length = math.pi * corner_radius / 2
        left_start = top_length + corner_arc_length + right_length + corner_arc_length + bottom_length + corner_arc_length
        
        # Left border length (excluding corners)
        start_y = self.height - corner_radius
        end_y = corner_radius
        left_length = start_y - end_y
        
        if left_length <= 0:
            return
            
        for i in range(left_length):
            current_position = left_start + i
            color = self._get_rainbow_color(current_position, perimeter, self.position)
            # Draw from bottom to top (clockwise direction)
            y_pos = start_y - i
            self.create_line(0, y_pos, border_width, y_pos, fill=color)

    def _draw_top_right_corner(self, perimeter):
        """Draw the top-right rounded corner with rainbow colors."""
        import math
        border_width = self._border_width
        corner_radius = self._corner_radius
        
        # Top border length for position calculation
        top_length = self.width - 2 * corner_radius
        arc_start_position = top_length
        
        # Draw the quarter circle arc
        center_x = self.width - corner_radius
        center_y = corner_radius
        
        for angle in range(0, 91, 2):  # 0 to 90 degrees, step by 2
            rad = math.radians(angle)
            
            # Calculate arc position for color
            arc_progress = angle / 90.0
            arc_length = math.pi * corner_radius / 2
            current_position = arc_start_position + (arc_progress * arc_length)
            
            color = self._get_rainbow_color(current_position, perimeter, self.position)
            
            # Draw small arc segment
            x1 = center_x + (corner_radius - border_width) * math.cos(rad)
            y1 = center_y - (corner_radius - border_width) * math.sin(rad)
            x2 = center_x + corner_radius * math.cos(rad)
            y2 = center_y - corner_radius * math.sin(rad)
            
            self.create_line(x1, y1, x2, y2, fill=color, width=2)

    def _draw_bottom_right_corner(self, perimeter):
        """Draw the bottom-right rounded corner with rainbow colors."""
        import math
        border_width = self._border_width
        corner_radius = self._corner_radius
        
        # Position after top border and right border
        top_length = self.width - 2 * corner_radius
        right_length = self.height - 2 * corner_radius
        corner_arc_length = math.pi * corner_radius / 2
        arc_start_position = top_length + corner_arc_length + right_length
        
        center_x = self.width - corner_radius
        center_y = self.height - corner_radius
        
        for angle in range(0, 91, 2):
            rad = math.radians(angle)
            arc_progress = angle / 90.0
            current_position = arc_start_position + (arc_progress * corner_arc_length)
            
            color = self._get_rainbow_color(current_position, perimeter, self.position)
            
            x1 = center_x + (corner_radius - border_width) * math.sin(rad)
            y1 = center_y + (corner_radius - border_width) * math.cos(rad)
            x2 = center_x + corner_radius * math.sin(rad)
            y2 = center_y + corner_radius * math.cos(rad)
            
            self.create_line(x1, y1, x2, y2, fill=color, width=2)

    def _draw_bottom_left_corner(self, perimeter):
        """Draw the bottom-left rounded corner with rainbow colors."""
        import math
        border_width = self._border_width
        corner_radius = self._corner_radius
        
        # Position calculation
        top_length = self.width - 2 * corner_radius
        right_length = self.height - 2 * corner_radius
        bottom_length = self.width - 2 * corner_radius
        corner_arc_length = math.pi * corner_radius / 2
        arc_start_position = top_length + corner_arc_length + right_length + corner_arc_length + bottom_length
        
        center_x = corner_radius
        center_y = self.height - corner_radius
        
        for angle in range(0, 91, 2):
            rad = math.radians(angle)
            arc_progress = angle / 90.0
            current_position = arc_start_position + (arc_progress * corner_arc_length)
            
            color = self._get_rainbow_color(current_position, perimeter, self.position)
            
            x1 = center_x - (corner_radius - border_width) * math.cos(rad)
            y1 = center_y + (corner_radius - border_width) * math.sin(rad)
            x2 = center_x - corner_radius * math.cos(rad)
            y2 = center_y + corner_radius * math.sin(rad)
            
            self.create_line(x1, y1, x2, y2, fill=color, width=2)

    def _draw_top_left_corner(self, perimeter):
        """Draw the top-left rounded corner with rainbow colors."""
        import math
        border_width = self._border_width
        corner_radius = self._corner_radius
        
        # Position calculation (last corner)
        top_length = self.width - 2 * corner_radius
        right_length = self.height - 2 * corner_radius
        bottom_length = self.width - 2 * corner_radius
        left_length = self.height - 2 * corner_radius
        corner_arc_length = math.pi * corner_radius / 2
        arc_start_position = top_length + corner_arc_length + right_length + corner_arc_length + bottom_length + corner_arc_length + left_length
        
        center_x = corner_radius
        center_y = corner_radius
        
        for angle in range(0, 91, 2):
            rad = math.radians(angle)
            arc_progress = angle / 90.0
            current_position = arc_start_position + (arc_progress * corner_arc_length)
            
            color = self._get_rainbow_color(current_position, perimeter, self.position)
            
            x1 = center_x - (corner_radius - border_width) * math.sin(rad)
            y1 = center_y - (corner_radius - border_width) * math.cos(rad)
            x2 = center_x - corner_radius * math.sin(rad)
            y2 = center_y - corner_radius * math.cos(rad)
            
            self.create_line(x1, y1, x2, y2, fill=color, width=2)


if __name__ == "__main__":
    root = ctk.CTk()
    root.resizable(False, False)
    root.geometry("1500x900+530+350")
    root.title("Rainbow Border Demo - Login Screen")

    rainbow_border = RainbowBorder(root, border_width=5, corner_radius=10, color="#2b2b2b")
    rainbow_border.grid_columnconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9), weight=1)
    rainbow_border.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9), weight=1)
    
    # Load and set background image
    img = Image.open("bg_gradient.jpg").resize((1500, 900))
    photo = ImageTk.PhotoImage(img)
    rainbow_border.photo = photo  # Keep reference
    rainbow_border.set_background_image(rainbow_border.photo)
    # Use persistent text method so it won't be deleted during animation
    rainbow_border.create_persistent_text(450, 450, text="Welcome back", 
                                         font=("Arial", 30, "bold"), 
                                         fill="white", 
                                         anchor="center")
    
    rainbow_border.create_persistent_text(450, 500, text="Please log in to continue", 
                                         font=("Arial", 20), 
                                         fill="white", 
                                         anchor="center")
    
    Username_entry = ctk.CTkEntry(rainbow_border, placeholder_text="Username", width=300, corner_radius=0, font=("Arial", 40))
    Username_entry.grid(row=4, column=7, columnspan=2, sticky="nsew", pady=(0, 30))
    Password_entry = ctk.CTkEntry(rainbow_border, placeholder_text="Password", show="*", width=300, corner_radius=0, font=("Arial", 40))
    Password_entry.grid(row=5, column=7, columnspan=2, sticky="nsew", pady=(0, 30))
    Login_button = ctk.CTkButton(rainbow_border, text="Login", width=100, corner_radius=0, font=("Arial", 40))
    Login_button.grid(row=7, column=7, columnspan=2, sticky="nsew", pady=(0, 30))

    root.mainloop()