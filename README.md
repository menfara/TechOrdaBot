# Руководство пользователя для администратора

## Изменение URL Google Таблиц

Как администратор, вы можете изменить URL Google Таблиц, которые бот использует для оценки NPS IT-школ. Для этого выполните следующие шаги:

1. **Откройте ваш чат с ботом в Telegram**:
   - Убедитесь, что вы находитесь в чате, где можете отправлять сообщения боту.

2. **Отправьте команду для изменения URL Google Таблиц**:
   - Введите следующую команду, заменив `[ссылка на страницу Google Таблицы]` на фактический URL страницы Google Таблицы, которую вы хотите использовать:
     ```
     pass123 [ссылка на страницу Google Таблицы]
     ```
   - Пример:
     ```
     pass123 https://docs.google.com/spreadsheets/d/1abcdEFGHIJklmnopQRSTUVWXyz1234567890/edit#gid=0
     ```

3. **Подтверждение**:
   - Бот обновит свою конфигурацию и начнет использовать новый URL Google Таблиц для получения данных NPS IT-школ.

### Примечания
- Убедитесь, что новый URL Google Таблиц доступен и у вас есть необходимые разрешения для доступа бота к этой таблице.
- **Важно:** Почта бота `google-sheets-reader@astanahubproject.iam.gserviceaccount.com` должна быть добавлена в редакторы этой Google Таблицы.
- **Напоминание:** В разных страницах (вкладках) таблицы разные ссылки, и бот читает данные именно с той страницы, на которую указывает предоставленная ссылка.
- **Обновление данных:** При обновлении ссылки на страницу бот читает BIN и сгенерированный 6-значный ID для IT-школ и связывает их. Эти данные находятся на странице таблицы с двумя колонками: BIN и ID. Если ID какой-то школы было обновлено в таблице с ID, то необходимо передать боту ссылку на страницу с NPS еще раз для обновления локальных ID у бота.

Следуя этим шагам, вы можете легко изменить источник Google Таблиц, используемых ботом для данных NPS.



## ClientStatusSelectionScene

Класс `ClientStatusSelectionScene` используется для предоставления пользователям возможности выбрать статус их обучения. Он наследует от класса `State`.

### Методы

#### `enter`

Метод `enter` вызывается при входе в сцену выбора статуса клиента.

- **Параметры**:
  - `update` (объект `Update`): объект обновления, содержащий данные о событии.
  - `context` (объект `ContextTypes.DEFAULT_TYPE`): объект контекста, содержащий данные о текущем состоянии бота.

- **Основные моменты**:
  - **Сообщение при входе**:
    Создание и отправка сообщения пользователю с предложением выбрать статус:
    ```python
    message = escape_markdown(Translations.status_prompt[self.language])
    message = message.replace('\<b\>', '*').replace('\</b\>', '*')

    await update.callback_query.message.reply_text(message,
                                                   reply_markup=reply_markup, parse_mode='MarkdownV2')
    ```
  - **Вывод клавиатуры**:
    Создание клавиатуры с кнопками для выбора статуса:
    ```python
    keyboard = [
        [
            InlineKeyboardButton(Translations.status_not_started[self.language], callback_data=self.STATUS_NOT_STARTED),
        ],
        [
            InlineKeyboardButton(Translations.status_teaching[self.language], callback_data=self.STATUS_TEACHING),
        ],
        [
            InlineKeyboardButton(Translations.status_finished[self.language], callback_data=self.STATUS_FINISHED)
        ],
        [
            InlineKeyboardButton(Translations.contact_admin_button[self.language], callback_data='contact_admin')
        ],
        [
            InlineKeyboardButton(Translations.back[self.language], callback_data='back')
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    ```

#### `handle_callback`

Метод `handle_callback` вызывается при нажатии на одну из кнопок выбора статуса.

- **Параметры**:
  - `update` (объект `Update`): объект обновления, содержащий данные о событии.
  - `context` (объект `ContextTypes.DEFAULT_TYPE`): объект контекста, содержащий данные о текущем состоянии бота.

- **Основные моменты**:
  - **Обработка нажатия на клавишы**:
    Обработка нажатия кнопки и установка выбранного статуса:
    Переход в соответствующую сцену после выбора статуса - TeachingNotStarted/TeachingStarted/TeachingFinished.
    ```python
    query = update.callback_query
    await query.answer()
    selected_status = query.data

    if selected_status == self.STATUS_NOT_STARTED:
        await self.bot.transition_to(TeachingNotStartedScene(self.bot, self.language), update, context)
    if selected_status == self.STATUS_TEACHING:
        await self.bot.transition_to(TeachingStartedScene(self.bot, self.language), update, context)
    if selected_status == self.STATUS_FINISHED:
        await self.bot.transition_to(TeachingFinishedScene(self.bot, self.language), update, context)
    ```
