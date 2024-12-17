# Одна запись в списке запланированных дел представляет собой словарь
# DailyItem, которая содержит время начала и окончания работы, описание
# и признак выполнения. Реализовать класс DailySchedule, представляющий собой
# план работ на день. Реализовать методы добавления, удаления и изменения
# планируемой работы. При добавлении проверять корректность временных рамок
# (они не должны пересекаться с уже запланированными мероприятиями).
# Реализовать метод поиска свободного промежутка времени. Условие поиска
# задает размер искомого интервала, а также временные рамки, в которые он
# должен попадать. Метод поиска возвращает словарь Dailyltern с пустым
# описанием вида работ. Реализовать операцию генерации объекта Redo (еще раз),
# содержащего список дел, не выполненных в течение дня,
# из объекта типа DailySchedule.

# !/usr/bin/env python3
# -*- coding: utf-8 -*-


from datetime import datetime, time, timedelta


class DailyItem:
    def __init__(
        self,
        start_time: time,
        end_time: time,
        description: str,
        is_done: bool = False,
    ):
        self.start_time = start_time
        self.end_time = end_time
        self.description = description
        self.is_done = is_done

    def __repr__(self):
        status = "Done" if self.is_done else "Pending"
        return (
            f"Task('{self.description}', {self.start_time} - "
            f"{self.end_time}, {status})"
        )


class DailySchedule:
    def __init__(self):
        self.schedule = []

    def add_task(self, start_time: time, end_time: time, description: str):
        """Добавление задачи с проверкой на пересечения"""
        new_task = DailyItem(start_time, end_time, description)
        if self._is_time_slot_free(start_time, end_time):
            self.schedule.append(new_task)
            self.schedule.sort(key=lambda task: task.start_time)
            print(f"Added: {new_task}")
        else:
            print("Error: Time slot is already taken.")

    def remove_task(self, description: str):
        """Удаление задачи по описанию"""
        self.schedule = [
            task for task in self.schedule if task.description != description
        ]

    def modify_task(
        self,
        description: str,
        new_start: time = None,
        new_end: time = None,
        new_description: str = None,
    ):
        """Изменение задачи"""
        for task in self.schedule:
            if task.description == description:
                if (
                    new_start
                    and new_end
                    and self._is_time_slot_free(
                        new_start, new_end, exclude_task=task
                    )
                ):
                    task.start_time = new_start
                    task.end_time = new_end
                if new_description:
                    task.description = new_description
                break

    def mark_task_as_done(self, description: str):
        """Отметить задачу как выполненную"""
        for task in self.schedule:
            if task.description == description:
                task.is_done = True
                print(f"Marked as done: {task}")
                break

    def _is_time_slot_free(
        self, start_time: time, end_time: time, exclude_task: DailyItem = None
    ) -> bool:
        """Проверка, свободен ли временной слот"""
        for task in self.schedule:
            if task == exclude_task:
                continue
            if end_time > task.start_time and start_time < task.end_time:
                return False
        return True

    def find_free_slot(
        self, required_duration: timedelta, start_bound: time, end_bound: time
    ) -> DailyItem:
        """Поиск свободного промежутка времени"""
        # Преобразуем time в datetime для удобства вычислений
        start_datetime = datetime.combine(datetime.today(), start_bound)
        end_datetime = datetime.combine(datetime.today(), end_bound)

        current_time = start_datetime

        # Проверка промежутков между задачами
        for task in self.schedule:
            task_start = datetime.combine(datetime.today(), task.start_time)
            task_end = datetime.combine(datetime.today(), task.end_time)

            if current_time + required_duration <= task_start:
                # Нашли свободный интервал
                free_start = current_time
                free_end = current_time + required_duration
                return DailyItem(free_start.time(), free_end.time(), "")

            current_time = task_end

        # Проверка после последней задачи
        if current_time + required_duration <= end_datetime:
            free_start = current_time
            free_end = current_time + required_duration
            return DailyItem(free_start.time(), free_end.time(), "")

        return None  # Если не нашли подходящий интервал

    def generate_redo_list(self):
        """Генерация списка невыполненных задач"""
        redo_list = DailySchedule()
        for task in self.schedule:
            if not task.is_done:
                redo_list.add_task(
                    task.start_time, task.end_time, task.description
                )
        return redo_list

    def __repr__(self):
        return "\n".join([str(task) for task in self.schedule])


# Пример использования
if __name__ == "__main__":
    # Создаем расписание
    schedule = DailySchedule()

    # Добавляем задачи
    schedule.add_task(time(8, 0), time(9, 35), "Математика")
    schedule.add_task(time(9, 40), time(11, 10), "Информатика")
    schedule.add_task(time(11, 20), time(12, 50), "Русский")

    print("\nInitial schedule:")
    print(schedule)

    # Отметим задачу как выполненную
    schedule.mark_task_as_done("Информатика")

    # Поиск свободного времени
    free_slot = schedule.find_free_slot(
        timedelta(minutes=30), time(8, 0), time(14, 0)
    )
    print("\nFound free slot:")
    print(free_slot)

    # Генерация списка невыполненных задач
    redo_list = schedule.generate_redo_list()
    print("\nRedo list:")
    print(redo_list)
