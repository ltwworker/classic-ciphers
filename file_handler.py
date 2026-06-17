def load_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        raise Exception("Файл не найден")
    except UnicodeDecodeError:
        raise Exception("Не удалось прочитать файл. Проверьте кодировку (должна быть UTF-8)")
    except Exception as e:
        raise Exception(f"Ошибка при чтении файла: {str(e)}")


def save_file(filepath, content):
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
    except Exception as e:
        raise Exception(f"Ошибка при сохранении файла: {str(e)}")