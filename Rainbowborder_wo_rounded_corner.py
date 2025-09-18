"""
Rainbow Border Animation for CustomTkinter

This module creates an animated rainbow border that continuously cycles colors
around the perimeter of a window. The rainbow effect moves smoothly in a clockwise
direction, creating a vibrant and dynamic visual effect.

Author: Your Name
Date: September 2025
"""

import customtkinter as ctk


class RainbowBorder(ctk.CTkCanvas):
    """
    A CustomTkinter Canvas widget that displays an animated rainbow border.
    
    The rainbow cycles through the full color spectrum (Red → Yellow → Green → 
    Cyan → Blue → Magenta → Red) and continuously moves around the border perimeter.
    """

    def __init__(self, master, border_width=5, fps=20, **kwargs):
        """
        Initialize the RainbowBorder widget.
        
        Args:
            master: Parent widget
            border_width: Width of the border in pixels (default: 10)
            **kwargs: Additional arguments passed to CTkCanvas
        """
        kwargs.setdefault('highlightthickness', 0)  # Remove focus border
        kwargs.setdefault('bd', 0)  # Remove border
        kwargs.setdefault('relief', 'flat')  # Flat relief
        
        super().__init__(master, **kwargs)
        self._border_width = border_width
        self.position = 0  # Current animation position around the perimeter
        self.fps = fps
        
        

        # Bind window resize event to redraw the border
        self.bind("<Configure>", self._on_configure)
        
        self.lower("all")
        
        # Pack the widget to fill the entire window
        self.pack(fill="both", expand=True)

        
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
        self.after(1000 // self.fps, self._animate)  # Schedule next frame

    def _draw_gradient(self):
        """
        Draw the complete rainbow border by rendering each border segment.
        
        The border is divided into four segments (top, right, bottom, left) and
        each segment is drawn with the appropriate rainbow colors based on the
        current animation position.
        """
        # Get current window dimensions
        self.width = self.winfo_width()
        self.height = self.winfo_height()
        border_width = self._border_width

        # Skip drawing if window is too small
        if self.width <= border_width or self.height <= border_width:
            return

        # Clear previous frame
        self.delete("all")

        # Calculate total perimeter for color mapping
        perimeter = 2 * (self.width + self.height - 2 * border_width)
        if perimeter <= 0:
            return

        # Draw each border segment with rainbow colors
        self._draw_top_border(perimeter)
        self._draw_right_border(perimeter)
        self._draw_bottom_border(perimeter)
        self._draw_left_border(perimeter)

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
        Draw the top border segment with rainbow colors.
        
        Args:
            perimeter: Total perimeter length for color calculation
        """
        border_width = self._border_width
        top_length = self.width - border_width
        
        for i in range(top_length):
            # Position 0 starts at top-left corner
            current_position = i
            color = self._get_rainbow_color(current_position, perimeter, self.position)
            # Draw vertical line from top edge down to border_width
            self.create_line(i, 0, i, border_width, fill=color)

    def _draw_right_border(self, perimeter):
        """
        Draw the right border segment with rainbow colors.
        
        Args:
            perimeter: Total perimeter length for color calculation
        """
        border_width = self._border_width
        right_start = self.width - border_width  # Start after top border
        right_length = self.height
        
        for i in range(right_length):
            # Continue position count from end of top border
            current_position = right_start + i
            color = self._get_rainbow_color(current_position, perimeter, self.position)
            # Draw horizontal line from right edge inward
            self.create_line(self.width - border_width, i, self.width, i, fill=color)

    def _draw_bottom_border(self, perimeter):
        """
        Draw the bottom border segment with rainbow colors.
        
        Args:
            perimeter: Total perimeter length for color calculation
        """
        border_width = self._border_width
        # Start position after top and right borders
        bottom_start = (self.width - border_width) + self.height
        bottom_length = self.width - border_width
        
        for i in range(bottom_length):
            # Continue position count from end of right border
            current_position = bottom_start + i
            color = self._get_rainbow_color(current_position, perimeter, self.position)
            # Draw from right to left (clockwise direction)
            x_pos = self.width - border_width - i
            self.create_line(x_pos, self.height - border_width, x_pos, self.height, fill=color)

    def _draw_left_border(self, perimeter):
        """
        Draw the left border segment with rainbow colors.
        
        Args:
            perimeter: Total perimeter length for color calculation
        """
        border_width = self._border_width
        # Start position after top, right, and bottom borders
        left_start = 2 * (self.width - border_width) + self.height
        left_length = self.height - border_width
        
        for i in range(left_length):
            # Continue position count from end of bottom border
            current_position = left_start + i
            color = self._get_rainbow_color(current_position, perimeter, self.position)
            # Draw from bottom to top (clockwise direction)
            y_pos = self.height - border_width - i
            self.create_line(0, y_pos, border_width, y_pos, fill=color)


if __name__ == "__main__":
    """
    Main execution block - creates and runs the rainbow border demonstration.
    
    This creates a small window with an animated rainbow border that continuously
    cycles colors around the perimeter. Perfect for testing or as a decorative
    element in larger applications.
    """
    # Create the main application window
    root = ctk.CTk()
    root.resizable(False, False)  # Fixed size window
    root.geometry("300x500+810+340")  # Width x Height + X_offset + Y_offset
    root.title("Rainbow Border Demo")  # Window title
    
    # Create the rainbow border widget
    rainbow_border = RainbowBorder(root, border_width=5)

    label = ctk.CTkLabel(rainbow_border, text="Rainbow Border", font=ctk.CTkFont(size=20, weight="bold"), bg_color="dark gray").pack(pady=10)

    # Start the GUI event loop
    root.mainloop()