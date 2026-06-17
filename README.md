# Классические шифры и криптоанализ

Интерактивное приложение для шифрования, дешифрования и криптоанализа классических шифров.

## Поддерживаемые алгоритмы
- Шифр Цезаря
- Шифр Виженера
- Шифр Полибия

## Скачать
- [Windows](https://github.com/ltwworker/classic-ciphers/releases/latest/download/CipherApp-windows.exe)
- [Linux](https://github.com/ltwworker/classic-ciphers/releases/latest/download/CipherApp-linux)
- [macOS](https://github.com/ltwworker/classic-ciphers/releases/latest/download/CipherApp-macos)

## Как запустить

**Windows**  
Скачайте файл `CipherApp-windows.exe` и запустите двойным щелчком.

**Linux**  
Скачайте файл `CipherApp-linux`, откройте терминал в папке со скачанным файлом, выполните команду `chmod +x CipherApp-linux`, затем запустите командой `./CipherApp-linux`.

**macOS**  
Скачайте файл `CipherApp-macos`, откройте терминал в папке со скачанным файлом, выполните команду `chmod +x CipherApp-macos`, затем запустите командой `./CipherApp-macos`. Если macOS блокирует запуск, выполните в терминале команду `xattr -d com.apple.quarantine ./CipherApp-macos`.

## Запуск из исходников
```bash
git clone https://github.com/ltwworker/classic-ciphers.git
cd classic-ciphers
python3 main.py
