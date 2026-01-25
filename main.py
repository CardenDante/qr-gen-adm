import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageDraw, ImageFont
import qrcode
import os
import sys
import platform
import subprocess
import tempfile

# Platform-specific imports
IS_WINDOWS = platform.system() == "Windows"
IS_LINUX = platform.system() == "Linux"

if IS_WINDOWS:
    import win32print
    import win32ui
    from PIL import ImageWin

# Set appearance with modern professional theme
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


class QRCodePrinterApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window configuration
        self.title("QR Code Label Printer")
        self.geometry("1000x600")
        self.resizable(False, False)

        # Set window icon using QR code
        try:
            icon_path = self.get_resource_path("qr_icon.ico")
            if os.path.exists(icon_path):
                if IS_WINDOWS:
                    self.iconbitmap(default=icon_path)
            else:
                # Create QR code icon programmatically if file doesn't exist
                self.create_qr_icon()
        except:
            pass

        # Label sizes in mm (width x height)
        self.label_sizes = {
            "60 x 40 mm": (60, 40),
            "50 x 30 mm": (50, 30),
            "40 x 30 mm": (40, 30),
            "50 x 25 mm": (50, 25),
            "70 x 40 mm": (70, 40),
        }

        self.generated_qr_data = None
        self.qr_image_display = None

        self.create_widgets()

    def get_resource_path(self, relative_path):
        """Get absolute path to resource for PyInstaller"""
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

    def create_qr_icon(self):
        """Create a simple QR code icon programmatically"""
        try:
            # Generate a simple QR code as app icon
            qr = qrcode.QRCode(version=1, box_size=10, border=1)
            qr.add_data("QR")
            qr.make(fit=True)
            icon_img = qr.make_image(fill_color="black", back_color="white")
            icon_img = icon_img.resize((64, 64), Image.Resampling.LANCZOS)

            # Save as ico file
            icon_path = "qr_icon.ico"
            icon_img.save(icon_path, format='ICO')
            if IS_WINDOWS:
                self.iconbitmap(default=icon_path)
        except:
            pass

    def create_widgets(self):
        # Clean modern background
        self.configure(fg_color="#F8F9FA")

        # Main container
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=30, pady=30)

        # Left Panel - Clean card
        left_panel = ctk.CTkFrame(main_frame, fg_color="#FFFFFF",
                                  corner_radius=12, border_width=0)
        left_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 15))

        # Right Panel - Clean card
        right_panel = ctk.CTkFrame(main_frame, fg_color="#FFFFFF",
                                   corner_radius=12, border_width=0)
        right_panel.grid(row=0, column=1, sticky="nsew")

        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)
        main_frame.grid_rowconfigure(0, weight=1)

        # ===== LEFT PANEL CONTENT =====
        # Header
        header_frame = ctk.CTkFrame(left_panel, fg_color="transparent")
        header_frame.pack(pady=(35, 25), padx=35)

        # Title
        title_label = ctk.CTkLabel(
            header_frame,
            text="QR Label Printer",
            font=ctk.CTkFont(size=26, weight="bold"),
            text_color="#1a1a1a"
        )
        title_label.pack()

        subtitle_label = ctk.CTkLabel(
            header_frame,
            text="Generate and print QR code labels",
            font=ctk.CTkFont(size=13),
            text_color="#6c757d"
        )
        subtitle_label.pack(pady=(5, 0))

        # Form container
        form_frame = ctk.CTkFrame(left_panel, fg_color="transparent")
        form_frame.pack(fill="both", expand=True, padx=35, pady=(15, 35))

        # Admission Number Section
        admission_label = ctk.CTkLabel(
            form_frame,
            text="Admission Number",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#495057",
            anchor="w"
        )
        admission_label.pack(fill="x", pady=(20, 8))

        self.admission_entry = ctk.CTkEntry(
            form_frame,
            placeholder_text="Enter number (e.g., 4433)",
            height=48,
            font=ctk.CTkFont(size=15),
            border_width=2,
            corner_radius=8,
            border_color="#dee2e6",
            fg_color="#FFFFFF"
        )
        self.admission_entry.pack(fill="x", pady=(0, 25))
        self.admission_entry.bind("<Return>", lambda e: self.handle_enter_key())

        # Label Size Section
        size_label = ctk.CTkLabel(
            form_frame,
            text="Label Size",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#495057",
            anchor="w"
        )
        size_label.pack(fill="x", pady=(0, 8))

        self.size_dropdown = ctk.CTkComboBox(
            form_frame,
            values=list(self.label_sizes.keys()),
            height=48,
            font=ctk.CTkFont(size=14),
            border_width=2,
            corner_radius=8,
            state="readonly",
            button_color="#007bff",
            border_color="#dee2e6",
            fg_color="#FFFFFF",
            dropdown_fg_color="#FFFFFF"
        )
        self.size_dropdown.set("60 x 40 mm")
        self.size_dropdown.pack(fill="x", pady=(0, 25))

        # Bulk Print Toggle
        self.bulk_mode_var = ctk.BooleanVar(value=False)
        self.bulk_mode_checkbox = ctk.CTkCheckBox(
            form_frame,
            text="Bulk Print Mode",
            variable=self.bulk_mode_var,
            command=self.toggle_bulk_mode,
            font=ctk.CTkFont(size=12),
            text_color="#495057",
            fg_color="#007bff",
            hover_color="#0056b3",
            checkbox_width=20,
            checkbox_height=20
        )
        self.bulk_mode_checkbox.pack(fill="x", pady=(0, 15))

        # Quantity input (hidden by default)
        self.quantity_frame = ctk.CTkFrame(form_frame, fg_color="transparent", height=0)

        quantity_label = ctk.CTkLabel(
            self.quantity_frame,
            text="Quantity",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#495057",
            anchor="w"
        )
        quantity_label.pack(fill="x", pady=(0, 8))

        self.quantity_entry = ctk.CTkEntry(
            self.quantity_frame,
            placeholder_text="How many labels? (e.g., 10)",
            height=48,
            font=ctk.CTkFont(size=15),
            border_width=2,
            corner_radius=8,
            border_color="#dee2e6",
            fg_color="#FFFFFF"
        )
        self.quantity_entry.pack(fill="x", pady=(0, 0))
        self.quantity_entry.bind("<Return>", lambda e: self.handle_enter_key())

        # Modern buttons
        self.generate_btn = ctk.CTkButton(
            form_frame,
            text="Generate QR Code",
            command=self.generate_qr_code,
            height=52,
            font=ctk.CTkFont(size=15, weight="bold"),
            corner_radius=8,
            fg_color="#28a745",
            hover_color="#218838"
        )
        self.generate_btn.pack(fill="x", pady=(0, 12))

        # Print Button
        self.print_btn = ctk.CTkButton(
            form_frame,
            text="Print Label",
            command=self.print_label,
            height=52,
            font=ctk.CTkFont(size=15, weight="bold"),
            corner_radius=8,
            fg_color="#007bff",
            hover_color="#0056b3",
            state="disabled"
        )
        self.print_btn.pack(fill="x")

        # Footer
        footer_label = ctk.CTkLabel(
            left_panel,
            text="WCN26F © 2025",
            font=ctk.CTkFont(size=10),
            text_color="#adb5bd"
        )
        footer_label.pack(side="bottom", pady=18)

        # ===== RIGHT PANEL CONTENT =====
        preview_header = ctk.CTkFrame(right_panel, fg_color="transparent")
        preview_header.pack(pady=(35, 20), padx=35)

        preview_title = ctk.CTkLabel(
            preview_header,
            text="Preview",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#1a1a1a"
        )
        preview_title.pack()

        # Preview Container
        self.preview_container = ctk.CTkFrame(
            right_panel,
            fg_color="#f8f9fa",
            corner_radius=10,
            border_width=2,
            border_color="#e9ecef"
        )
        self.preview_container.pack(fill="both", expand=True, padx=35, pady=(0, 35))

        # Placeholder
        self.placeholder_label = ctk.CTkLabel(
            self.preview_container,
            text="No QR code generated\n\nEnter admission number\nand click Generate",
            font=ctk.CTkFont(size=14),
            text_color="#adb5bd",
            justify="center"
        )
        self.placeholder_label.place(relx=0.5, rely=0.5, anchor="center")

        # QR Code Display (hidden initially)
        self.qr_display_label = ctk.CTkLabel(self.preview_container, text="")

        # Info Labels (hidden initially)
        self.info_frame = ctk.CTkFrame(self.preview_container, fg_color="transparent")

    def toggle_bulk_mode(self):
        """Show/hide quantity input based on bulk mode toggle"""
        if self.bulk_mode_var.get():
            self.quantity_frame.pack(fill="x", pady=(0, 25), before=self.generate_btn)
        else:
            self.quantity_frame.pack_forget()

    def handle_enter_key(self):
        """Handle Enter key: Generate on first press, Print on second press"""
        admission_number = self.admission_entry.get().strip()

        if not admission_number:
            messagebox.showwarning("Input Required", "Please enter an admission number")
            return

        # In bulk mode, check if quantity is provided
        if self.bulk_mode_var.get():
            quantity_str = self.quantity_entry.get().strip()
            if not quantity_str:
                # Focus on quantity field if empty
                self.quantity_entry.focus()
                return

        # If QR already generated for this admission number, print it
        if self.generated_qr_data == admission_number:
            self.print_label()
        else:
            # Generate new QR code
            self.generate_qr_code()

    def generate_qr_code(self):
        admission_number = self.admission_entry.get().strip()

        if not admission_number:
            messagebox.showwarning("Input Required", "Please enter an admission number")
            return

        # Generate QR Code with only the admission number (no prefix in QR)
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=2,
        )
        qr.add_data(admission_number)
        qr.make(fit=True)

        qr_img = qr.make_image(fill_color="black", back_color="white")

        # Full number with prefix for display only
        full_number = f"{admission_number}"

        # Resize for display
        qr_img_display = qr_img.resize((250, 250), Image.Resampling.LANCZOS)

        # Convert to CTkImage
        self.qr_image_display = ctk.CTkImage(light_image=qr_img_display, size=(250, 250))

        # Update UI
        self.placeholder_label.place_forget()

        self.qr_display_label.configure(image=self.qr_image_display)
        self.qr_display_label.pack(pady=(20, 10))

        # Clear old info labels before creating new ones
        for widget in self.info_frame.winfo_children():
            widget.destroy()

        # Show info
        self.info_frame.pack(pady=(0, 20))

        admission_info = ctk.CTkLabel(
            self.info_frame,
            text=full_number,
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#2C3E50"
        )
        admission_info.pack()

        size_info = ctk.CTkLabel(
            self.info_frame,
            text=f"Size: {self.size_dropdown.get()}",
            font=ctk.CTkFont(size=13),
            text_color="#7F8C8D"
        )
        size_info.pack(pady=(5, 0))

        # Enable print button
        self.print_btn.configure(state="normal")

        # Store data
        self.generated_qr_data = admission_number

    def mm_to_pixels(self, mm, dpi=203):
        """Convert millimeters to pixels for thermal printer (203 DPI)"""
        return int((mm / 25.4) * dpi)

    def create_label(self, admission_number, width_mm, height_mm):
        """Create professional label with QR code and text"""
        width_px = self.mm_to_pixels(width_mm)
        height_px = self.mm_to_pixels(height_mm)

        # Create RGB image first for easier drawing, then convert
        label = Image.new('RGB', (width_px, height_px), 'white')
        draw = ImageDraw.Draw(label)

        # Generate QR code with ONLY the admission number (no prefix in QR)
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=1,
        )
        qr.add_data(admission_number)
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="black", back_color="white")

        # Calculate sizes based on label dimensions
        # QR code takes 90% of height, text area takes the rest
        qr_size = int(height_px * 0.90)
        text_area_width = width_px - qr_size - int(width_px * 0.06)  # Remaining space with margin

        # Resize QR code
        qr_img = qr_img.resize((qr_size, qr_size), Image.Resampling.LANCZOS)

        # Position QR code on the left with minimal margin
        margin = int(width_px * 0.02)
        qr_x = margin
        qr_y = (height_px - qr_size) // 2

        label.paste(qr_img, (qr_x, qr_y))

        # Add text on the right side - VERTICALLY (rotated 90 degrees)
        text_x = qr_x + qr_size + int(margin * 0.5)

        # Try to load a bold font, fallback to default
        try:
            # Calculate font size based on available space
            # Font should fit in the remaining width when rotated
            # Increased size for better visibility on all label types
            font_size = int(height_px * 0.18)

            # Try to find fonts based on platform
            if IS_WINDOWS:
                font_paths = [
                    "C:/Windows/Fonts/arialbd.ttf",  # Arial Bold
                    "C:/Windows/Fonts/arial.ttf",     # Arial Regular
                    "C:/Windows/Fonts/calibrib.ttf",  # Calibri Bold
                ]
            else:
                # Linux font paths
                font_paths = [
                    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
                    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
                    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
                    "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
                    "/usr/share/fonts/TTF/DejaVuSans-Bold.ttf",
                    "/usr/share/fonts/TTF/DejaVuSans.ttf",
                ]

            text_font = None

            for font_path in font_paths:
                if os.path.exists(font_path):
                    try:
                        text_font = ImageFont.truetype(font_path, font_size)
                        break
                    except:
                        continue

            if not text_font:
                text_font = ImageFont.load_default()

        except Exception as e:
            text_font = ImageFont.load_default()

        # Create the full text (no line breaks)
        full_text = admission_number

        # Create a temporary image to draw the text horizontally
        temp_bbox = draw.textbbox((0, 0), full_text, font=text_font)
        text_width = temp_bbox[2] - temp_bbox[0]
        text_height = temp_bbox[3] - temp_bbox[1]

        # Create temporary image for text
        text_img = Image.new('RGB', (text_width + 20, text_height + 20), 'white')
        text_draw = ImageDraw.Draw(text_img)
        text_draw.text((10, 10), full_text, fill='black', font=text_font)

        # Rotate text 90 degrees counter-clockwise
        text_img_rotated = text_img.rotate(90, expand=True)

        # Calculate position to center the rotated text vertically and place it on the right
        rotated_width, rotated_height = text_img_rotated.size
        text_paste_x = text_x
        text_paste_y = (height_px - rotated_height) // 2

        # Paste the rotated text onto the label
        label.paste(text_img_rotated, (text_paste_x, text_paste_y))

        # Add a visible border for professional look
        border_width = 4
        draw.rectangle(
            [border_width, border_width, width_px - border_width, height_px - border_width],
            outline='black',
            width=border_width
        )

        # Convert to monochrome for thermal printer
        label = label.convert('1', dither=Image.Dither.NONE)

        return label

    def find_printer(self):
        """Find printer based on platform"""
        if IS_WINDOWS:
            return self.find_xprinter_windows()
        else:
            return self.find_printer_linux()

    def find_xprinter_windows(self):
        """Find Xprinter 470B on Windows"""
        printers = [printer[2] for printer in win32print.EnumPrinters(2)]

        for printer in printers:
            if "470B" in printer or "XP-470B" in printer or "XPRINTER" in printer.upper():
                return printer

        return win32print.GetDefaultPrinter()

    def find_printer_linux(self):
        """Find printer on Linux using CUPS"""
        try:
            # Get list of printers
            result = subprocess.run(['lpstat', '-p'], capture_output=True, text=True)
            printers = result.stdout

            # Look for Xprinter
            for line in printers.split('\n'):
                if '470B' in line or 'XP-470B' in line or 'XPRINTER' in line.upper():
                    # Extract printer name
                    parts = line.split()
                    if len(parts) >= 2:
                        return parts[1]

            # Get default printer
            result = subprocess.run(['lpstat', '-d'], capture_output=True, text=True)
            if 'system default destination:' in result.stdout:
                return result.stdout.split(':')[1].strip()

            # Fallback: get first available printer
            result = subprocess.run(['lpstat', '-p'], capture_output=True, text=True)
            for line in result.stdout.split('\n'):
                if line.startswith('printer'):
                    parts = line.split()
                    if len(parts) >= 2:
                        return parts[1]

            return None
        except Exception as e:
            return None

    def print_label_windows(self, label_image, printer_name):
        """Print using Windows API"""
        hPrinter = win32print.OpenPrinter(printer_name)

        try:
            hDC = win32ui.CreateDC()
            hDC.CreatePrinterDC(printer_name)

            hDC.StartDoc("QR Code Label")
            hDC.StartPage()

            # Convert and print
            dib = ImageWin.Dib(label_image)
            img_width, img_height = label_image.size
            dib.draw(hDC.GetHandleOutput(), (0, 0, img_width, img_height))

            hDC.EndPage()
            hDC.EndDoc()
            hDC.DeleteDC()

        finally:
            win32print.ClosePrinter(hPrinter)

    def print_label_linux(self, label_image, printer_name):
        """Print using CUPS on Linux"""
        # Save image to temporary file
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
            tmp_path = tmp.name
            # Convert to RGB for PNG saving
            if label_image.mode == '1':
                label_image = label_image.convert('RGB')
            label_image.save(tmp_path, 'PNG')

        try:
            # Print using lp command
            cmd = ['lp']
            if printer_name:
                cmd.extend(['-d', printer_name])
            cmd.append(tmp_path)

            result = subprocess.run(cmd, capture_output=True, text=True)

            if result.returncode != 0:
                raise Exception(f"Print failed: {result.stderr}")

        finally:
            # Clean up temp file
            try:
                os.unlink(tmp_path)
            except:
                pass

    def print_label(self):
        if not self.generated_qr_data:
            messagebox.showwarning("No QR Code", "Please generate a QR code first")
            return

        # Check if bulk mode is enabled
        if self.bulk_mode_var.get():
            self.print_bulk_labels()
            return

        try:
            # Disable button
            self.print_btn.configure(state="disabled", text="Printing...")
            self.update()

            # Get size
            selected_size = self.size_dropdown.get()
            width_mm, height_mm = self.label_sizes[selected_size]

            # Create label
            label_image = self.create_label(self.generated_qr_data, width_mm, height_mm)

            # Find printer
            printer_name = self.find_printer()

            if not printer_name and IS_LINUX:
                raise Exception("No printer found. Please ensure CUPS is installed and a printer is configured.")

            # Print based on platform
            if IS_WINDOWS:
                self.print_label_windows(label_image, printer_name)
            else:
                self.print_label_linux(label_image, printer_name)

            # Show auto-disappearing success dialog
            admission_num = self.generated_qr_data
            self.show_auto_close_dialog(
                "Success",
                f"Label printed successfully!\n\nAdmission: {admission_num}\nPrinter: {printer_name}\nSize: {selected_size}"
            )

            # Clear
            self.clear_preview()

        except Exception as e:
            messagebox.showerror(
                "Print Error",
                f"Failed to print:\n{str(e)}\n\nPlease check:\n- Printer is connected\n- Printer is turned on\n- Printer drivers are installed"
            )
        finally:
            self.print_btn.configure(state="normal", text="Print Label")

    def print_bulk_labels(self):
        """Print multiple labels in sequence"""
        try:
            # Get starting number and quantity
            starting_number = self.admission_entry.get().strip()
            quantity_str = self.quantity_entry.get().strip()

            if not starting_number:
                messagebox.showwarning("Input Required", "Please enter starting admission number")
                return

            if not quantity_str:
                messagebox.showwarning("Input Required", "Please enter quantity")
                self.quantity_entry.focus()
                return

            try:
                quantity = int(quantity_str)
                if quantity <= 0:
                    raise ValueError()
            except ValueError:
                messagebox.showwarning("Invalid Input", "Quantity must be a positive number")
                return

            # Disable button
            self.print_btn.configure(state="disabled")
            self.generate_btn.configure(state="disabled")
            self.update()

            # Get size
            selected_size = self.size_dropdown.get()
            width_mm, height_mm = self.label_sizes[selected_size]

            # Find printer
            printer_name = self.find_printer()

            if not printer_name and IS_LINUX:
                raise Exception("No printer found. Please ensure CUPS is installed and a printer is configured.")

            # Check if starting number is numeric for incrementing
            try:
                start_num = int(starting_number)
                is_numeric = True
            except ValueError:
                is_numeric = False
                messagebox.showwarning("Invalid Input", "Starting admission number must be numeric for bulk printing")
                return

            # Print each label in sequence
            for i in range(quantity):
                current_number = str(start_num + i)

                # Update button with progress
                self.print_btn.configure(text=f"Printing {i+1}/{quantity}...")
                self.update()

                # Create label
                label_image = self.create_label(current_number, width_mm, height_mm)

                # Print based on platform
                if IS_WINDOWS:
                    self.print_label_windows(label_image, printer_name)
                else:
                    self.print_label_linux(label_image, printer_name)

            # Show success dialog
            self.show_auto_close_dialog(
                "Bulk Print Complete",
                f"Successfully printed {quantity} labels!\n\nRange: {start_num} to {start_num + quantity - 1}\nPrinter: {printer_name}\nSize: {selected_size}",
                timeout=3000
            )

            # Clear
            self.clear_preview()

        except Exception as e:
            messagebox.showerror(
                "Print Error",
                f"Failed to print:\n{str(e)}\n\nPlease check:\n- Printer is connected\n- Printer is turned on\n- Printer drivers are installed"
            )
        finally:
            self.print_btn.configure(state="normal", text="Print Label")
            self.generate_btn.configure(state="normal")

    def clear_preview(self):
        """Clear preview and reset form"""
        self.qr_display_label.pack_forget()
        self.info_frame.pack_forget()
        self.placeholder_label.place(relx=0.5, rely=0.5, anchor="center")

        self.admission_entry.delete(0, 'end')
        self.quantity_entry.delete(0, 'end')
        self.generated_qr_data = None
        self.print_btn.configure(state="disabled")
        self.admission_entry.focus()

    def show_auto_close_dialog(self, title, message, timeout=2000):
        """Show a modal dialog that auto-closes after timeout (in milliseconds)"""
        # Create a top-level window
        dialog = ctk.CTkToplevel(self)
        dialog.title(title)
        dialog.geometry("400x200")
        dialog.resizable(False, False)

        # Center the dialog on parent window
        dialog.transient(self)
        dialog.grab_set()

        # Add message
        label = ctk.CTkLabel(
            dialog,
            text=message,
            font=ctk.CTkFont(size=14),
            wraplength=350
        )
        label.pack(expand=True, pady=30, padx=20)

        # Schedule auto-close
        dialog.after(timeout, dialog.destroy)

        # Center dialog on screen
        dialog.update_idletasks()
        x = self.winfo_x() + (self.winfo_width() - dialog.winfo_width()) // 2
        y = self.winfo_y() + (self.winfo_height() - dialog.winfo_height()) // 2
        dialog.geometry(f"+{x}+{y}")


if __name__ == "__main__":
    app = QRCodePrinterApp()
    app.mainloop()
