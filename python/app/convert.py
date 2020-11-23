import copy
from app import db, Note
from typing import Dict, Any
from datetime import datetime

class NoteConverter(object):

  @staticmethod
  def _decode_dict(dict_to_decode: Dict[Any, Any]) -> Dict[Any, Any]:
    decoded_dict = dict()
    for k, v in dict_to_decode.items():
        if not isinstance(k, int):
            var = k.decode()
            decoded_dict[var] = v.decode()
    return decoded_dict

  @staticmethod
  def note_to_dict(note: Note) -> Dict[str, str]:
    # convert dict values to str
    return {k: str(v) for k, v in note.__dict__.items()}

  @staticmethod
  def dict_to_note(note_dict: Dict[str, str]) -> Note:
    note_dict = NoteConverter._decode_dict(note_dict)
    note_dict['id'] = int(note_dict['id'])
    note_dict['creation_date'] = datetime.strptime(note_dict['creation_date'], '%Y-%m-%d %H:%M:%S.%f')
    note_dict['edit_date'] = datetime.strptime(note_dict['edit_date'], '%Y-%m-%d %H:%M:%S.%f')
    note_dict['id_user'] = int(note_dict['id_user'])
    note_dict['is_public'] = bool(note_dict['is_public'])
    note_dict.pop('_sa_instance_state', None)
    return Note(**note_dict)
