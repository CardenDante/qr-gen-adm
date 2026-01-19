import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageDraw, ImageFont
import qrcode
import win32print
import win32ui
from PIL import ImageWin
import os
import sys

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

        # Set window icon if available
        try:
            icon_path = self.get_resource_path("Profile.png")
            if os.path.exists(icon_path):
                self.iconbitmap(default=icon_path)
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
        self.admission_entry.bind("<Return>", lambda e: self.generate_qr_code())

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
        self.size_dropdown.pack(fill="x", pady=(0, 35))

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
        full_number = f"WCN26F-{admission_number}"

        # Resize for display
        qr_img_display = qr_img.resize((250, 250), Image.Resampling.LANCZOS)

        # Convert to CTkImage
        self.qr_image_display = ctk.CTkImage(light_image=qr_img_display, size=(250, 250))

        # Update UI
        self.placeholder_label.place_forget()

        self.qr_display_label.configure(image=self.qr_image_display)
        self.qr_display_label.pack(pady=(20, 10))

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

        # Add text on the right side
        text_x = qr_x + qr_size + int(margin * 0.5)
        text_y_center = height_px // 2

        # Try to load a bold font, fallback to default
        try:
            # Calculate font sizes based on label height - smaller fonts
            title_font_size = int(height_px * 0.12)
            number_font_size = int(height_px * 0.22)

            # Try to find Arial Bold
            font_paths = [
                "C:/Windows/Fonts/arialbd.ttf",  # Arial Bold
                "C:/Windows/Fonts/arial.ttf",     # Arial Regular
                "C:/Windows/Fonts/calibrib.ttf",  # Calibri Bold
            ]

            title_font = None
            number_font = None

            for font_path in font_paths:
                if os.path.exists(font_path):
                    try:
                        title_font = ImageFont.truetype(font_path, title_font_size)
                        number_font = ImageFont.truetype(font_path, number_font_size)
                        break
                    except:
                        continue

            if not title_font:
                title_font = ImageFont.load_default()
                number_font = ImageFont.load_default()

        except Exception as e:
            title_font = ImageFont.load_default()
            number_font = ImageFont.load_default()

        # Draw "WCN26F-" title
        title_text = "WCN26F-"
        title_bbox = draw.textbbox((0, 0), title_text, font=title_font)
        title_width = title_bbox[2] - title_bbox[0]
        title_height = title_bbox[3] - title_bbox[1]

        # Draw admission number
        number_bbox = draw.textbbox((0, 0), admission_number, font=number_font)
        number_width = number_bbox[2] - number_bbox[0]
        number_height = number_bbox[3] - number_bbox[1]

        # Calculate vertical positions to center the text block
        total_text_height = title_height + number_height + int(height_px * 0.05)
        text_start_y = text_y_center - (total_text_height // 2)

        # Center text horizontally in available space
        title_x = text_x + (text_area_width - title_width) // 2
        number_x = text_x + (text_area_width - number_width) // 2

        # Draw the text
        draw.text((title_x, text_start_y), title_text, fill='black', font=title_font)
        draw.text((number_x, text_start_y + title_height + int(height_px * 0.05)),
                  admission_number, fill='black', font=number_font)

        # Add a subtle border for professional look
        border_width = 2
        draw.rectangle(
            [border_width, border_width, width_px - border_width, height_px - border_width],
            outline='black',
            width=border_width
        )

        # Convert to monochrome for thermal printer
        label = label.convert('1', dither=Image.Dither.NONE)

        return label

    def find_xprinter(self):
        """Find Xprinter 470B"""
        printers = [printer[2] for printer in win32print.EnumPrinters(2)]

        for printer in printers:
            if "470B" in printer or "XP-470B" in printer or "XPRINTER" in printer.upper():
                return printer

        return win32print.GetDefaultPrinter()

    def print_label(self):
        if not self.generated_qr_data:
            messagebox.showwarning("No QR Code", "Please generate a QR code first")
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
            printer_name = self.find_xprinter()

            # Print
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

            messagebox.showinfo(
                "Success",
                f"Label printed successfully!\n\nAdmission: {self.generated_qr_data}\nPrinter: {printer_name}\nSize: {selected_size}"
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

    def clear_preview(self):
        """Clear preview and reset form"""
        self.qr_display_label.pack_forget()
        self.info_frame.pack_forget()
        self.placeholder_label.place(relx=0.5, rely=0.5, anchor="center")

        self.admission_entry.delete(0, 'end')
        self.generated_qr_data = None
        self.print_btn.configure(state="disabled")
        self.admission_entry.focus()


if __name__ == "__main__":
    app = QRCodePrinterApp()
    app.mainloop()
