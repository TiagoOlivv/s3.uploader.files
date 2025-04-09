def check_all_fields_filled(self):
    all_filled = all(field.text().strip() for field in self.inputs) and self.folder_path
    self.upload_button.setEnabled(bool(all_filled))
