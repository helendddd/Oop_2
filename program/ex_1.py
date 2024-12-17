# Реализовать внешнюю функцию с именем make_тип() , где тип — тип реализуемой
# структуры. Функция должна получать в качестве аргументов значения для полей
# структуры и возвращать структуру требуемого типа. При передаче ошибочных
# параметров следует выводить сообщение и заканчивать работу.
# Элемент геометрической прогрессии вычисляется по формуле:
# aj = a0* r^j, j = 0, 1, 2,...
# Поле first — дробное число, первый элемент прогрессии а ;
# поле second — постоянное отношение.
# Определить метод для вычисления заданного элемента прогрессии.

# Выполнить индивидуальное задание 1 лабораторной работы 4.1, максимально
# задействовав имеющиеся в Python средства перегрузки операторов.

# !/usr/bin/env python3
# -*- coding: utf-8 -*-


class GeometricProgression:
    """
    Класс для представления геометрической прогрессии.
    Поле first — первый элемент прогрессии (a0).
    Поле second — постоянное отношение (r).
    """

    def __init__(self, first=1.0, second=1.0):
        """
        Инициализация первого элемента и постоянного отношения.
        """
        if not isinstance(first, (int, float)):
            raise ValueError("Первый элемент прогрессии должен быть числом.")
        if not isinstance(second, (int, float)):
            raise ValueError("Постоянное отношение должно быть числом.")

        self.first = float(first)
        self.second = float(second)

    def __getitem__(self, j):
        """
        Получение j-го элемента прогрессии через оператор [].
        """
        if not isinstance(j, int) or j < 0:
            raise ValueError("Индекс должен быть положительным целым числом.")
        return self.first * (self.second**j)

    def __mul__(self, scalar):
        """
        Умножение прогрессии на скаляр через оператор *.
        Возвращает новую прогрессию.
        """
        if not isinstance(scalar, (int, float)):
            raise ValueError("Множитель должен быть числом.")
        return GeometricProgression(self.first * scalar, self.second * scalar)

    def __eq__(self, other):
        """
        Проверка равенства двух прогрессий через оператор ==.
        """
        if not isinstance(other, GeometricProgression):
            return False
        return self.first == other.first and self.second == other.second

    def __str__(self):
        """
        Возвращает строковое представление прогрессии.
        """
        return f"1 элемент: {self.first}, Постоянное отношение: {self.second}"

    def read(self):
        """
        Чтение значений для первого элемента и отношения с клавиатуры.
        """
        self.first = float(input("Введите первый элемент прогрессии (a0): "))
        self.second = float(input("Введите постоянное отношение (r): "))

    def display(self):
        """
        Вывод данных о прогрессии и вычисление j-го элемента.
        """
        print(self)
        j = int(input("Введите номер элемента прогрессии для вычисления: "))
        if not isinstance(j, int) or j < 0:
            raise ValueError("Индекс должен быть положительным целым числом.")
        print(f"{j}-й элемент прогрессии: {self[j]}")


def make_geometric_progression(first, second):
    """
    Внешняя функция для создания объекта GeometricProgression.
    """
    try:
        return GeometricProgression(first, second)
    except ValueError as e:
        print(f"Ошибка: {e}")
        exit(1)


if __name__ == "__main__":
    # Создание первого объекта прогрессии
    gp1 = GeometricProgression(2, 3)
    gp1.display()

    # Ввод значений для второго объекта с клавиатуры
    gp2 = GeometricProgression()
    gp2.read()
    gp2.display()

    # Сравнение прогрессий
    print("Прогрессии равны?", gp1 == gp2)

    # Умножение прогрессии на скаляр
    gp3 = gp1 * 2
    print("Новая прогрессия после умножения:", gp3)
