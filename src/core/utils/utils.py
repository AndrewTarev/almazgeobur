import os


def format_and_save_report(
    date, total_revenue, top_products, categories, report_content
):
    # Создаем документ Word
    doc = Document()

    # Добавляем заголовок
    doc.add_heading("Отчет о продажах", level=1)
    doc.add_paragraph(f"Дата отчета: {date}")

    # Добавляем разделы
    doc.add_heading("1. Общая выручка", level=2)

    doc.add_paragraph(f"Выручка за период: руб.")

    doc.add_heading("2. Топ-3 товара по продажам", level=2)
    for product in top_products:
        doc.add_paragraph(product, style="List Bullet")

    doc.add_heading("3. Распределение по категориям", level=2)
    for category in categories:
        doc.add_paragraph(category, style="List Bullet")

    doc.add_heading("4. Аналитические выводы", level=2)
    doc.add_paragraph(report_content)

    # Указываем директорию для сохранения отчетов
    reports_dir = "reports"
    if not os.path.exists(reports_dir):
        os.makedirs(reports_dir)

    # Создаем имя файла для отчета
    report_filename = os.path.join(reports_dir, f"отчет_продажи_{date}.docx")

    # Сохраняем документ
    doc.save(report_filename)

    return report_filename


def generate_and_save_report(date, total_revenue, top_products, categories):
    content = generate_report_content(date, total_revenue, top_products, categories)
    report_filename = format_and_save_report(
        date, total_revenue, top_products, categories, content
    )
    return f"Отчет сохранен в файле {report_filename}"
