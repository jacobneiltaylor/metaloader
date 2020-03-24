from .stanza_handler import TypedStanzaHandler


class DictStanzaHandler(TypedStanzaHandler, register="dict"):
    @property
    def _type(self):
        return dict

    def _merge(self, stanza_data: dict, new_data: dict):
        stanza_data.update(new_data)
