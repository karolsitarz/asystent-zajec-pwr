from tkinter import Label, Entry, Button, Frame, Tk, Text, END, WORD, messagebox
from tkinter.ttk import Checkbutton
from typing import Optional, Tuple, Union

from model.data.course import Course
from model.data.education_data import EducationData
from model.data.event import Event
from util.constants import ViewName
from views.education_data_form.education_data_form_adapter import EducationDataFormAdapter
from views.frame_view import FrameView


class EducationDataFormView(FrameView):
    def __init__(self, root: Tk):
        super().__init__(root, ViewName.EDUCATION_DATA_FORM)
        self.adapter = EducationDataFormAdapter()

        # START create layout
        parent = Frame(self)

        container_titles = Frame(parent)
        self.header = Label(container_titles, anchor="w")
        self.header.pack(fill="x")
        self.title = Label(container_titles, font="Arial 11 bold", anchor="w")
        self.title.pack(fill="x")
        self.subtitle = Label(container_titles, font="Arial 10 bold", anchor="w")
        self.subtitle.pack(fill="x")
        container_titles.pack(pady=10, padx=20, fill="x")

        container_name = Frame(parent)
        Label(container_name, text="Nazwa").pack()
        self.field_name = Entry(container_name)
        self.field_name.pack(pady=2, fill="x")
        self.field_name.bind("<Return>", self.submit_form)
        container_name.pack(pady=10, padx=20, fill="x")

        container_value = Frame(parent)
        Label(container_value, text="Zawartość").pack()
        self.field_value = Text(container_value, height=5, wrap=WORD)
        self.field_value.pack(pady=2, fill="x")
        container_value.pack(pady=10, padx=20, fill="x")

        self.field_is_url = Checkbutton(parent, text="Czy link URL")
        self.field_is_url.state(['!alternate'])
        self.field_is_url.pack(pady=2, padx=20)

        self.__errors = Label(parent, fg="red")
        self.__errors.pack(pady=5)

        container_buttons = Frame(parent)

        self.button_submit = Button(container_buttons, text="Zapisz", command=self.submit_form, padx=5)
        self.button_submit.pack(side="right")

        self.button_cancel = Button(container_buttons, text="Anuluj", command=self.cancel_form, padx=5)
        self.button_cancel.pack(side="right", padx=10)

        self.button_delete = Button(container_buttons, text="Usuń", command=self.delete_form, padx=5)
        self.button_delete.pack(side="left")

        container_buttons.pack(pady=5, padx=20, fill="x")

        parent.pack(expand=1)

        self.setup_observers()
        self.clear_fields()

    def setup_observers(self):
        def observe_errors(errors: list[str]):
            self.__errors["text"] = "\n".join(errors)
            self.update()

        self.adapter.errors.observe(observe_errors)

        def observe_selected_education_data(data: Tuple[Union[Course, Event], Optional[EducationData], bool]):
            (source, education_data, is_course) = data
            course: Course
            if is_course:
                course = source
                self.subtitle["text"] = "Kurs (globalnie)"
            else:
                event: Event = source
                course = event.course
                self.subtitle["text"] = f"Zajęcia {event.start.__str__()}"

            self.title["text"] = f"{course.type} {course.name}"

            if education_data is None:
                self.header["text"] = "Dodawanie notatki:"
                self.button_delete["state"] = "disabled"
                return

            self.button_delete["state"] = "normal"
            self.header["text"] = "Edycja notatki:"
            self.field_name.delete(0, END)
            self.field_name.insert(0, education_data.name)
            self.field_value.delete('1.0', END)
            self.field_value.insert('1.0', education_data.value)
            self.field_is_url.state(['selected'] if education_data.is_url else ['!selected'])

        self.adapter.selected.observe(observe_selected_education_data)

    def submit_form(self, _=None):
        name = self.field_name.get()
        value = self.field_value.get('1.0', 'end-1c')
        is_url = self.field_is_url.instate(['selected'])
        is_success = self.adapter.action_submit(name, value, is_url)
        if is_success:
            self.clear_fields()

    def cancel_form(self):
        self.adapter.action_cancel()
        self.clear_fields()

    def delete_form(self):
        response = messagebox.askyesno("Potwierdzenie", "Czy na pewno chcesz usunąć notatkę w kursie?")
        if not response:
            return
        self.adapter.action_delete()
        self.clear_fields()

    def clear_fields(self):
        self.adapter.errors.value = []
        self.field_name.delete(0, END)
        self.field_value.delete('1.0', END)
