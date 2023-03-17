import docx

# загрузка шаблона документа
def create_pass_word(fio, org_name, driver_doc, car_number):
    document = docx.Document("C:/Users/povar/OneDrive/Desktop/pass_bot/wq.docx")

    # поиск места для вставки данных и их вставка
    for paragraph in document.paragraphs:
        paragraph.style.font.name = 'Calibri'
        paragraph.style.font.size = docx.shared.Pt(8)
        paragraph.style.paragraph_format.space_before = docx.shared.Pt(0)
        paragraph.style.paragraph_format.space_after = docx.shared.Pt(0)
        if  "Ф., И., О.," in paragraph.text:
            paragraph.text = f"Ф., И., О., {fio}"
        elif "Наименование организации" in paragraph.text:
            paragraph.text = f"Наименование организации {org_name}"
        elif "Документ водителя" in paragraph.text:
            paragraph.text = f"Документ водителя {driver_doc}"
        # elif "Марка а/м" in paragraph.text:
        #     paragraph.text = f"Марка а/м {car_number}"
        elif "Номер а/м" in paragraph.text:
            paragraph.text = f"Номер а/м {car_number}"

    # сохранение измененного документа
    document.save("pass.docx")
