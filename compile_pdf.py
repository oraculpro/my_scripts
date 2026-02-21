from PIL import Image
import sys
import os

def create_pdf(output_pdf, image_files):
    """
    Создаёт PDF из списка изображений.
    
    Args:
        output_pdf: Имя выходного PDF файла
        image_files: Список путей к изображениям
    """
    try:
        # Открываем все изображения
        images = []
        for img_path in image_files:
            if not os.path.exists(img_path):
                print(f'❌ Файл не найден: {img_path}')
                continue
            
            try:
                img = Image.open(img_path)
                # Конвертируем в RGB (для совместимости с PDF)
                if img.mode in ('RGBA', 'P'):
                    img = img.convert('RGB')
                images.append(img)
                print(f'✅ Добавлено: {img_path}')
            except Exception as e:
                print(f'❌ Ошибка открытия {img_path}: {e}')
        
        if not images:
            print('❌ Нет изображений для создания PDF')
            return
        
        # Сохраняем как PDF
        images[0].save(
            output_pdf,
            save_all=True,
            append_images=images[1:],
            resolution=100.0,
            quality='high'
        )
        
        print(f'\n✅ PDF успешно создан: {output_pdf}')
        print(f'📄 Страниц: {len(images)}')
        print(f'📁 Файлы:')
        for i, img_path in enumerate(image_files, 1):
            print(f'   {i}. {img_path}')
        
    except Exception as e:
        print(f'❌ Ошибка создания PDF: {e}')

def main():
    # Проверка аргументов
    if len(sys.argv) < 3:
        print('Использование:')
        print('  python compile_pdf.py <output.pdf> <image1.png> <image2.png> ...')
        print('\nПример:')
        print('  python compile_pdf.py меню_неделя_1.png Меню_Завтраки_Салаты.png Меню_Горячие_Гарниры.png Меню_Супы_Напитки_Фрукты.png')
        sys.exit(1)
    
    output_pdf = sys.argv[1]
    image_files = sys.argv[2:]
    
    # Проверка расширения выходного файла
    if not output_pdf.lower().endswith('.pdf'):
        print('⚠️  Выходной файл должен иметь расширение .pdf')
        print(f'   Исправлено: {output_pdf} -> {output_pdf}.pdf')
        output_pdf = output_pdf + '.pdf'
    
    create_pdf(output_pdf, image_files)

if __name__ == '__main__':
    main()