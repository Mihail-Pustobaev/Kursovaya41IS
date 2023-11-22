import os
from tkinter import *
from tkinter import font
from tkinter import filedialog as fd
from tkinter.ttk import Notebook
from tkinter import messagebox as mb
import nnReading
from PIL import Image, ImageTk, ImageOps

#КЛАСС ОКНА ТКИНТЕР
class MainTkinterClass:
    def __init__(self):
        self.root = Tk()
        self.image_tabs = Notebook(self.root)  # нотбук для вкладок картинок
        self.opened_images = [] # массив для хранения открытых вкладок
        self.root.iconbitmap('resources/logoPK.ico')
        self.mainFont = font.Font(size=15)
        self.root.configure(background="#DEB887")
        self.lbl = Label(text="Чтение текста с фото", font=self.mainFont, background="#DEB887")
        self.lbl.pack()

        self.root.state("zoomed")

        self.selection_x = 0
        self.selection_y = 0
        self.selection_bottom_x = 0
        self.selection_bottom_y = 0
        self.canvas_for_selection = None
        self.selection_rect = None

        self.init()


    #МЕТОД ИНИЦИАЛИЗАЦИИ
    def init(self):
        self.root.title("Чтение документов")
        #self.root.iconphoto()

        self.image_tabs.enable_traversal() # ПОЗВОЛЯЕТ МАНИПУЛИРОВАТЬ С NOTEBOOK С ПОМОЩЬЮ КЛАВИАТУРЫ

        self.root.bind("<Escape>", self._close) # бинд кнопки эскейп на выход
        self.root.bind("<Control-a>", self.open_new_images)
        self.root.bind("<Control-d>", self.start_selection_of_current_image)
        self.root.bind("<Control-f>", self.stop_selection)
        self.root.bind("<Control-c>", self.save_as)
        self.root.bind("<Control-s>", self.save_curren_img)
        self.root.bind("<Control-g>", self.read_img)

    def run(self): # метод прорисовки приложения
        self.draw_menu() #нарисовать меню ("Файл")
        self.draw_widjets() #нарисовать все виджиты

        self.root.mainloop()

    def draw_menu(self):
        menu_bar = Menu(self.root) # меню ("Файл")

        file_menu = Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Открыть (Control+A)", command=self.open_new_images) # вкладка в меню для открытия файла
        file_menu.add_command(label="Сохранить как (Control+C)", command=self.save_as)
        file_menu.add_command(label="Сохранить (Control+S)", command=self.save_curren_img)
        file_menu.add_command(label="Прочитать (Control+G)", command=self.read_img)
        file_menu.add_separator()
        file_menu.add_command(label="Выход (Esc)", command=self._close)
        menu_bar.add_cascade(label="Файл", menu=file_menu)

        edit_menu = Menu(menu_bar, tearoff=0)

        transfrom_menu = Menu(edit_menu, tearoff=0)
        transfrom_menu.add_command(label="Повернуть влево на 90", command=lambda: self.rotate_current_img(90))
        transfrom_menu.add_command(label="Повернуть вправо на 90", command=lambda: self.rotate_current_img(270))
        transfrom_menu.add_command(label="Повернуть на 180", command=lambda: self.rotate_current_img(180))
        edit_menu.add_cascade(label="Преобразовать", menu=transfrom_menu)

        resize_menu = Menu(edit_menu, tearoff=0)
        resize_menu.add_command(label='25% от текущего размера', command=lambda:self.resize_current_image(25))
        resize_menu.add_command(label='50% от текущего размера', command=lambda: self.resize_current_image(50))
        resize_menu.add_command(label='75% от текущего размера', command=lambda: self.resize_current_image(75))
        resize_menu.add_command(label='125% от текущего размера', command=lambda: self.resize_current_image(125))
        resize_menu.add_command(label='150% от текущего размера', command=lambda: self.resize_current_image(150))
        resize_menu.add_command(label='200% от текущего размера', command=lambda: self.resize_current_image(200))

        edit_menu.add_cascade(label="Изменить размер", menu=resize_menu)

        flip_menu = Menu(edit_menu, tearoff=0)
        flip_menu.add_command(label="Отзеркалить по горизонту", command=lambda: self.flip_current_image("horizon"))
        flip_menu.add_command(label="Отзеркалить по вертикали", command=lambda: self.flip_current_image("vertical"))
        edit_menu.add_cascade(label="Отзеркалить", menu=flip_menu)

        crop_menu = Menu(edit_menu, tearoff=0)
        crop_menu.add_command(label="Выделить область (Control+D)", command=self.start_selection_of_current_image)
        crop_menu.add_command(label="Обрезать область (Control+F)", command=self.stop_selection)
        edit_menu.add_cascade(label="Выделить", menu=crop_menu)

        menu_bar.add_cascade(label="Редактировать", menu=edit_menu)

        help_menu = Menu(menu_bar, tearoff=0)

        help_menu.add_command(label='Помощь', command=self.show_help)

        menu_bar.add_cascade(label='Помощь', menu=help_menu)


        self.root.configure(menu=menu_bar)

    def show_help(self):
        mb.showinfo(title='Помощь', message="Данное ПО разработано для редактирования изображений файлов с текстом и последующим их чтением. Для начала работы нажмите на 'Файл' и нажмите открыть. После чего выберите картинку с форматом jpg, jpeg или png. После отредактируйте данную картинку используя инструментарий ПО, который находится во вкладке 'Редактировать'."
                                            " После этого этого сохраните данную картинку, нажав на 'Файл', 'Сохранить как' и укажите путь и название сохранённого файла под новым именем, либо же нажмите кнопку 'Сохранить', для сохранения текущего файла. После этого нажмите на кнопку 'Прочитать', после чего укажите путь до нужной картинки. После этого ПО сообщит вам, что файл прочитан и сохранён в папку 'outImgText', которая находится в корневой папке ПО (полный путь до папки ПО вам напишет). Текст сохраняется в формате docx и txt.")

    def draw_widjets(self): # прорисовка виждитов
        self.image_tabs.pack(fill="both", expand=1)

    def open_new_images(self, event=None):
        image_paths = fd.askopenfilenames(filetypes=(("Images", "*.jpeg; *.jpg; *.png"),)) # открытие картинок

        for image_path in image_paths:
            self.add_new_image(image_path) # метод открытия картинок и добавление их в открытые вкладки


    def add_new_image(self, image_path):
        # Получите размеры экрана
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        image = Image.open(image_path) # открытие картинки PIL

        w, h = image.size


        if w > screen_width or h > screen_height:
            # Уменьшите ширину и высоту изображения пропорционально,
            # чтобы оно сохранило соотношение сторон
            ratio = min(screen_width / w, screen_height / h)
            new_width = int(w * ratio)
            new_height = int(h * ratio)

            # Масштабируйте изображение до новых размеров
            image = image.resize((new_width, new_height - 200))

        image_tk = ImageTk.PhotoImage(image)  # открытие картинки Tk

        self.opened_images.append([image_path, image]) # добавление в октрытые вкладки

        image_tab = Frame(self.image_tabs)

        image_panel = Canvas(image_tab, width=image_tk.width(), height=image_tk.height(), bd=0, highlightthickness=0)  # прорисовка картинки
        image_panel.image = image_tk
        image_panel.create_image(0,0, image=image_tk, anchor="nw")
        image_panel.pack(expand=1)

        self.image_tabs.add(image_tab, text=image_path.split('/')[-1])
        self.image_tabs.select(image_tab)

    def save_curren_img(self, event=None):
        current_tab = self.image_tabs.select()
        if not current_tab:
            return
        tab_number = self.image_tabs.index(current_tab)
        path, image = self.opened_images[tab_number]
        if path[-1] == "*":
            path = path[:-1]
            self.opened_images[tab_number][0] = path
            image.save(path)
            self.image_tabs.add(current_tab, text=path.split('/')[-1])

    def flip_current_image(self, flip_type):
        current_tab = self.image_tabs.select()
        if not current_tab:
            return

        tab_number = self.image_tabs.index(current_tab)

        image = self.opened_images[tab_number][1]

        if flip_type == "horizon":
            image = ImageOps.mirror(image)
        elif flip_type == "vertical":
            image = ImageOps.flip(image)

        self.update_current_image(current_tab, image)

    def save_as(self, event=None):
        current_tab =self.image_tabs.select()
        if not current_tab:
            return

        tab_number = self.image_tabs.index(current_tab)
        old_path, old_ext = os.path.splitext(self.opened_images[tab_number][0])

        if old_ext[-1] == "*":
            old_ext = old_ext[:-1]

        new_path = fd.asksaveasfilename(initialdir=old_path, filetypes=(("Images", "*.jpeg; *.jpg; *.png"),))

        if not new_path:
            return

        new_path, new_ext = os.path.splitext(new_path)

        if not new_ext:
            new_ext = old_ext
        elif old_ext != new_ext:
            mb.showerror("Неправильное разрешение файла", f"Получено неправильное разрешение: {new_ext}. Старое разрешение: {old_ext}")
            return

        image = self.opened_images[tab_number][1]
        image.save(new_path + new_ext)
        image.close()

        del self.opened_images[tab_number]
        self.image_tabs.forget(current_tab)

        self.add_new_image(new_path+new_ext)

    def rotate_current_img(self, degrees):
        current_tab = self.image_tabs.select()
        if not current_tab:
            return

        tab_number = self.image_tabs.index(current_tab)

        image = self.opened_images[tab_number][1]
        image = image.rotate(degrees, expand=True)

        self.update_current_image(current_tab, image)

    def update_current_image(self, current_tab, image):
        tab_number = self.image_tabs.index(current_tab)
        self.opened_images[tab_number][1] = image

        tab_frame = self.image_tabs.children[current_tab[current_tab.rfind("!"):]]
        canvas = tab_frame.children["!canvas"]

        image_tk = ImageTk.PhotoImage(image)

        canvas.delete("all")
        canvas.image = image_tk

        canvas.configure(width=image_tk.width(), height=image_tk.height())
        canvas.create_image(0, 0, image=image_tk, anchor="nw")

        image_path = self.opened_images[tab_number][0]

        if image_path[-1] != "*":
            image_path += "*"
            self.opened_images[tab_number][0] = image_path
            image_name = image_path.split("/")[-1]
            self.image_tabs.tab(current_tab, text=image_name)

    def resize_current_image(self, percents):
        current_tab = self.image_tabs.select()
        if not current_tab:
            return

        tab_number = self.image_tabs.index(current_tab)
        image = self.opened_images[tab_number][1]

        w, h = image.size
        w = (w * percents) // 100
        h = (h * percents) // 100

        image = image.resize((w, h), Image.ADAPTIVE)

        self.update_current_image(current_tab, image)


    def start_selection_of_current_image(self, event=None):
        current_tab = self.image_tabs.select()
        if not current_tab:
            return

        tab_frame = self.image_tabs.children[current_tab[current_tab.rfind("!"):]]
        canvas = tab_frame.children["!canvas"]

        self.canvas_for_selection = canvas
        self.selection_rect = canvas.create_rectangle(self.selection_x, self.selection_y, self.selection_bottom_x, self.selection_bottom_y, dash=(10,10), fill='', outline="black", width=2)

        canvas.bind("<Button-1>", self.get_selection_start_pos)
        canvas.bind("<B1-Motion>", self.update_selection_by_pos)

    def get_selection_start_pos(self, event):
        self.selection_x, self.selection_y = event.x, event.y

    def update_selection_by_pos(self, event):
        self.selection_bottom_x, self.selection_bottom_y = event.x, event.y
        if self.canvas_for_selection is not None and self.selection_rect is not None:
            self.canvas_for_selection.coords(self.selection_rect, self.selection_x, self.selection_y, self.selection_bottom_x, self.selection_bottom_y)

    def stop_selection(self, event=None):
        if not self.canvas_for_selection:
            return

        self.canvas_for_selection.unbind("<Button-1>")
        self.canvas_for_selection.unbind("<B1-Motion>")

        self.canvas_for_selection.delete(self.selection_rect)

        self.crop_current_image()

        self.selection_rect = None
        self.canvas_for_selection = None
        self.selection_x, self.selection_y = 0,0
        self.selection_bottom_x, self.selection_bottom_y = 0, 0

    def crop_current_image(self):
        current_tab = self.image_tabs.select()
        if not current_tab:
            return

        tab_number = self.image_tabs.index(current_tab)
        image = self.opened_images[tab_number][1]

        image = image.crop((self.selection_x, self.selection_y, self.selection_bottom_x, self.selection_bottom_y))

        self.update_current_image(current_tab, image)

    def read_img(self, event=None):
        image_path = fd.askopenfilenames(filetypes=(("Images", "*.jpeg; *.jpg; *.png"),))  # открытие картинок
        if not image_path:
            return
        out_arr = nnReading.readFile(image_path[0])
        if out_arr[0]:
            mb.showinfo(title="ФАЙЛ ЗАПИСАН", message=f"Файл записан в {out_arr[1]}")
        else:
            mb.showinfo(title="Произошла ошибка", message=f"Ошибка: {out_arr[1]}")



    def _close(self, event=None): # бинд кнопки ескейп на выход
        self.root.quit()



if __name__=="__main__":
    MainTkinterClass().run() # запуска программы
