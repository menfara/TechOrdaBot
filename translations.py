class Translations:
    other_option_message = {
        "kz": "Жауабыңызды жіберіңіз және біз оны администраторға жібереміз.",
        "ru": "Отправьте ваш вопрос, и мы передадим его администратору.",
        "en": "Please send your question, and we will forward it to the administrator."
    }

    return_to_client_status_prompt = {
        'en': "Would you like to return to the Client Status Selection?",
        'ru': "Хотите вернуться к выбору статуса клиента?",
        'kz': "Клиент статусын таңдауға оралу?"
    }

    return_to_client_status_button = {
        'en': "Return to Client Status",
        'ru': "Вернуться к статусу клиента",
        'kz': "Клиент статусына оралу"
    }

    contact_admin_prompt = {
        'en': "Would you like to contact an administrator?",
        'ru': "Хотите задать вопрос администратору?",
        'kz': "Администратормен хабарласу керек пе?"
    }

    contact_admin_button = {
        'en': "Contact administrator",
        'ru': "Связаться с администратором",
        'kz': "Администратормен хабарласу"
    }

    other = {
        "kz": "Басқа сұрақ",
        "ru": "Другой вопрос",
        "en": "Another question"
    }

    back = {
        "kz": "⬅️ Артқа",
        "ru": "⬅️ Назад",
        "en": "⬅️ Back"
    }

    admin_response = {
        "kz": "Администратордың жауабы",
        "ru": "Ответ от администратора",
        "en": "Admin's answer"
    }

    ask_question_prompt = {
        "kz": "Сұрауға жауап беру үшін жазыңыз:",
        "ru": "Напишите ваш вопрос для ответа:",
        "en": "Please write your question to get a response:"
    }

    variant_promt = {
        "kz": "Опцияны таңдаңыз:",
        "ru": "Выберите вариант:",
        "en": "Please select an option:"
    }

    variant_selected = {
        "kz": "Сіз таңдадыңыз:",
        "ru": "Вы выбрали вариант:",
        "en": "You have chosen the option:"
    }

    language_prompt = {
        "kz": "Тілді таңдаңыз:",
        "ru": "Выберите язык:",
        "en": "Please select a language:"
    }

    language_selected = {
        "kz": "Сіз Қазақ тілін таңдадыңыз.",
        "ru": "Вы выбрали Русский язык.",
        "en": "You selected English language."
    }

    status_prompt = {
        "kz": "Бұл бот бүкіл оқу процесінде бағдарламаға қатысушылар үшін нұсқаулық ретінде қызмет етеді. \n\n<b>Статус таңдаңыз:</b>",
        "ru": "Данный бот служит гидом для участников программы в течении всего процесса обучения. \n\n<b>Выберите ваш статус:</b>",
        "en": "This bot serves as a guide for program participants throughout the learning process. \n\n<b>Select your status:</b>"
    }

    status_not_started = {
        "kz": "Студенттерді оқытуды бастамадым",
        "ru": "Еще не начал обучать студентов",
        "en": "Hasn't started teaching students yet"
    }

    status_teaching = {
        "kz": "Студенттерді оқытып жатырмын",
        "ru": "Обучаю студентов",
        "en": "Teaching students"
    }

    status_finished = {
        "kz": "Студенттерді оқыту аяқталды",
        "ru": "Закончил обучать студентов",
        "en": "Finished teaching students"
    }

    status_selected_not_started = {
        "kz": "Сіз таңдадыңыз: Студенттерді оқытуды бастамадым.",
        "ru": "Вы выбрали статус: Еще не начал обучать студентов.",
        "en": "You selected status: Hasn't started teaching students yet."
    }

    status_selected_teaching = {
        "kz": "Сіз таңдадыңыз: Студенттерді оқытып жатырмын.",
        "ru": "Вы выбрали статус: Обучаю студентов.",
        "en": "You selected status: Teaching students."
    }

    status_selected_finished = {
        "kz": "Сіз таңдадыңыз: Студенттерді оқыту аяқталды.",
        "ru": "Вы выбрали статус: Закончил обучать студентов.",
        "en": "You selected status: Finished teaching students."
    }

    showcase_it_school = {
        "kz": "It мектептерінің көрмесі",
        "ru": "Витрина IT школ",
        "en": "IT School Showcase"
    }

    student_selection_process = {
        "kz": "Студенттерді 3 кезеңдік іріктеу",
        "ru": "3-х этапный отбор студентов",
        "en": "3-stage student selection process"
    }

    instructions_links = {
        "round_1": "https://drive.google.com/file/d/1tmJ62fl_jKmWw0qnBXOtlUJif6mTQ_Ld/view",
        "round_2": "https://drive.google.com/file/d/1HrKxblRtI93o4axY5x9Pzo2IcgoifYne/view",
        "round_3": "https://drive.google.com/file/d/19ju_pkzoPM6x7I09MU7860P1GG8clU2u/view"
    }

    student_selection_instructions = {
        "kz": (
            f"<a href=\"{instructions_links['round_1']}\">1-раунд студенттерді іріктеу бойынша нұсқаулық</a>\n"
            f"<a href=\"{instructions_links['round_2']}\">2-раунд студенттерді іріктеу бойынша нұсқаулық</a>\n"
            f"<a href=\"{instructions_links['round_3']}\">3-раунд студенттерді іріктеу бойынша нұсқаулық</a>"
        ),
        "ru": (
            f"<a href=\"{instructions_links['round_1']}\">Инструкция по 1 раунду отбора студентов</a>\n"
            f"<a href=\"{instructions_links['round_2']}\">Инструкция по 2 раунду отбора студентов</a>\n"
            f"<a href=\"{instructions_links['round_3']}\">Инструкция по 3 раунду отбора студентов</a>"
        ),
        "en": (
            f"<a href=\"{instructions_links['round_1']}\">Instructions for Round 1 of Student Selection</a>\n"
            f"<a href=\"{instructions_links['round_2']}\">Instructions for Round 2 of Student Selection</a>\n"
            f"<a href=\"{instructions_links['round_3']}\">Instructions for Round 3 of Student Selection</a>"
        )
    }

    student_contract_link = {
        "contract_1": "https://drive.google.com/file/d/1tmJ62fl_jKmWw0qnBXOtlUJif6mTQ_Ld/view"
    }

    student_contracts_document = {
        "kz": f"<a href=\"{student_contract_link['contract_1']}\">Шарт үлгісі</a>",
        "ru": f"<a href=\"{student_contract_link['contract_1']}\">Шаблон договора</a>",
        "en": f"<a href=\"{student_contract_link['contract_1']}\">Contract template</a>",
    }

    student_contracts = {
        "kz": "Студенттермен шарттар",
        "ru": "Договоры со студентами",
        "en": "Student contracts"
    }

    signing_contract_fund_school = {
        "kz": "Шартқа қол қою Фонд-школа",
        "ru": "Подписание договора Фонд-школа",
        "en": "Signing contract with the school fund"
    }

    advance_payment = {
        "kz": "Аванстық төлем",
        "ru": "Авансовый платеж",
        "en": "Advance payment"
    }

    monthly_report = {
        "kz": "Ай сайынғы есеп беру",
        "ru": "Ежемесячная отчетность",
        "en": "Monthly Report"
    }

    monthly_report_message = {
        "kz": "No translate",
        "ru": "Участник Программы ежемесячно до 10 (десятого) числа месяца следующего за отчетным периодом, на протяжении срока обучения по Курсу(-ам) в рамках Программы, заполняет электронную форму отчета на Портале, содержащую информацию согласно Договору.",
        "en": "No translate"
    }

    learning_change = {
        "kz": "Оқу аясындағы өзгерістер",
        "ru": "Изменения в рамках обучения",
        "en": "Learning Changes"
    }

    learning_change_message = {
        "kz": "No translate",
        "ru": "Все изменения осуществляются по взаимному согласию Сторон и действительны при условии, что они совершены в электронной форме на портале astanahub.com и подписаны уполномоченными на то представителями Сторон.",
        "en": "No translate"
    }

    special_flow = {
        "kz": "Арнайы ағын",
        "ru": "Специализированный поток",
        "en": "Special Flow"
    }

    competence_assessment = {
        "kz": "Құзыреттілікті бағалау",
        "ru": "Оценка компетенций",
        "en": "Competence Assessment"
    }

    competence_assessment_message = {
        "kz": "No trans",
        "ru": "Оценка компетенции- комплексный метод оценки Студента(-ов) и(или) выпускников Программы с целью мониторинга эффективности обучения по Курсам в рамках Программы.",
        "en": "No trans"
    }

    financial_documents = {
        "kz": "No t",
        "ru": "Финальная оплата",
        "en": "Final payment"
    }

    final_payment_message = {
        "kz": "No t",
        "ru": "Оставшаяся сумма Платежа от Суммы финансирования за каждого Студента перечисляется Участнику Программы, при выполнении Участником Программы следующих условий: 1. Завершения обучения Студентом который прошел оценку компетенции. 2. Предоставление финального отчета 3. Предоставления копии сертификатов о прохождении Курсов 4. Предоставления Фонду надлежащим образом сформированного счета на оплату, оформленного на основании ранее направленного акта выполненных работ и электронной счет-фактуры",
        "en": "No t"
    }

    final_report = {
        "kz": "Қорытынды есеп",
        "ru": "Финальная отчетность",
        "en": "Final Report"
    }

    final_report_message = {
        "kz": "No t",
        "ru": "По завершению обучения Участник Программы, в дополнение к заключительному ежемесячному отчету, предоставляет финальный отчет и сертификат Студента по форме, определенной Технопарком.",
        "en": "No t"
    }

    final_report_template_button = {
        "kz": "No t",
        "ru": "Шаблон заполнения финального отчета",
        "en": "No t"
    }

    final_report_template = {
        "kz": "No t",
        "ru": "Шаблон заполнения финального отчета",
        "en": "No t"
    }

    certificate_instructions_button = {
        "kz": "No t",
        "ru": "Инструкция к шаблону сертификата",
        "en": "No t"
    }

    certificate_instructions_template = {
        "kz": "No t",
        "ru": "Инструкция к шаблону сертификата",
        "en": "No t"
    }

    fund_school_link = "https://astanahub.com/ru/l/forms"

    fund_school = {
        "kz": "No translate",
        "ru": f"Договор между Фондом и Школой подписывается после того как школа предоставила все документы Фонду: 1. Подробный график обучения 2. Типовой договор с каждым студентом 3. Согласия студентов на сбор и обработку персональных данных 4. Учредительный документ. Участник Программы может предоставить все необходимые документы через специальную форму <a href=\"{fund_school_link}\">заявки</a>",
        "en": "No translate"
    }

    fund_school_template_button = {
        "kz": f"Шарт үлгісі",
        "ru": f"Шаблон договора",
        "en": f"Contract template",
    }

    fund_school_template = {
        "kz": f"<a href=\"{student_contract_link['contract_1']}\">Шарт үлгісі</a>",
        "ru": f"<a href=\"{student_contract_link['contract_1']}\">Шаблон договора</a>",
        "en": f"<a href=\"{student_contract_link['contract_1']}\">Contract template</a>",
    }

    advance_payment_message = {
        "kz": f"No translate",
        "ru": f"Cумма денежных средств в размере 30% (тридцати процентов) от Общей суммы финансирования, подлежащая финансированию Фондом в пользу Участника Программы после подписания настоящего Договора и передачи Фонду всех необходимых документов.",
        "en": f"No translate",
    }

    get_advance_payment = {
        "kz": f"No translate",
        "ru": f"Что нужно для того чтобы выплатили аванс?",
        "en": f"No translate",
    }

    advance_payment_link = 'https://astanahub.com/account/service/techorda_schools_before/request/266/create/'

    advance_payment_template = {
        "kz": f"No translate",
        "ru": f"Авансовый Платеж оплачивается при выполнении Участником Программы следующих условий: 1. Передачи Фонду подписанных каждым Студентом согласий на сбор и обработку персональных данных 2. Передачи Фонду графика занятий по Курсу(-ам) по форме, предоставленной Фондом 3.  Предоставления Фонду надлежащим образом сформированного счета на оплату 4. Передачи Фонду копий всех подписанных типовых договоров между Школой и Студентом 5. (При наличии) Передачи Фонду копий всех подписанных договоров между Участником Программы и КИК Вы можете загрузить все вышеперечисленные документы по данной ссылке: <a href =\"{advance_payment_link}\">ССЫЛКА</a>",
        "en": f"No translate",
    }

    learning_change_message = {
        "kz": f"No translate",
        "ru": f"Все изменения осуществляются по взаимному согласию Сторон и действительны при условии, что они совершены в электронной форме на портале astanahub.com и подписаны уполномоченными на то представителями Сторон.",
        "en": f"No translate",
    }

    learning_change_details = {
        "kz": f"No translate",
        "ru": f"1. Замена либо исключение студента \n2. Изменение в персональных данных студента \n3. Изменение реквизитов компании (Смена юридического адреса, смена названия компании, банковские реквизиты и смена руководителя) \n4. Изменения в графике обучения (длительность обучения, ссылка на онлайн урок, дни и время проведения занятий, преподаватель по курсу, дата окончания обучения и количество академ часов) \n5. Место проведения занятий (для оффлайн курсов)",
        "en": f"No translate",
    }

    notify_learning_change = {
        "kz": "Қандай өзгерістер туралы Қорды хабардар ету керек?",
        "ru": "О каких изменениях нужно оповещать Фонд?",
        "en": "What changes need to be reported to the Fund?",
    }

    additional_agreements = {
        "kz": "No translate",
        "ru": "Дополнительные соглашения",
        "en": "No translate",
    }

    additional_agreements_message = {
        "kz": "No translate",
        "ru": "Все изменения в настоящий Договор осуществляются по взаимному согласию Сторон и действительны при условии, что они совершены в письменной форме в виде дополнительного соглашения и подписаны уполномоченными на то представителями Сторон",
        "en": "No translate",
    }


class ITSchoolsShowcaseQuestions:
    questions = [
        {
            'question': {
                "kz": "Витринаға қандай деректер жүктеледі?",
                "ru": "Какие данные подгружаются в витрину?",
                "en": "What data is uploaded to the showcase?"
            },
            'answer': {
                "kz": "It мектептердің витринасына бағдарламаға қатысуға өтінімнен деректер тартылады",
                "ru": "В Витрину IT школ подтягиваются данные с заявки на участие в программе.",
                "en": "Data from the application for participation in the program is being pulled into the Showcase of IT schools"
            },
        },

        {
            'question': {
                "kz": "Студенттердің өтінімдер санын қайдан көруге болады?",
                "ru": "Где можно посмотреть количество заявок от студентов?",
                "en": "Where can I see the number of applications from students?"
            },
            'answer': {
                "kz": "astanahub.com порталында, \"Tech Orda\" және \"Менің өтініштерім\" бөліміне өтіңіз",
                "ru": "На портале astanahub.com, заходите в раздел \"Tech Orda\" и в \"Мои заявки\"",
                "en": "On the portal astanahub.com , go to the \"Tech Orda\" section and to \"My applications\""
            },
        },

        {
            'question': {
                "kz": "Менің деректерім витринаға дұрыс енгізілмеген бе?",
                "ru": "У меня некорректно сели данные в Витрину?",
                "en": "Is my data entered incorrectly in the showcase?"
            },
            'answer': {
                "kz": "Мәселеңізді егжей тегжейлі сипаттаңыз",
                "ru": "Развернуто опишите вашу проблему",
                "en": "Describe your problem in detail"
            },
        },

    ]


class MonthlyReportQuestions:
    questions = [
        {
            'question': {
                "kz": "No translation",
                "ru": "Инструкция по заполнению ежемесячного отчета",
                "en": "No translation"
            },
            'answer': {
                "kz": "link",
                "ru": "link",
                "en": "link"
            },
        },

        {
            'question': {
                "kz": "No translation",
                "ru": "Инструкция по заполнению отчета студентами",
                "en": "No translation"
            },
            'answer': {
                "kz": "link",
                "ru": "link",
                "en": "link"
            },
        },

    ]


class CompetenceAssessmentQuestions:
    questions = [
        {
            'question': {
                "kz": "No t",
                "ru": "Сколько нужно набрать баллов для прохождения тестирования",
                "en": "No t"
            },
            'answer': {
                "kz": "No t",
                "ru": "Завершившим обучение Студентом признается Студент, прошедший обучение и набравший проходной балл - 50% (пятьдесят процентов) в рамках Оценки компетенций.",
                "en": "No t"
            },
        },

        {
            'question': {
                "kz": "No t",
                "ru": "Обязательно ли сдавать тестирование каждому студенту?",
                "en": "No t"
            },
            'answer': {
                "kz": "No t",
                "ru": "Студент обязуется принять участие в тестировании и(или) иных мероприятиях в рамках Оценки компетенций в течение обучения по Курсу, следуя правилам честности и академической этики.",
                "en": "No t"
            },
        },



    ]
