import floppy.models


class NoteOriginator:

    @staticmethod
    def take_snapshot(note):
        memento = NoteOriginator.save_state_to_memento(note=note)
        caretaker = floppy.models.NoteCareTaker.objects.get(note=note)
        caretaker.add(memento)

    @staticmethod
    def save_state_to_memento(note):
        memento = floppy.models.NoteMemento()
        memento.title = note.title
        memento.content = note.content
        return memento

    @staticmethod
    def get_state_from_memento(self, memento):
        return (memento.title, memento.content)
