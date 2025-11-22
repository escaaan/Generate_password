import secrets
import string
import pyperclip
import os

class PasswordGenerator:
    def __init__(self):
        self.strength_levels = {
            'weak': (8, False, False),
            'medium': (12, True, False),
            'strong': (16, True, True),
            'very_strong': (20, True, True)
        }

    def generate_secure_password(self, length=16, use_digits=True, use_special=True):
        """Генерация криптографически безопасного пароля"""
        characters = string.ascii_letters

        if use_digits:
            characters += string.digits
        if use_special:
            characters += string.punctuation

        password = []

        if use_digits:
            password.append(secrets.choice(string.digits))
        if use_special:
            password.append(secrets.choice(string.punctuation))

        # Заполняем оставшуюся длину
        remaining = length - len(password)
        if remaining > 0:
            password.extend(secrets.choice(characters) for _ in range(remaining))

        # перемешиваем
        secrets.SystemRandom().shuffle(password)

        return ''.join(password)

    def generate_multiple_passwords(self, count=5, **kwargs):
        """Генерация нескольких паролей"""
        return [self.generate_secure_password(**kwargs) for _ in range(count)]

    def calculate_strength(self, password):
        """Оценка сложности пароля"""
        score = 0
        if any(c.islower() for c in password):
            score += 1
        if any(c.isupper() for c in password):
            score += 1
        if any(c.isdigit() for c in password):
            score += 1
        if any(c in string.punctuation for c in password):
            score += 1
        if len(password) >= 12:
            score += 1
        if len(password) >= 16:
            score += 1

        strength_map = {
            1: "Очень слабый",
            2: "Слабый",
            3: "Средний",
            4: "Хороший",
            5: "Сильный",
            6: "Очень сильный"
        }
        return strength_map.get(score, "Очень слабый")

    def save_passwords(self, passwords, filename="passwords.txt"):
        """Сохранение паролей в файл"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                for i, pwd in enumerate(passwords, 1):
                    strength = self.calculate_strength(pwd)
                    f.write(f"{i}. {pwd} | Длина: {len(pwd)} | Сложность: {strength}\n")
            return True
        except Exception as e:
            return False

class PasswordManager:
    def __init__(self):
        self.generator = PasswordGenerator()
        self.saved_passwords_file = "saved_passwords.json"

    def clear_screen(self):
        """Очистка экрана консоли"""
        os.system('cls' if os.name == 'nt' else 'clear')

    def display_banner(self):
        """Отображение заголовка"""
        banner = """
╔══════════════════════════════════════════════╗
║           ГЕНЕРАТОР БЕЗОПАСНЫХ ПАРОЛЕЙ       ║
║                CryptoPass v1.0               ║
╚══════════════════════════════════════════════╝
        """
        print(banner)

    def get_user_choice(self):
        """Получение выбора пользователя"""
        menu = """
1. Сгенерировать один пароль
2. Сгенерировать несколько паролей  
3. Пароли по уровню сложности
4. Сохранить пароли в файл
5. Выход

Выберите действие (1-5): """

        while True:
            try:
                choice = int(input(menu).strip())
                if 1 <= choice <= 5:
                    return choice
                else:
                    print("❌ Пожалуйста, введите число от 1 до 5")
            except ValueError:
                print("❌ Введите корректное число!")

    def get_password_settings(self):
        """Получение настроек генерации от пользователя"""
        print("\n⚙️  Настройки генерации пароля:")

        while True:
            try:
                length = int(input("Длина пароля (8-50): "))
                if 8 <= length <= 50:
                    break
                else:
                    print("❌ Длина должна быть от 8 до 50 символов")
            except ValueError:
                print("❌ Введите число!")

        use_digits = input("Использовать цифры? (y/n): ").lower().strip() == 'y'
        use_special = input("Использовать спецсимволы? (y/n): ").lower().strip() == 'y'

        return length, use_digits, use_special

    def generate_single_password(self):
        """Генерация одного пароля"""
        length, use_digits, use_special = self.get_password_settings()
        password = self.generator.generate_secure_password(length, use_digits, use_special)
        strength = self.generator.calculate_strength(password)

        print(f"\n✅ Сгенерирован пароль:")
        print(f"🔐 {password}")
        print(f"📊 Длина: {len(password)} | Сложность: {strength}")

        # Предлагаем скопировать в буфер обмена
        try:
            if input("\n📋 Скопировать в буфер обмена? (y/n): ").lower() == 'y':
                pyperclip.copy(password)
                print("✅ Пароль скопирован в буфер обмена!")
        except:
            print("⚠️  Не удалось скопировать в буфер обмена")

    def generate_multiple_passwords(self):
        """Генерация нескольких паролей"""
        while True:
            try:
                count = int(input("Сколько паролей сгенерировать? (1-20): "))
                if 1 <= count <= 20:
                    break
                else:
                    print("❌ Введите число от 1 до 20")
            except ValueError:
                print("❌ Введите число!")

        length, use_digits, use_special = self.get_password_settings()
        passwords = self.generator.generate_multiple_passwords(count, length=length,
                                                               use_digits=use_digits,
                                                               use_special=use_special)

        print(f"\n✅ Сгенерировано {count} паролей:")
        for i, pwd in enumerate(passwords, 1):
            strength = self.generator.calculate_strength(pwd)
            print(f"{i:2d}. {pwd} | Сложность: {strength}")

        # Предлагаем сохранить в файл
        if input("\n💾 Сохранить в файл? (y/n): ").lower() == 'y':
            filename = input("Имя файла (по умолчанию: passwords.txt): ").strip() or "passwords.txt"
            if self.generator.save_passwords(passwords, filename):
                print(f"✅ Пароли сохранены в {filename}")
            else:
                print("❌ Ошибка при сохранении файла")

    def generate_by_strength(self):
        """Генерация паролей по уровню сложности"""
        print("\n🎯 Выберите уровень сложности:")
        print("1. Слабый (8 символов, только буквы)")
        print("2. Средний (12 символов, буквы + цифры)")
        print("3. Сильный (16 символов, все символы)")
        print("4. Очень сильный (20 символов, все символы)")

        while True:
            try:
                choice = int(input("Ваш выбор (1-4): "))
                if 1 <= choice <= 4:
                    break
                else:
                    print("❌ Введите число от 1 до 4")
            except ValueError:
                print("❌ Введите число!")

        strength_map = {1: 'weak', 2: 'medium', 3: 'strong', 4: 'very_strong'}
        level = strength_map[choice]
        length, use_digits, use_special = self.generator.strength_levels[level]

        count = 1
        if input("Сгенерировать несколько паролей? (y/n): ").lower() == 'y':
            while True:
                try:
                    count = int(input("Сколько паролей? (1-10): "))
                    if 1 <= count <= 10:
                        break
                    else:
                        print("❌ Введите число от 1 до 10")
                except ValueError:
                    print("❌ Введите число!")

        passwords = self.generator.generate_multiple_passwords(count, length=length,
                                                               use_digits=use_digits,
                                                               use_special=use_special)

        print(f"\n✅ Пароли уровня '{level}':")
        for i, pwd in enumerate(passwords, 1):
            strength = self.generator.calculate_strength(pwd)
            print(f"{i:2d}. {pwd}       | Сложность: {strength}")

def main():
    app = PasswordManager()

    while True:
        app.clear_screen()
        app.display_banner()

        choice = app.get_user_choice()

        if choice == 1:
            app.generate_single_password()
        elif choice == 2:
            app.generate_multiple_passwords()
        elif choice == 3:
            app.generate_by_strength()
        elif choice == 4:
            # Здесь можно добавить функционал сохранения
            print("\nℹ️  Эта функция доступна при генерации паролей")
        elif choice == 5:
            print("\n👋 До свидания! Берегите свои пароли!")
            break

        input("\n↵ Нажмите Enter для продолжения...")
main()
'''
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Программа прервана пользователем")
    except Exception as e:
        print(f"\n❌ Произошла ошибка: {e}")'''