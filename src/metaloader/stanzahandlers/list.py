from .stanza_handler import TypedStanzaHandler


class ListStanzaHandler(TypedStanzaHandler, register="list"):
    @property
    def _type(self):
        return list

    def _merge(self, stanza_data: list, new_data: list):
        stanza_data += new_data
