from __future__ import annotations
from tinydb import TinyDB, Query
from typing import TypeVar, Generic, Type, List

T = TypeVar("T")


class TinyDbService(Generic[T]):
    """Class for managing entities using TinyDB as a JSON database"""

    """The TinyDB instance"""
    db: TinyDB

    """Constructor
    Type Parameters
    ---------------
    T - The type of model this controller manages
    Parameters
    ----------
    db: TinyDB
    The tinydb database to use
    modelClass: Type[T]
    The model class itself
    """

    def __init__(self, db: TinyDB, modelClass: Type[T]):
        """ Instantiate db and model """
        self.db = db
        self.modelClass = modelClass

    def find_all(self):
        """Fetch all documents from tinydb"""
        return [self.marshall(d) for d in self.db.all()]

    def find_by_element(self, elementKey: str, elementValue: str) -> T:
        """Return document matching a single key/value"""
        self.modelClass = Query()
        return self.db.search(getattr(self.modelClass, elementKey) == elementValue)

    def find_by_elements(self, query_dict: dict) -> List[T]:
        """Returns a document meeting all key/values of query dict"""
        return [self.marshall(doc) for doc in self.db.all() if query_dict.items() <= doc.items()]

    def insert(self, document: T):
        """Insert a document, returns the updated document"""
        if vars(document) not in self.db.all():
            id = self.db.insert(vars(document))
            document.id = id
            return document

    def find_by_id(self, id: int):
        """ Find doc by id """
        return self.marshall(self.db.get(doc_id=id))

    def remove_doc(self, id: int) -> List[int]:
        """Remove event by id from DB"""
        doc = self.db.remove(doc_ids=[id])
        return doc

    def update_event(self, updated_model: T, id: int):
        return self.db.update(updated_model.__dict__, Query().id == id, [id])


    def marshall(self, doc):
        """Marshall a model object from a tinydb document"""
        model = self.modelClass()
        for key in doc:
            setattr(model, key, doc[key])
        setattr(model, "id", doc.doc_id)
        return model
