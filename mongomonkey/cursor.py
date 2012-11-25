from pymongo.cursor import Cursor as PyMongoCursor
from pymongo.read_preferences import ReadPreference

class Cursor(PyMongoCursor):

    def __init__(self, collection, spec=None, fields=None, skip=0, limit=0,
                 timeout=True, snapshot=False, tailable=False, sort=None,
                 max_scan=None, as_class=None, slave_okay=False,
                 await_data=False, partial=False, manipulate=True,
                 read_preference=ReadPreference.PRIMARY, tag_sets=[{}],
                 secondary_acceptable_latency_ms=None,
                 _must_use_master=False, _uuid_subtype=None, model=None, **kwargs):
        """Create a new cursor.

        Should not be called directly by application developers - see
        :meth:`~pymongo.collection.Collection.find` instead.

        .. mongodoc:: cursors
        """

        self.__model = model
        super(Cursor, self).__init__(collection, spec=spec, fields=fields, skip=skip, limit=limit,
            timeout=timeout, snapshot=snapshot, tailable=tailable, sort=sort,
            max_scan=max_scan, as_class=as_class, slave_okay=slave_okay,
            await_data=await_data, partial=partial, manipulate=manipulate,
            read_preference=read_preference, tag_sets=tag_sets,
            secondary_acceptable_latency_ms=secondary_acceptable_latency_ms,
            _must_use_master=_must_use_master, _uuid_subtype=_uuid_subtype, **kwargs)

    # TODO: Should optionally include only necessary fields
    def map_to(self, model):
        self.__model = model
        return self


    def clone(self):
        """Get a clone of this cursor.

        Returns a new Cursor instance with options matching those that have
        been set on the current instance. The clone will be completely
        unevaluated, even if the current instance has been partially or
        completely evaluated.
        """
        copy = Cursor(self.__collection, self.__spec, self.__fields,
            self.__skip, self.__limit, self.__timeout,
            self.__snapshot, self.__tailable)
        copy.__ordering = self.__ordering
        copy.__explain = self.__explain
        copy.__hint = self.__hint
        copy.__batch_size = self.__batch_size
        copy.__max_scan = self.__max_scan
        copy.__as_class = self.__as_class
        copy.__slave_okay = self.__slave_okay
        copy.__await_data = self.__await_data
        copy.__partial = self.__partial
        copy.__manipulate = self.__manipulate
        copy.__read_preference = self.__read_preference
        copy.__tag_sets = self.__tag_sets
        copy.__secondary_acceptable_latency_ms = (
            self.__secondary_acceptable_latency_ms)
        copy.__must_use_master = self.__must_use_master
        copy.__uuid_subtype = self.__uuid_subtype
        copy.__query_flags = self.__query_flags
        copy.__kwargs = self.__kwargs
        copy.__model = self.__model
        return copy

    def __getitem__(self, index):
        if issubclass(index, slice):
            return super(Cursor, self).__getitem__(index)
        else:
            document = super(Cursor, self).__getitem__(index)
            if self.__model is not None:
                return self.__model.from_mongo(document)
            return document

    def next(self):
        document = super(Cursor, self).next()

        if self.__model is not None:
            return self.__model.from_mongo(document)
        return document
