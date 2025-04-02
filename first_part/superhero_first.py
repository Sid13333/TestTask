import requests


def get_tallest_hero(gender, has_work):
    """
    Функция для поиска самого высокого супергероя по заданным критериям.

    :param gender: Пол героя ('Male', 'Female' и т.д.)
    :param has_work: Булево значение, указывающее, должен ли герой иметь работу
    :return: Кортеж (имя, рост) самого высокого героя или None, если не найдено
    """
    try:
        response = requests.get('https://akabab.github.io/superhero-api/api/all.json')
        response.raise_for_status()
        heroes = response.json()
    except requests.RequestException as e:
        print(f"Ошибка при получении данных: {e}")
        return None

    filtered_heroes = []

    for hero in heroes:
        if not all(key in hero for key in ['name', 'appearance']):
            continue

        appearance = hero['appearance']
        if not all(key in appearance for key in ['gender', 'height']):
            continue

        if appearance['gender'].lower() != gender.lower():
            continue

        work_condition = ('work' in hero and 'occupation' in hero['work']) if has_work else True
        if not work_condition:
            continue

        height_str = appearance['height'][0] if isinstance(appearance['height'], list) else appearance['height']

        try:
            height = float(''.join(filter(str.isdigit, str(height_str))))
        except (ValueError, TypeError):
            continue

        filtered_heroes.append((hero['name'], height))

    return max(filtered_heroes, key=lambda x: x[1]) if filtered_heroes else None


if __name__ == '__main__':
    print("Самый высокий мужчина-супергерой с работой:")
    print(get_tallest_hero("Male", True))

    print("\nСамая высокая женщина-супергерой без работы:")
    print(get_tallest_hero("Female", False))