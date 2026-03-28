CATEGORIES = {
    'Images': ['.jpeg', '.jpg', '.png', '.gif', '.bmp'],
    'Documents': ['.pdf', '.doc', '.docx', '.txt', '.xls'],
    'Spreadsheets': ['.xls', '.xlsx'],
    'Audio': ['.mp3', '.wav', '.aac'],
    'Video': ['.mp4', '.mkv', '.avi'],
    'Archives': ['.zip', '.rar', '.tar', '.gz'],
    'Code': ['.py', '.java', '.js', '.cpp'],
    'Presentations': ['.ppt', '.pptx'],
    'Executables': ['.exe', '.bat'],
    'Others': []
}

class FileClassifier:
    def classify(self, filename):
        extension = filename.rsplit('.', 1)[-1].lower() if '.' in filename else ''
        for category, extensions in CATEGORIES.items():
            if f'.{extension}' in extensions:
                return category
        return 'Others'