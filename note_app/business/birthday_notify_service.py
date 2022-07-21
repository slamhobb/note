import inject

from itertools import groupby

from datetime import date

from note_app.business.birthday_service import BirthdayService
from note_app.business.user_service import UserService

from note_app.telegramapi import send_message


class BirthdayNotifyService:
    birthday_service = inject.attr(BirthdayService)
    user_service = inject.attr(UserService)

    def notify_about_birthday_on_date(self, on_date: date):
        birthdays = self.birthday_service.get_by_month_day(on_date.month, on_date.day)

        if len(birthdays) == 0:
            return

        users = self.user_service.get_all()
        user_by_id = dict([(user.id, user) for user in users])

        for user_id, birthdays in groupby(birthdays, lambda b: b.user_id):
            user = user_by_id.get(user_id, None)
            if user is None or len(user.telegram_id) == 0:
                continue

            names = [birthday.name for birthday in birthdays]

            text = f'Сегодня ДР у {", ".join(names)}'

            send_message(user.telegram_id, text)
