import tkinter as tk
from collections import defaultdict
import json
import os
from PIL import ImageTk, Image

DATA_FILE = r"cats_data.json"
ANIMATION_PATH = r"cat_animation.gif"
IMAGE_DIR = r"image_path"

def center_window(window, width, height):

    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = int((screen_width - width) / 2)
    y = int((screen_height - height) / 2)
    window.geometry(f"{width}x{height}+{x}+{y}")

def load_data():
    if os.path.exists(DATA_FILE):
        print(f"Файл найден: {DATA_FILE}")
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as file:
                content = file.read().strip()
                if not content:
                    raise json.JSONDecodeError("Файл пустой", content, 0)
                return json.loads(content)
        except json.JSONDecodeError:
            print("Ошибка: Некорректный формат JSON. Файл будет перезаписан.")

            initial_data = [
                {'name': 'Сибирская кошка',
                 'desc': 'Одна из старейших русских пород кошек.',
                 'weight': '4–10 кг',
                 'height': '25–38 см',
                 'life_span': '12–16 лет'},
                {'name': 'Британская короткошёрстная',
                 'desc': 'Известна своей спокойной натурой и густым мехом.',
                 'weight': '4–8 кг',
                 'height': '25–30 см',
                 'life_span': '12–17 лет'},
                {'name': 'Сфинкс',
                 'desc': 'Безволосые кошки с большими ушами и выразительными глазами.',
                 'weight': '3–6 кг',
                 'height': '23–30 см',
                 'life_span': '10–15 лет'},
                {'name': 'Русская голубая',
                 'desc': 'Изящная кошка с короткой серовато-голубоватой шерстью.',
                 'weight': '3–6 кг',
                 'height': '25–30 см',
                 'life_span': '12–15 лет'},
                {'name': 'Мейн-кун',
                 'desc': 'Одна из крупнейших домашних пород кошек.',
                 'weight': '6–11 кг',
                 'height': '25–41 см',
                 'life_span': '12–15 лет'}
            ]
            save_data(initial_data)
            return initial_data
    else:
        print(f"Файл не найден: {DATA_FILE}. Создаем новый файл.")
        initial_data = [
            {'name': 'Сибирская кошка',
             'desc': 'Одна из старейших русских пород кошек.',
             'weight': '4–10 кг',
             'height': '25–38 см',
             'life_span': '12–16 лет'},
            {'name': 'Британская короткошёрстная',
             'desc': 'Известна своей спокойной натурой и густым мехом.',
             'weight': '4–8 кг',
             'height': '25–30 см',
             'life_span': '12–17 лет'},
            {'name': 'Сфинкс',
             'desc': 'Безволосые кошки с большими ушами и выразительными глазами.',
             'weight': '3–6 кг',
             'height': '23–30 см',
             'life_span': '10–15 лет'},
            {'name': 'Русская голубая',
             'desc': 'Изящная кошка с короткой серовато-голубоватой шерстью.',
             'weight': '3–6 кг',
             'height': '25–30 см',
             'life_span': '12–15 лет'},
            {'name': 'Мейн-кун',
             'desc': 'Одна из крупнейших домашних пород кошек.',
             'weight': '6–11 кг',
             'height': '25–41 см',
             'life_span': '12–15 лет'}
        ]
        save_data(initial_data)
        return initial_data

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

data = load_data()

grouped_data = defaultdict(list)
for cat in data:
    first_letter = cat['name'][0].upper()
    grouped_data[first_letter].append(cat)

theme_colors = {
    'light': {'bg': '#fafafa', 'fg': '#333'},
    'dark': {'bg': '#333', 'fg': '#fff'}
}

current_theme = 'light'

def change_theme():
    global current_theme
    new_theme = 'dark' if current_theme == 'light' else 'light'
    root.configure(bg=theme_colors[new_theme]['bg'])
    main_frame.configure(bg=theme_colors[new_theme]['bg'])
    categories_menu.configure(bg=theme_colors[new_theme]['bg'], fg=theme_colors[new_theme]['fg'])
    theme_button.configure(bg=theme_colors[new_theme]['bg'], fg=theme_colors[new_theme]['fg'])
    canvas.config(bg=theme_colors[new_theme]['bg'])
    canvas.delete("all")
    for window in root.winfo_children():
        if isinstance(window, tk.Toplevel):
            apply_theme_to_toplevel(window, new_theme)
    current_theme = new_theme

def apply_theme_to_toplevel(window, theme):
    window.configure(bg=theme_colors[theme]['bg'])
    for widget in window.winfo_children():
        if isinstance(widget, tk.Label):
            widget.configure(bg=theme_colors[theme]['bg'], fg=theme_colors[theme]['fg'])
        elif isinstance(widget, tk.Listbox):
            widget.configure(bg=theme_colors[theme]['bg'], fg=theme_colors[theme]['fg'])
        elif isinstance(widget, tk.Button):
            widget.configure(bg=theme_colors[theme]['bg'], fg=theme_colors[theme]['fg'])

def show_cat_info(category_name):
    top_window = tk.Toplevel(root)
    center_window(top_window, 600, 400)
    top_window.title(f"Породы кошек ({category_name})")

    def display_description(index):
        cat = grouped_data[category_name][index]
        detail_window = tk.Toplevel(top_window)
        center_window(detail_window, 800, 400)
        detail_window.title(f"Подробности о {cat['name']}")
        # Формирование полного пути к изображению из директории IMAGE_DIR и имени файла из JSON
        image_filename = cat.get("image_path", "")
        try:
            if image_filename:
                full_image_path = os.path.join(IMAGE_DIR, image_filename)
                img = Image.open(full_image_path)
                resized_img = img.resize((200, 200), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(resized_img)
                image_label = tk.Label(detail_window, image=photo)
                image_label.photo = photo  # Сохраняем ссылку для предотвращения удаления сборщиком мусора
                image_label.pack(padx=10, pady=10)
            else:
                raise ValueError("Путь к изображению не указан в JSON")
        except Exception as e:
            print(f"Ошибка при загрузке изображения: {e}")

        title = f"{cat['name']}"
        rest = f"\nОписание: {cat['desc']}\nВес: {cat['weight']}, Рост: {cat['height']}, Продолжительность жизни: {cat['life_span']}"
        title_label = tk.Label(detail_window, text=title, font=("Segoe UI", 12, "bold"))
        title_label.pack(padx=10, pady=10)
        detail_label = tk.Label(detail_window, text=rest, font=("Segoe UI", 12))
        detail_label.pack(padx=10, pady=10)

        apply_theme_to_toplevel(detail_window, current_theme)

    list_box = tk.Listbox(top_window, font=("Segoe UI", 12))
    list_box.pack(fill=tk.BOTH, expand=True)
    for i, cat in enumerate(grouped_data[category_name]):
        list_box.insert(i, cat['name'])
        list_box.itemconfig(i, bg=theme_colors[current_theme]['bg'], fg=theme_colors[current_theme]['fg'])
    list_box.bind('<<ListboxSelect>>', lambda e:
                 display_description(int(e.widget.curselection()[0])) if e.widget.curselection() else None)
    info_label = tk.Label(top_window, wraplength=500, justify=tk.LEFT,
                          font=("Segoe UI", 12), highlightthickness=0, borderwidth=0)
    info_label.pack(padx=10, pady=10)
    apply_theme_to_toplevel(top_window, current_theme)

root = tk.Tk()
center_window(root, 800, 600)
root.title("Энциклопедия Кошек ₍^. .^₎⟆")

canvas = tk.Canvas(root, width=300, height=300, highlightthickness=0)
canvas.place(relx=0.5, rely=0.5, anchor="center")

animation_frames = []
img = Image.open(ANIMATION_PATH)
frames_count = img.n_frames
for frame_number in range(frames_count):
    img.seek(frame_number)
    animation_frames.append(ImageTk.PhotoImage(img.copy()))
frame_number = 0
def animate_gif():
    global frame_number
    canvas.delete("all")
    canvas.create_image(canvas.winfo_width()/2, canvas.winfo_height()/2, image=animation_frames[frame_number], tags="animated")
    frame_number += 1
    if frame_number >= frames_count:
        frame_number = 0
    root.after(100, animate_gif)
animate_gif()

def main():
    main_frame = tk.Frame(root, bd=2, relief=tk.GROOVE)
    main_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

    category_var = tk.StringVar(value=list(grouped_data.keys())[0])
    categories_menu = tk.OptionMenu(main_frame, category_var, *grouped_data.keys(),
                                    command=lambda x: show_cat_info(x))
    categories_menu.pack(fill=tk.X, side=tk.TOP, anchor=tk.NW)

    theme_button = tk.Button(main_frame, text=" ≽^◕⩊◕ ^≼ Изменить тему", command=change_theme)
    theme_button.pack(side=tk.BOTTOM, anchor=tk.SE)

    root.mainloop()
if __name__ == "__main__":
  main()
