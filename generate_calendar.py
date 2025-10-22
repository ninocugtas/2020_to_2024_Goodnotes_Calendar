"""
Goodnotes Calendar Generator (2020-2024)
Creates a clickable PDF calendar with dark mode and colorful navigation tabs
"""

import calendar
from datetime import datetime
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, white, black
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Configuration
YEARS = [2020, 2021, 2022, 2023, 2024]
MONTHS = list(range(1, 13))
MONTH_NAMES = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN',
               'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']

# Page settings
PAGE_WIDTH, PAGE_HEIGHT = letter  # 8.5 x 11 inches
MARGIN = 0.15 * inch  # Minimal margin for maximum space
TAB_WIDTH = 0.5 * inch  # Slightly narrower tabs

# Dark mode colors
BG_COLOR = HexColor('#000000')  # True black
TEXT_COLOR = HexColor('#FFFFFF')  # White
GRID_COLOR = HexColor('#333333')  # Dark gray for grid lines
HEADER_COLOR = HexColor('#1a1a1a')  # Slightly lighter black for headers
NOTES_LINE_COLOR = HexColor('#2a2a2a')  # Very dark gray for notes lines

# Year base colors (each year has its own color family)
YEAR_BASE_COLORS = [
    HexColor('#8B4566'),  # 2020 - Red/Pink family
    HexColor('#A87632'),  # 2021 - Orange/Brown family
    HexColor('#8B8B3A'),  # 2022 - Yellow/Gold family
    HexColor('#5A7A6A'),  # 2023 - Green family
    HexColor('#5A6A8B'),  # 2024 - Blue family
]


def generate_month_shades(base_color, num_shades=12):
    """Generate shades of a base color for month tabs"""
    # Extract RGB from base color
    hex_val = base_color.hexval()[2:]  # Remove '0x' prefix
    r = int(hex_val[0:2], 16)
    g = int(hex_val[2:4], 16)
    b = int(hex_val[4:6], 16)

    shades = []
    for i in range(num_shades):
        # Create variations by adjusting brightness with more dramatic difference
        # Vary from 0.5 to 1.6 of base color for better distinction
        factor = 0.5 + (i / (num_shades - 1)) * 1.1
        new_r = min(255, max(30, int(r * factor)))  # Keep minimum at 30 to stay visible
        new_g = min(255, max(30, int(g * factor)))
        new_b = min(255, max(30, int(b * factor)))
        shades.append(HexColor(f'#{new_r:02x}{new_g:02x}{new_b:02x}'))

    return shades


# Generate month colors for each year (each year's months are shades of that year's base color)
YEAR_MONTH_COLORS = {}
for idx, year in enumerate(YEARS):
    YEAR_MONTH_COLORS[year] = generate_month_shades(YEAR_BASE_COLORS[idx])


def create_calendar_pdf(filename='goodnotes_calendar_2020_2024.pdf'):
    """Generate the complete calendar PDF with navigation tabs"""

    c = canvas.Canvas(filename, pagesize=letter)

    # Calculate page destinations for linking
    page_index = 0
    page_destinations = {}

    # Create destination names for each page
    for year in YEARS:
        for month in MONTHS:
            dest_name = f"page_{year}_{month}"
            page_destinations[(year, month)] = dest_name

    # Generate cover page first
    draw_cover_page(c)
    c.showPage()
    page_index += 1

    # Generate all month pages
    for year in YEARS:
        for month in MONTHS:
            page_index += 1
            draw_month_page(c, year, month, page_destinations)
            c.showPage()

    c.save()
    print(f"Calendar PDF generated: {filename}")
    print(f"Total pages: {page_index}")


def draw_cover_page(c):
    """Draw the elegant cover page with proper typography and spacing"""
    import math

    # Set background to black
    c.setFillColor(BG_COLOR)
    c.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, fill=True, stroke=False)

    # Refined gold color - more luxurious
    gold_color = HexColor('#C9A961')  # Softer, more refined gold

    # Center of page
    center_x = PAGE_WIDTH / 2
    center_y = PAGE_HEIGHT / 2

    # Draw elegant decorative line at top
    c.setStrokeColor(gold_color)
    c.setLineWidth(1.5)
    line_width = 2.5 * inch
    c.line(center_x - line_width/2, PAGE_HEIGHT - 1.5*inch,
           center_x + line_width/2, PAGE_HEIGHT - 1.5*inch)

    # Draw "NINO YAP CUGTAS" straight above - in gold with letter spacing
    c.setFillColor(gold_color)
    c.setFont("Helvetica", 16)
    name_text = "N I N O  Y A P  C U G T A S"  # Add letter spacing
    text_width = c.stringWidth(name_text, "Helvetica", 16)
    c.drawString(center_x - text_width / 2, center_y + 100, name_text)

    # Draw main heading "5 YEAR CALENDAR" - with proper spacing
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 48)

    # Split into two lines for better hierarchy
    main_text_1 = "5 YEAR"
    main_text_2 = "CALENDAR"

    text_width_1 = c.stringWidth(main_text_1, "Helvetica-Bold", 48)
    text_width_2 = c.stringWidth(main_text_2, "Helvetica-Bold", 48)

    # Draw with proper spacing
    c.drawString(center_x - text_width_1 / 2, center_y + 15, main_text_1)
    c.drawString(center_x - text_width_2 / 2, center_y - 35, main_text_2)

    # Draw decorative dots on either side of main text
    dot_radius = 3
    dot_offset = max(text_width_1, text_width_2) / 2 + 30
    c.setFillColor(gold_color)
    c.circle(center_x - dot_offset, center_y - 10, dot_radius, fill=True, stroke=False)
    c.circle(center_x + dot_offset, center_y - 10, dot_radius, fill=True, stroke=False)

    # Draw "2020-2024" below - in gold with letter spacing
    c.setFont("Helvetica", 16)
    year_range = "2 0 2 0  -  2 0 2 4"  # Add letter spacing
    text_width = c.stringWidth(year_range, "Helvetica", 16)
    c.drawString(center_x - text_width / 2, center_y - 100, year_range)

    # Draw elegant decorative line at bottom
    c.setStrokeColor(gold_color)
    c.setLineWidth(1.5)
    c.line(center_x - line_width/2, 1.5*inch,
           center_x + line_width/2, 1.5*inch)

    # Add small decorative flourish in center bottom
    flourish_y = 1.2 * inch
    c.setLineWidth(0.5)
    c.line(center_x - 15, flourish_y, center_x + 15, flourish_y)
    c.circle(center_x - 15, flourish_y, 2, fill=True, stroke=False)
    c.circle(center_x + 15, flourish_y, 2, fill=True, stroke=False)
    c.circle(center_x, flourish_y, 3, fill=True, stroke=False)


def draw_month_page(c, year, month, page_destinations):
    """Draw a single month page with calendar and navigation tabs"""

    # Set background to black
    c.setFillColor(BG_COLOR)
    c.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, fill=True, stroke=False)

    # Create bookmark destination for this page
    dest_name = page_destinations[(year, month)]
    c.bookmarkPage(dest_name)

    # Draw navigation tabs on the right side
    draw_navigation_tabs(c, year, month, page_destinations)

    # Draw the calendar grid
    draw_calendar_grid(c, year, month)


def draw_navigation_tabs(c, year, month, page_destinations):
    """Draw clickable navigation tabs on the right side with vertical text"""

    # Uniform tab dimensions - fill entire page height with no gaps
    total_tabs = 17  # 5 year tabs + 12 month tabs
    uniform_tab_height = PAGE_HEIGHT / total_tabs
    start_x = PAGE_WIDTH - TAB_WIDTH  # Flush with right edge

    # Year tabs (top 5) - uniform height, no spacing
    for idx, yr in enumerate(YEARS):
        y_pos = PAGE_HEIGHT - ((idx + 1) * uniform_tab_height)

        # Draw year tab
        c.setFillColor(YEAR_BASE_COLORS[idx])
        c.rect(start_x, y_pos, TAB_WIDTH, uniform_tab_height, fill=True, stroke=False)

        # Add vertical year text (reading top to bottom)
        c.saveState()
        c.setFillColor(white)
        c.setFont("Helvetica-Bold", 11)
        # Rotate and position text vertically in the center of the tab
        text_x = start_x + TAB_WIDTH / 2 - 3
        text_y = y_pos + uniform_tab_height / 2
        c.translate(text_x, text_y)
        c.rotate(270)  # 270 degrees for top-to-bottom reading
        text_width = c.stringWidth(str(yr), "Helvetica-Bold", 11)
        c.drawString(-text_width / 2, 0, str(yr))
        c.restoreState()

        # Make it clickable - link to January of that year
        dest = page_destinations[(yr, 1)]
        c.linkRect(dest, dest, (start_x, y_pos, start_x + TAB_WIDTH, y_pos + uniform_tab_height), relative=0)

    # Month tabs (below year tabs) - uniform height, no spacing
    year_idx = YEARS.index(year)
    month_colors = YEAR_MONTH_COLORS[year]

    for idx, mn in enumerate(MONTHS):
        tab_index = 5 + idx  # Start after the 5 year tabs
        y_pos = PAGE_HEIGHT - ((tab_index + 1) * uniform_tab_height)

        # Highlight current month with full brightness, others dimmed
        if mn == month:
            c.setFillColor(month_colors[idx])
        else:
            # Dimmer version for non-current months
            color = month_colors[idx]
            hex_val = color.hexval()[2:]
            r = int(hex_val[0:2], 16)
            g = int(hex_val[2:4], 16)
            b = int(hex_val[4:6], 16)
            c.setFillColor(HexColor(f'#{int(r*0.4):02x}{int(g*0.4):02x}{int(b*0.4):02x}'))

        c.rect(start_x, y_pos, TAB_WIDTH, uniform_tab_height, fill=True, stroke=False)

        # Add vertical month text (reading top to bottom)
        c.saveState()
        c.setFillColor(white)
        c.setFont("Helvetica-Bold", 8)
        # Rotate and position text vertically in the center of the tab
        text_x = start_x + TAB_WIDTH / 2 - 2
        text_y = y_pos + uniform_tab_height / 2
        c.translate(text_x, text_y)
        c.rotate(270)  # 270 degrees for top-to-bottom reading
        text_width = c.stringWidth(MONTH_NAMES[idx], "Helvetica-Bold", 8)
        c.drawString(-text_width / 2, 0, MONTH_NAMES[idx])
        c.restoreState()

        # Make it clickable - link to this month in current year
        dest = page_destinations[(year, mn)]
        c.linkRect(dest, dest, (start_x, y_pos, start_x + TAB_WIDTH, y_pos + uniform_tab_height), relative=0)


def draw_calendar_grid(c, year, month):
    """Draw the monthly calendar grid"""

    # Calendar area dimensions - with margin on right side too
    cal_left = MARGIN
    cal_right = PAGE_WIDTH - TAB_WIDTH - MARGIN  # Add margin between calendar and tabs
    cal_top = PAGE_HEIGHT - MARGIN
    cal_bottom = MARGIN

    cal_width = cal_right - cal_left

    # Notes section height
    notes_height = 1.8 * inch
    notes_top = cal_bottom + notes_height

    # Month/Year header - more compact
    month_name = calendar.month_name[month].upper()
    header_text = f"{month_name} {year}"

    c.setFillColor(TEXT_COLOR)
    c.setFont("Helvetica-Bold", 18)
    text_width = c.stringWidth(header_text, "Helvetica-Bold", 18)
    c.drawString(cal_left + (cal_width - text_width) / 2, cal_top - 30, header_text)

    # Day of week headers - more compact
    day_names = ['SUN', 'MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT']
    header_y = cal_top - 50
    col_width = cal_width / 7

    c.setFont("Helvetica-Bold", 10)
    for i, day_name in enumerate(day_names):
        x_pos = cal_left + (i * col_width)

        # Draw header background
        c.setFillColor(HEADER_COLOR)
        c.rect(x_pos, header_y - 20, col_width, 20, fill=True, stroke=False)

        # Draw day name
        c.setFillColor(TEXT_COLOR)
        text_width = c.stringWidth(day_name, "Helvetica-Bold", 10)
        c.drawString(x_pos + (col_width - text_width) / 2, header_y - 14, day_name)

    # Calendar grid
    grid_top = header_y - 20
    grid_bottom = notes_top  # Calendar ends where notes begin
    row_height = (grid_top - grid_bottom) / 6  # 6 rows for weeks

    # Get calendar data - set first day of week to Sunday (6)
    # Python's calendar module uses Monday (0) as default, but we display Sunday first
    cal_obj = calendar.Calendar(firstweekday=calendar.SUNDAY)
    cal = cal_obj.monthdayscalendar(year, month)

    # Draw grid and dates
    c.setStrokeColor(GRID_COLOR)
    c.setLineWidth(0.5)

    for week_num, week in enumerate(cal):
        for day_num, day in enumerate(week):
            x_pos = cal_left + (day_num * col_width)
            y_pos = grid_top - ((week_num + 1) * row_height)

            # Draw cell border
            c.rect(x_pos, y_pos, col_width, row_height, fill=False, stroke=True)

            # Draw day number if it exists
            if day != 0:
                c.setFillColor(TEXT_COLOR)
                c.setFont("Helvetica", 12)
                c.drawString(x_pos + 5, y_pos + row_height - 18, str(day))

    # Draw notes section at bottom
    draw_notes_section(c, cal_left, cal_right, cal_bottom, notes_top)


def draw_notes_section(c, left, right, bottom, top):
    """Draw lined notes section at the bottom of the page"""

    # Draw notes box border
    c.setStrokeColor(GRID_COLOR)
    c.setLineWidth(1)
    c.rect(left, bottom, right - left, top - bottom, fill=False, stroke=True)

    # Draw "NOTES" label
    c.setFillColor(TEXT_COLOR)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(left + 10, top - 20, "NOTES")

    # Draw horizontal lines for writing
    c.setStrokeColor(NOTES_LINE_COLOR)
    c.setLineWidth(0.5)

    line_spacing = 0.25 * inch
    current_y = top - 35

    while current_y > bottom + 10:
        c.line(left + 5, current_y, right - 5, current_y)
        current_y -= line_spacing


if __name__ == "__main__":
    print("Generating Goodnotes Calendar (2020-2024)...")
    print("This may take a moment...")
    create_calendar_pdf()
    print("Done! Import the PDF into Goodnotes and enjoy your calendar!")
