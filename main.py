import configparser
import time

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ForceReply
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters, CallbackQueryHandler

from google_sheets_reader import create_and_fill_dict_from_json, \
    OUTPUT_FILENAME, IDS_OUTPUT_FILENAME, update_dicts
from translations import Translations, ITSchoolsShowcaseQuestions, MonthlyReportQuestions, CompetenceAssessmentQuestions

SPECIAL_CHARS = [
    '\\',
    '_',
    '*',
    '[',
    ']',
    '(',
    ')',
    '~',
    '`',
    '>',
    '<',
    '&',
    '#',
    '+',
    '-',
    '=',
    '|',
    '{',
    '}',
    '.',
    '!'
]


def escape_markdown(text):
    for char in SPECIAL_CHARS:
        text = text.replace(char, f'\\{char}')
    return text


class State:
    def __init__(self, bot, language=None):
        self.bot = bot
        self.language = language

    async def enter(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        pass

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        pass

    async def handle_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        stack = self.bot.user_states[update.effective_user.id]['state_stack']
        try:
            if stack[-1] != "inner":
                stack.append(self)
                stack.append("inner")
        except Exception:
            pass

    async def handle_back(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.callback_query.message.reply_text("No previous state to go back to.")


class LanguageSelectionScene(State):
    async def enter(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        keyboard = [
            [
                InlineKeyboardButton("Қазақша", callback_data='lang_kz'),
                InlineKeyboardButton("Русский", callback_data='lang_ru'),
                # InlineKeyboardButton("English", callback_data='lang_en')
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        chat_id = update.effective_chat.id
        await context.bot.send_message(
            chat_id=chat_id,
            text=f"{Translations.language_prompt['kz']}\n"
                 f"{Translations.language_prompt['ru']}\n",
            # f"{Translations.language_prompt['en']}\n",
            reply_markup=reply_markup)

    async def handle_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()
        selected_language = query.data
        self.bot.language = selected_language.split('_')[1]  # Extract the language code

        await query.edit_message_text(Translations.language_selected[self.bot.language])

        # Transition to the next scene
        await self.bot.transition_to(ClientStatusSelectionScene(self.bot, self.bot.language), update, context)


class ClientStatusSelectionScene(State):
    STATUS_NOT_STARTED = 'status_not_started'
    STATUS_TEACHING = 'status_teaching'
    STATUS_FINISHED = 'status_finished'

    async def enter(self, update: Update, context: ContextTypes.DEFAULT_TYPE):

        keyboard = [
            [
                InlineKeyboardButton(Translations.status_not_started[self.language],
                                     callback_data=self.STATUS_NOT_STARTED),
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

        message = escape_markdown(Translations.status_prompt[self.language])
        message = message.replace('\<b\>', '*').replace('\</b\>', '*')

        await update.callback_query.message.reply_text(message,
                                                       reply_markup=reply_markup, parse_mode='MarkdownV2')

    async def handle_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()
        selected_status = query.data

        if selected_status == self.STATUS_NOT_STARTED:
            await self.bot.transition_to(TeachingNotStartedScene(self.bot, self.language), update, context)
        if selected_status == self.STATUS_TEACHING:
            await self.bot.transition_to(TeachingStartedScene(self.bot, self.language), update, context)
        if selected_status == self.STATUS_FINISHED:
            await self.bot.transition_to(TeachingFinishedScene(self.bot, self.language), update, context)


class TeachingNotStartedScene(State):
    SCENE_TAG = 'не_начал_обучать'
    options = [
        'showcase_it_school',
        'student_selection_process',
        'student_contracts',
        'signing_contract_fund_school',
        'advance_payment',
    ]

    async def enter(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        keyboard = []

        for option in self.options:
            keyboard.append([InlineKeyboardButton(Translations.__dict__[option][self.language],
                                                  callback_data=option)])

        keyboard.append(
            [InlineKeyboardButton(Translations.back[self.language], callback_data='back')])

        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.callback_query.message.reply_text(Translations.status_message[self.language],
                                                       reply_markup=reply_markup)

    async def handle_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()
        selected_option = query.data

        # Handle the selected course
        # await query.edit_message_text(f"{Translations.variant_selected[self.language]}: {Translations.variant_promt[]}")

        # Transition to another scene or handle further actions if needed
        if selected_option == self.options[0]:
            await self.bot.transition_to(TNESchoolShowcaseScene(self.bot, self.language), update, context)
        if selected_option == self.options[1]:
            await self.bot.transition_to(TNEStudentSelectionScene(self.bot, self.language), update, context)
        if selected_option == self.options[2]:
            await self.bot.transition_to(TNEStudentContractScene(self.bot, self.language), update, context)
        if selected_option == self.options[3]:
            await self.bot.transition_to(TNEFundSchoolScene(self.bot, self.language), update, context)
        if selected_option == self.options[4]:
            await self.bot.transition_to(TNEAdvancePaymentScene(self.bot, self.language), update, context)


# Витрина IT школ
class TNESchoolShowcaseScene(State):
    SCENE_TAG = 'витрина_школ'
    OPTION_OTHER = 'other'

    def __init__(self, bot, language=None):
        super().__init__(bot, language)
        self.questions = ITSchoolsShowcaseQuestions.questions

    async def enter(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        keyboard = []
        for index, question_set in enumerate(self.questions):
            question_text = question_set['question'][self.language]
            button = InlineKeyboardButton(f"{question_text}", callback_data=f'question_{index}')
            keyboard.append([button])

        keyboard.append([InlineKeyboardButton(f"{Translations.other[self.language]}", callback_data=self.OPTION_OTHER)])
        keyboard.append([InlineKeyboardButton(f"{Translations.back[self.language]}", callback_data='back')])

        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.callback_query.message.reply_text(Translations.variant_promt[self.language],
                                                       reply_markup=reply_markup)

    async def handle_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await super().handle_callback(update, context)
        query = update.callback_query
        await query.answer()
        selected_option = query.data

        if selected_option == self.OPTION_OTHER:
            await self.bot.send_message_with_force_reply(update, Translations.other_option_message[self.language])

        else:
            # Extract the question index from the callback data
            question_index = int(selected_option.split('_')[1])

            # Get the answer for the selected question in the current language
            answer_text = self.questions[question_index]['answer'][self.language]

            # Retrieve the question text from the questions list
            question_text = self.questions[question_index]['question'][self.language]

            # Send the answer to the chat
            await query.edit_message_text(f"{question_text}:\n\n{answer_text}")
        await self.bot.suggest_return_to_client_status(update, context)


class TNEStudentSelectionScene(State):
    SCENE_TAG = 'отбор_студентов'
    OPTION_OTHER = 'other'

    def __init__(self, bot, language=None):
        super().__init__(bot, language)
        self.questions = ITSchoolsShowcaseQuestions.questions

    async def enter(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        keyboard = []

        keyboard.append([InlineKeyboardButton(f"{Translations.other[self.language]}", callback_data=self.OPTION_OTHER)])
        keyboard.append([InlineKeyboardButton(f"{Translations.back[self.language]}", callback_data='back')])

        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.callback_query.message.reply_text(Translations.student_selection_instructions[self.language],
                                                       reply_markup=reply_markup, parse_mode="HTML")

    async def handle_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await super().handle_callback(update, context)

        query = update.callback_query
        await query.answer()
        selected_option = query.data

        if selected_option == self.OPTION_OTHER:
            await self.bot.send_message_with_force_reply(update, Translations.other_option_message[self.language])

        else:
            # Extract the question index from the callback data
            question_index = int(selected_option.split('_')[1])

            # Get the answer for the selected question in the current language
            answer_text = self.questions[question_index]['answer'][self.language]

            # Retrieve the question text from the questions list
            question_text = self.questions[question_index]['question'][self.language]

            # Send the answer to the chat
            await query.edit_message_text(f"{question_text}:\n\n{answer_text}")
        await self.bot.suggest_return_to_client_status(update, context)


class TNEStudentContractScene(State):
    SCENE_TAG = 'договоры_со_студентами'
    OPTION_OTHER = 'other'
    OPTION_1 = 'doc'

    def __init__(self, bot, language=None):
        super().__init__(bot, language)

    async def enter(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        keyboard = []

        keyboard.append([InlineKeyboardButton(f"{Translations.fund_school_template_button[self.language]}",
                                              callback_data=self.OPTION_1)])
        keyboard.append([InlineKeyboardButton(f"{Translations.other[self.language]}", callback_data=self.OPTION_OTHER)])
        keyboard.append([InlineKeyboardButton(f"{Translations.back[self.language]}", callback_data='back')])

        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.callback_query.message.reply_text(Translations.variant_promt[self.language],
                                                       reply_markup=reply_markup, parse_mode="HTML")

    async def handle_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await super().handle_callback(update, context)

        query = update.callback_query
        await query.answer()
        selected_option = query.data

        if selected_option == self.OPTION_1:
            with open('docs/типовой_договор_школа_студент.docx', 'rb') as document:
                await context.bot.send_document(chat_id=query.message.chat_id, document=document)

        if selected_option == self.OPTION_OTHER:
            await self.bot.send_message_with_force_reply(update, Translations.other_option_message[self.language])

        await self.bot.suggest_return_to_client_status(update, context)


class TNEFundSchoolScene(State):
    SCENE_TAG = 'фонд_школа'
    OPTION_1 = 'fund_school_template'
    OPTION_OTHER = 'other'

    def __init__(self, bot, language=None):
        super().__init__(bot, language)

    async def enter(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        keyboard = []

        # keyboard.append([InlineKeyboardButton(f"{Translations.__dict__[self.OPTION_1][self.language]}",
        #                                       callback_data=self.OPTION_1)])
        keyboard.append([InlineKeyboardButton(f"{Translations.fund_school_template_button[self.language]}",
                                              callback_data=self.OPTION_1)])
        keyboard.append([InlineKeyboardButton(f"{Translations.other[self.language]}", callback_data=self.OPTION_OTHER)])
        keyboard.append([InlineKeyboardButton(f"{Translations.back[self.language]}", callback_data='back')])

        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.callback_query.message.reply_text(Translations.fund_school[self.language],
                                                       reply_markup=reply_markup, parse_mode="HTML")

    async def handle_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await super().handle_callback(update, context)

        query = update.callback_query
        await query.answer()
        selected_option = query.data

        if selected_option == self.OPTION_1:
            with open('docs/договор_фонд_школа.docx', 'rb') as document:
                await context.bot.send_document(chat_id=query.message.chat_id, document=document)

        if selected_option == self.OPTION_OTHER:
            await self.bot.send_message_with_force_reply(update, Translations.other_option_message[self.language])

        await self.bot.suggest_return_to_client_status(update, context)


class TNEAdvancePaymentScene(State):
    SCENE_TAG = 'авансовый_платеж'
    OPTION_1 = 'get_advance_payment'
    OPTION_OTHER = 'other'

    def __init__(self, bot, language=None):
        super().__init__(bot, language)

    async def enter(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        keyboard = []

        keyboard.append([InlineKeyboardButton(f"{Translations.get_advance_payment[self.language]}",
                                              callback_data=self.OPTION_1)])
        keyboard.append([InlineKeyboardButton(f"{Translations.other[self.language]}", callback_data=self.OPTION_OTHER)])
        keyboard.append([InlineKeyboardButton(f"{Translations.back[self.language]}", callback_data='back')])

        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.callback_query.message.reply_text(Translations.advance_payment_message[self.language],
                                                       reply_markup=reply_markup, parse_mode="HTML")

    async def handle_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await super().handle_callback(update, context)

        query = update.callback_query
        await query.answer()
        selected_option = query.data

        if selected_option == self.OPTION_1:
            await update.callback_query.message.reply_text(Translations.advance_payment_template[self.language],
                                                           parse_mode="HTML")
        if selected_option == self.OPTION_OTHER:
            await self.bot.send_message_with_force_reply(update, Translations.other_option_message[self.language])

        await self.bot.suggest_return_to_client_status(update, context)


class TeachingStartedScene(State):
    options = [
        'monthly_report',
        'learning_change',
        'other',
    ]

    async def enter(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        keyboard = []

        for option in self.options:
            keyboard.append([InlineKeyboardButton(Translations.__dict__[option][self.language],
                                                  callback_data=option)])

        keyboard.append(
            [InlineKeyboardButton(Translations.nps[self.language], callback_data='nps')])

        keyboard.append(
            [InlineKeyboardButton(Translations.back[self.language], callback_data='back')])

        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.callback_query.message.reply_text(Translations.variant_promt[self.language],
                                                       reply_markup=reply_markup)

    async def handle_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await super().handle_callback(update, context)

        query = update.callback_query
        await query.answer()
        selected_status = query.data

        if selected_status == 'nps':
            await update.callback_query.message.reply_text(Translations.nps_message[self.language])

        if selected_status == self.options[2]:
            await self.bot.send_message_with_force_reply(update, Translations.other_option_message[self.language])

        if selected_status == self.options[0]:
            await self.bot.transition_to(TSMonthlyReport(self.bot, self.language), update, context)
        if selected_status == self.options[1]:
            await self.bot.transition_to(TSLearningChange(self.bot, self.language), update, context)


class TSMonthlyReport(State):
    SCENE_TAG = 'ежемесячная_отчетность'
    OPTION_OTHER = 'other'

    def __init__(self, bot, language=None):
        super().__init__(bot, language)
        self.questions = MonthlyReportQuestions.questions

    async def enter(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        keyboard = []
        for index, question_set in enumerate(self.questions):
            question_text = question_set['question'][self.language]
            button = InlineKeyboardButton(f"{question_text}", callback_data=f'question_{index}')
            keyboard.append([button])

        keyboard.append([InlineKeyboardButton(f"{Translations.other[self.language]}", callback_data=self.OPTION_OTHER)])
        keyboard.append([InlineKeyboardButton(f"{Translations.back[self.language]}", callback_data='back')])

        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.callback_query.message.reply_text(Translations.monthly_report_message[self.language],
                                                       reply_markup=reply_markup)

    async def handle_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await super().handle_callback(update, context)

        query = update.callback_query
        await query.answer()
        selected_option = query.data

        if selected_option == self.OPTION_OTHER:
            await self.bot.send_message_with_force_reply(update, Translations.other_option_message[self.language])

        else:
            # Extract the question index from the callback data
            question_index = int(selected_option.split('_')[1])

            # Get the answer for the selected question in the current language
            document_path = self.questions[question_index]['answer'][self.language]

            # Retrieve the question text from the questions list
            question_text = self.questions[question_index]['question'][self.language]

            with open(f'docs/{document_path}', 'rb') as document:
                await context.bot.send_document(chat_id=query.message.chat_id, document=document)

            # Send the answer to the chat
        await self.bot.suggest_return_to_client_status(update, context)


class TSLearningChange(State):
    SCENE_TAG = 'изменение_обучения'
    OPTION_1 = 'notify_learning_change'
    OPTION_2 = 'additional_agreements'
    OPTION_OTHER = 'other'

    def __init__(self, bot, language=None):
        super().__init__(bot, language)

    async def enter(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        keyboard = []

        keyboard.append([InlineKeyboardButton(f"{Translations.notify_learning_change[self.language]}",
                                              url="https://astanahub.com/account/service/techorda_request/request/168/create/")])
        keyboard.append([InlineKeyboardButton(f"{Translations.additional_agreements[self.language]}",
                                              callback_data=self.OPTION_2)])
        keyboard.append([InlineKeyboardButton(f"{Translations.other[self.language]}", callback_data=self.OPTION_OTHER)])
        keyboard.append([InlineKeyboardButton(f"{Translations.back[self.language]}", callback_data='back')])

        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.callback_query.message.reply_text(Translations.learning_change_message[self.language],
                                                       reply_markup=reply_markup)

    async def handle_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await super().handle_callback(update, context)

        query = update.callback_query
        await query.answer()
        selected_option = query.data

        if selected_option == self.OPTION_1:
            # https://astanahub.com/account/service_request/98827/update/?tab=0
            # await update.callback_query.message.reply_text(Translations.learning_change_details[self.language])
            pass
        if selected_option == self.OPTION_2:
            keyboard = [[InlineKeyboardButton(f"{Translations.other[self.language]}", callback_data=self.OPTION_OTHER)]]

            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.callback_query.message.reply_text(Translations.additional_agreements_message[self.language],
                                                           reply_markup=reply_markup)

        if selected_option == self.OPTION_OTHER:
            await self.bot.send_message_with_force_reply(update, Translations.other_option_message[self.language])

        await self.bot.suggest_return_to_client_status(update, context)


class TeachingFinishedScene(State):
    options = [
        'competence_assessment',
        'final_report',
        'financial_documents',
    ]

    async def enter(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        keyboard = []

        for option in self.options:
            keyboard.append([InlineKeyboardButton(Translations.__dict__[option][self.language],
                                                  callback_data=option)])

        keyboard.append(
            [InlineKeyboardButton(Translations.back[self.language], callback_data='back')])

        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.callback_query.message.reply_text(Translations.variant_promt[self.language],
                                                       reply_markup=reply_markup)

    async def handle_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()
        selected_status = query.data

        if selected_status == self.options[0]:
            await self.bot.transition_to(TFCompetenceAssessment(self.bot, self.language), update, context)
        if selected_status == self.options[1]:
            await self.bot.transition_to(TFFinalReport(self.bot, self.language), update, context)
        if selected_status == self.options[2]:
            await self.bot.transition_to(TFFinalPayment(self.bot, self.language), update, context)


class TFCompetenceAssessment(State):
    SCENE_TAG = 'оценка_компетенции'
    OPTION_OTHER = 'other'

    def __init__(self, bot, language=None):
        super().__init__(bot, language)
        self.questions = CompetenceAssessmentQuestions.questions

    async def enter(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        keyboard = []
        for index, question_set in enumerate(self.questions):
            question_text = question_set['question'][self.language]
            button = InlineKeyboardButton(f"{question_text}", callback_data=f'question_{index}')
            keyboard.append([button])

        keyboard.append([InlineKeyboardButton(f"{Translations.other[self.language]}", callback_data=self.OPTION_OTHER)])
        keyboard.append([InlineKeyboardButton(f"{Translations.back[self.language]}", callback_data='back')])

        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.callback_query.message.reply_text(Translations.competence_assessment_message[self.language],
                                                       reply_markup=reply_markup)

    async def handle_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await super().handle_callback(update, context)


        query = update.callback_query
        await query.answer()
        selected_option = query.data

        if selected_option == self.OPTION_OTHER:
            await self.bot.send_message_with_force_reply(update, Translations.other_option_message[self.language])
        elif selected_option == 'question_3':
            with open(f'docs/инструкция.docx', 'rb') as document:
                await context.bot.send_document(chat_id=query.message.chat_id, document=document)
            with open(f'docs/инструкция_для_школ.docx', 'rb') as document:
                await context.bot.send_document(chat_id=query.message.chat_id, document=document)
        else:
            # Extract the question index from the callback data
            question_index = int(selected_option.split('_')[1])

            # Get the answer for the selected question in the current language
            answer_text = self.questions[question_index]['answer'][self.language]

            # Retrieve the question text from the questions list
            question_text = self.questions[question_index]['question'][self.language]

            # Send the answer to the chat
            await query.edit_message_text(f"{question_text}:\n\n{answer_text}", parse_mode='HTML')
        await self.bot.suggest_return_to_client_status(update, context)


class TFFinalReport(State):
    SCENE_TAG = 'финальная_отчетность'
    OPTION_OTHER = 'other'
    OPTION_1 = 'final_report_template'
    OPTION_2 = 'certificate_instructions'

    def __init__(self, bot, language=None):
        super().__init__(bot, language)
        self.questions = CompetenceAssessmentQuestions.questions

    async def enter(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        keyboard = [
            [InlineKeyboardButton(f"{Translations.final_report_form[self.language]}",
                                  url="https://astanahub.com/account/service_request/98834/update/?tab=0")],

            [InlineKeyboardButton(f"{Translations.final_report_template_button[self.language]}",
                                  callback_data=self.OPTION_1)],

            [InlineKeyboardButton(f"{Translations.certificate_instructions_button[self.language]}",
                                  callback_data=self.OPTION_2)],
            [InlineKeyboardButton(f"{Translations.other[self.language]}", callback_data=self.OPTION_OTHER)],
            [InlineKeyboardButton(f"{Translations.back[self.language]}", callback_data='back')]]

        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.callback_query.message.reply_text(Translations.final_report_message[self.language],
                                                       reply_markup=reply_markup)

    async def handle_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await super().handle_callback(update, context)

        query = update.callback_query
        await query.answer()
        selected_option = query.data

        if selected_option == self.OPTION_1:
            keyboard = [[InlineKeyboardButton(f"{Translations.other[self.language]}", callback_data=self.OPTION_OTHER)]]

            reply_markup = InlineKeyboardMarkup(keyboard)
            with open('docs/шаблон_финального_отчета.docx', 'rb') as document:
                await context.bot.send_document(chat_id=query.message.chat_id, document=document,
                                                reply_markup=reply_markup)

        if selected_option == self.OPTION_2:
            keyboard = [[InlineKeyboardButton(f"{Translations.other[self.language]}", callback_data=self.OPTION_OTHER)]]

            reply_markup = InlineKeyboardMarkup(keyboard)
            with open('docs/инструкция_к_шаблону_сертификата.pdf', 'rb') as document:
                await context.bot.send_document(chat_id=query.message.chat_id, document=document,
                                                reply_markup=reply_markup)

        if selected_option == self.OPTION_OTHER:
            await self.bot.send_message_with_force_reply(update, Translations.other_option_message[self.language])

        await self.bot.suggest_return_to_client_status(update, context)


class TFFinalPayment(State):
    SCENE_TAG = 'финальная_оплата'
    OPTION_OTHER = 'other'
    OPTION_1 = 'electronic_act'
    OPTION_2 = 'final_payment_bill'

    def __init__(self, bot, language=None):
        super().__init__(bot, language)
        self.questions = CompetenceAssessmentQuestions.questions

    async def enter(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        keyboard = [[InlineKeyboardButton(f"{Translations.electronic_act[self.language]}",
                                          callback_data=self.OPTION_1)],
                    [InlineKeyboardButton(f"{Translations.final_payment_bill[self.language]}",
                                          callback_data=self.OPTION_2)],
                    [InlineKeyboardButton(f"{Translations.other[self.language]}", callback_data=self.OPTION_OTHER)],
                    [InlineKeyboardButton(f"{Translations.back[self.language]}", callback_data='back')]]

        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.callback_query.message.reply_text(Translations.final_payment_message[self.language],
                                                       reply_markup=reply_markup)

    async def handle_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await super().handle_callback(update, context)

        query = update.callback_query
        await query.answer()
        selected_option = query.data

        if selected_option == self.OPTION_1:
            keyboard = [[InlineKeyboardButton(f"{Translations.other[self.language]}", callback_data=self.OPTION_OTHER)]]

            reply_markup = InlineKeyboardMarkup(keyboard)
            with open('docs/памятка_по_ЭАВР_для_школы.docx', 'rb') as document:
                await context.bot.send_document(chat_id=query.message.chat_id, document=document,
                                                reply_markup=reply_markup)

        if selected_option == self.OPTION_2:
            keyboard = [[InlineKeyboardButton(f"{Translations.other[self.language]}", callback_data=self.OPTION_OTHER)]]

            reply_markup = InlineKeyboardMarkup(keyboard)
            with open('docs/счет_на_фин_оплату_для_школы.docx', 'rb') as document:
                await context.bot.send_document(chat_id=query.message.chat_id, document=document,
                                                reply_markup=reply_markup)

        if selected_option == self.OPTION_OTHER:
            await self.bot.send_message_with_force_reply(update, Translations.other_option_message[self.language])

        await self.bot.suggest_return_to_client_status(update, context)


class ContactAdminScene(State):
    OPTIONS = [
        'monthly_report',
        'learning_change',
        'special_flow',
        'competence_assessment',
        'financial_documents',
        'final_report',
        'other'
    ]

    STATUS_NOT_STARTED = 'status_not_started'
    STATUS_TEACHING = 'status_teaching'
    STATUS_FINISHED = 'status_finished'

    async def enter(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_language = self.language

        keyboard = [
            [InlineKeyboardButton(Translations.status_not_started[self.language],
                                  callback_data=self.STATUS_NOT_STARTED), ],
            [InlineKeyboardButton(Translations.status_teaching[self.language], callback_data=self.STATUS_TEACHING), ],
            [InlineKeyboardButton(Translations.status_finished[self.language], callback_data=self.STATUS_FINISHED)],
            # [InlineKeyboardButton(Translations.back[user_language], callback_data='back')],
            [InlineKeyboardButton(Translations.confirm_contact_button[user_language],
                                  callback_data='confirm_contact_admin')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        if update.message:
            await update.message.reply_text(Translations.convince_message[user_language], reply_markup=reply_markup)
        elif update.callback_query:
            await update.callback_query.message.reply_text(Translations.convince_message[user_language],
                                                           reply_markup=reply_markup)

    async def handle_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()
        selected_option = query.data

        if selected_option == self.STATUS_NOT_STARTED:
            await self.bot.transition_to(TeachingNotStartedScene(self.bot, self.language), update, context)
        if selected_option == self.STATUS_TEACHING:
            await self.bot.transition_to(TeachingStartedScene(self.bot, self.language), update, context)
        if selected_option == self.STATUS_FINISHED:
            await self.bot.transition_to(TeachingFinishedScene(self.bot, self.language), update, context)

        if selected_option == 'confirm_contact_admin':
            await self.show_options(update, context)
        elif self.OPTIONS.__contains__(selected_option):
            await self.bot.send_message_with_force_reply(update, Translations.other_option_message[self.language],
                                                         Translations.__dict__[selected_option]['ru'].lower().replace(
                                                             ' ', '_'))

    async def show_options(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        keyboard = []
        for option in self.OPTIONS:
            button = InlineKeyboardButton(Translations.__dict__[option][self.language], callback_data=option)
            keyboard.append([button])

        keyboard.append([InlineKeyboardButton(Translations.back[self.language], callback_data='back')])

        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.callback_query.message.reply_text(Translations.variant_promt[self.language],
                                                       reply_markup=reply_markup)


class Bot:
    def __init__(self, config_file):
        self.nps = create_and_fill_dict_from_json(OUTPUT_FILENAME)
        self.ids = create_and_fill_dict_from_json(IDS_OUTPUT_FILENAME)

        self.contact_admin_tag = {}

        self.user_states = {}
        self.last_interaction_time = {}

        self.config = configparser.ConfigParser()
        self.config.read(config_file)
        self.token = self.config.get('telegram', 'token')
        self.application = Application.builder().token(self.token).build()

        self.admin_ids = [int(admin_id) for admin_id in
                          self.config.get('telegram', 'admin_ids').split(',')]

        self.application.add_handler(CommandHandler('start', self.start))
        self.application.add_handler(CommandHandler('chat_id', self.chat_id))
        # self.application.add_handler(CommandHandler('getvalue', self.handle_get_value))
        self.application.add_handler(CallbackQueryHandler(self.handle_callback_query))
        self.register_reply_handler()

    async def chat_id(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        print(update.effective_chat.id)

    def is_spamming(self, user_id):
        current_time = time.time()
        if user_id in self.last_interaction_time:
            if current_time - self.last_interaction_time[user_id] < 1:
                return True
        self.last_interaction_time[user_id] = current_time
        return False

    async def check_for_spam(self, update: Update):
        user_id = update.effective_user.id
        if self.is_spamming(user_id):
            if update.message:
                await update.message.reply_text(
                    "You're sending messages too quickly. Please wait a moment before trying again.")
            elif update.callback_query:
                await update.callback_query.answer(
                    "You're interacting too quickly. Please wait a moment before trying again.")
            return True
        return False

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if await self.check_for_spam(update):
            return

        await self.transition_to(LanguageSelectionScene(self), update, context)

    async def handle_get_value(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        key = update.message.text
        print(key)
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text=f"{self.nps['name']}: {self.nps[self.ids[key]]}")

    async def transition_to(self, state: State, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = update.effective_user
        user_id = user.id

        if user_id not in self.user_states:
            self.user_states[user_id] = {'state_stack': [], 'current_state': None}

        if self.user_states[user_id]['current_state']:
            self.user_states[user_id]['state_stack'].append(self.user_states[user_id]['current_state'])

        self.user_states[user_id]['current_state'] = state
        await self.user_states[user_id]['current_state'].enter(update, context)

    async def handle_callback_query(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if await self.check_for_spam(update):
            return

        query = update.callback_query
        data = query.data
        user = update.effective_user
        user_id = user.id

        if user_id not in self.user_states:
            self.user_states[user_id] = {'state_stack': [], 'current_state': None}

        user_language = self.user_states[user_id]['current_state'].language

        if data == 'back':
            await self.handle_back(update, context)
        elif data == 'return_to_client_status':
            await self.transition_to(ClientStatusSelectionScene(self, user_language), update, context)
        elif data == 'contact_admin':
            await self.transition_to(ContactAdminScene(self, user_language), update, context)
        else:
            if self.user_states[user_id]['current_state']:
                await self.user_states[user_id]['current_state'].handle_callback(update, context)

    async def handle_back(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = update.effective_user
        user_id = user.id

        if user_id not in self.user_states:
            self.user_states[user_id] = {'state_stack': [], 'current_state': None}

        user_id_state_stack = self.user_states[user_id]['state_stack']
        if user_id_state_stack:
            previous_state = user_id_state_stack.pop()

            if previous_state == "inner":
                previous_state = user_id_state_stack.pop()
                print(previous_state)
            
            self.user_states[user_id]['current_state'] = previous_state
            await self.user_states[user_id]['current_state'].enter(update, context)
        else:
            await update.callback_query.message.reply_text("No previous state to go back to.")

    async def send_message_with_force_reply(self, update: Update, text, question_tag=""):
        self.user_states[update.effective_user.id]['question_tag'] = question_tag
        await update.callback_query.message.reply_text(
            text,
            reply_markup=ForceReply(selective=True)
        )

    def register_reply_handler(self):
        reply_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_reply)
        self.application.add_handler(reply_handler)

    async def handle_reply(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if await self.check_for_spam(update):
            return

        chat_id = update.message.chat_id

        # ADMIN REPLY
        if update.message.reply_to_message and chat_id in self.admin_ids:
            user_chat_id = int(update.message.reply_to_message.text.split()[0].replace('|', ''))
            user_language = self.user_states[user_chat_id]['current_state'].language

            print(self.user_states, update.effective_user.id, user_chat_id)

            await context.bot.send_message(
                chat_id=user_chat_id,
                text=f"{Translations.admin_response[user_language]}:\n\n{update.message.text}",
            )
            return

        if update.message.reply_to_message and update.message.reply_to_message.from_user.id == context.bot.id:
            print("Reply is to the bot's message.")
            await self.send_question_to_admin_group(update, context)

        elif update.message.text.startswith('pass123'):
            new_url = update.message.text.split(' ', 1)[1]
            config = configparser.ConfigParser()
            config.read('config.ini')
            if 'google_sheets' not in config:
                config.add_section('google_sheets')
            config.set('google_sheets', 'sheet_url', new_url)
            with open('config.ini', 'w') as config_file:
                config.write(config_file)

            update_dicts()
            self.nps = create_and_fill_dict_from_json(OUTPUT_FILENAME)
            self.ids = create_and_fill_dict_from_json(IDS_OUTPUT_FILENAME)

        else:
            print("Reply is not to the bot's message. Ignoring.")
            if len(update.message.text) == 6:
                await self.handle_get_value(update, context)

    async def send_question_to_admin_group(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = update.effective_user
        message_text = update.message.text  # Используем текст ответа пользователя

        admin_message = (
            f"<spoiler>{update.message.chat_id}</spoiler>\n\n"
            f"Вопрос от пользователя {user.full_name} (@{user.username}):\n\n"
            f"{message_text}"
        )

        question_tag = self.user_states[user.id]['question_tag']

        if hasattr(self.user_states[user.id]['current_state'], 'SCENE_TAG'):
            admin_message += f"\n\n#{self.user_states[user.id]['current_state'].SCENE_TAG}"
        elif question_tag != '':
            admin_message += f"\n\n#{question_tag}"
        else:
            admin_message += "\n\n#другое"

        admin_message = escape_markdown(admin_message)
        print(admin_message)
        admin_message = admin_message.replace('\<spoiler\>', '||').replace('\</spoiler\>', '||')

        for admin_id in self.admin_ids:
            await context.bot.send_message(chat_id=admin_id, text=admin_message, parse_mode='MarkdownV2')

    async def suggest_return_to_client_status(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_language = self.user_states[update.effective_user.id]['current_state'].language

        keyboard = [
            [InlineKeyboardButton(Translations.return_to_client_status_button[user_language],
                                  callback_data='return_to_client_status')],
            [InlineKeyboardButton(Translations.back[user_language],
                                  callback_data='back')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        if update.message:
            await update.message.reply_text(Translations.return_to_client_status_prompt[user_language],
                                            reply_markup=reply_markup)
        elif update.callback_query:
            await update.callback_query.message.reply_text(Translations.return_to_client_status_prompt[user_language],
                                                           reply_markup=reply_markup)

    async def suggest_contact_admin(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_language = self.user_states[update.effective_user.id]['current_state'].language

        keyboard = [
            [InlineKeyboardButton(Translations.contact_admin_button[user_language],
                                  callback_data='contact_admin')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        if update.message:
            await update.message.reply_text(Translations.contact_admin_prompt[user_language],
                                            reply_markup=reply_markup)
        elif update.callback_query:
            await update.callback_query.message.reply_text(Translations.contact_admin_prompt[user_language],
                                                           reply_markup=reply_markup)

    def run(self):
        self.application.run_polling()


if __name__ == "__main__":
    bot = Bot('config.ini')
    bot.run()
