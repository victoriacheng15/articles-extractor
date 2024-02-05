def check_existing_header(sheet, header):
    existing_header = sheet.row_values(1)
    if existing_header != header:
        sheet.append_row(header)


def get_all_titles(sheet):
    data = sheet.get_all_values()[1:]
    return tuple(row[1] for row in data)