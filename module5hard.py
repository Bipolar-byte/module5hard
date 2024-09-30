import hashlib
import time
from datetime import datetime


class User:
    def __init__(self, nickname, password, birthdate):
        self.nickname = nickname
        self.password = self._hash_password(password)
        self.age = self._calculate_age(birthdate)

    def _hash_password(self, password):
        return int(hashlib.sha256(password.encode()).hexdigest(), 16)

    def _calculate_age(self, birthdate):
        birth_date = datetime.strptime(birthdate, '%d.%m.%Y')
        today = datetime.today()
        return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))


class Video:
    def __init__(self, title, duration, adult_mode=False):
        self.title = title
        self.duration = duration
        self.time_now = 0
        self.adult_mode = adult_mode


class UrTube:
    def __init__(self):
        self.users = []
        self.videos = []
        self.current_user = None
        self.search_results = []

    def log_in(self, nickname, password):
        hashed_password = int(hashlib.sha256(password.encode()).hexdigest(), 16)
        for user in self.users:
            if user.nickname == nickname and user.password == hashed_password:
                self.current_user = user
                print(f"Пользователь {nickname} успешно вошел.")
                return True
        print("Неверные данные для входа.")
        return False

    def register(self, nickname, password, birthdate):
        for user in self.users:
            if user.nickname == nickname:
                print(f"Пользователь {nickname} уже существует")
                return False
        new_user = User(nickname, password, birthdate)
        self.users.append(new_user)
        self.current_user = new_user
        print(f"Пользователь {nickname} зарегистрирован и вошел в систему.")
        return True

    def log_out(self):
        self.current_user = None
        self.search_results = []
        print("Пользователь вышел из системы.")

    def add(self, *videos):
        for video in videos:
            if not any(v.title == video.title for v in self.videos):
                self.videos.append(video)
                print(f"Видео '{video.title}' добавлено.")
            else:
                print(f"Видео '{video.title}' уже существует.")

    def get_videos(self, search_term):
        search_term_lower = search_term.lower()
        self.search_results = [video for video in self.videos if search_term_lower in video.title.lower()]
        return [video.title for video in self.search_results]

    def watch_video(self, title):
        if self.current_user is None:
            print("Войдите в аккаунт, чтобы смотреть видео")
            return

        for video in self.search_results:
            if video.title == title:
                if video.adult_mode and self.current_user.age < 18:
                    print("Вам нет 18 лет, пожалуйста покиньте страницу")
                    return

                print(f"Начинается просмотр видео: {video.title}")
                for second in range(video.time_now, video.duration):
                    time.sleep(1)
                    print(f"Воспроизведение: {second + 1} сек.")
                video.time_now = 0
                print("Конец видео")
                return

        print(f"Видео с названием '{title}' не найдено среди результатов поиска.")


ur = UrTube()


def main():
    logged_in = False
    while True:
        if not ur.current_user:
            print("\nДоступные команды:")
            print("1. Зарегистрироваться")
            print("2. Войти в систему")
            print("3. Выйти из программы")
            choice = input("Введите номер команды: ")

            if choice == '1':
                nickname = input("Введите никнейм: ")
                password = input("Введите пароль: ")
                birthdate = input("Введите дату рождения (ДД.ММ.ГГГГ): ")
                if ur.register(nickname, password, birthdate):
                    logged_in = True

            elif choice == '2':
                nickname = input("Введите никнейм: ")
                password = input("Введите пароль: ")
                if ur.log_in(nickname, password):
                    logged_in = True

            elif choice == '3':
                print("Программа завершена.")
                break

            else:
                print("Неверная команда, попробуйте снова.")


        else:
            print("\nДоступные команды:")
            print("1. Выйти из системы")
            print("2. Добавить видео")
            print("3. Найти видео")
            print("4. Смотреть видео")
            print("5. Выйти из программы")

            choice = input("Введите номер команды: ")

            if choice == '1':
                ur.log_out()
                logged_in = False

            elif choice == '2':
                title = input("Введите название видео: ")
                duration = int(input("Введите продолжительность видео в секундах: "))
                adult_mode = input("Видео с ограничением 18+? (да/нет): ").lower() == 'да'
                video = Video(title, duration, adult_mode)
                ur.add(video)

            elif choice == '3':
                search_term = input("Введите поисковое слово: ")
                results = ur.get_videos(search_term)
                print("Найденные видео:", results)

            elif choice == '4':
                if ur.search_results:
                    title = input("Введите название видео для просмотра: ")
                    ur.watch_video(title)
                else:
                    print("Сначала выполните поиск видео.")

            elif choice == '5':
                print("Программа завершена.")
                break

            else:
                print("Неверная команда, попробуйте снова.")


if __name__ == "__main__":
    main()

# внес небольшие изменения в код P.S. (Это мой внутрений перфекционист)
