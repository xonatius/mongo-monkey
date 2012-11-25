from pymongo.collection import Collection as PyMongoCollection

from mongomonkey.cursor import Cursor
from mongomonkey.model import Model


class Collection(PyMongoCollection):

    # TODO: Think about merging *_object functions with original pymongo function

    def save_object(self, obj, manipulate=True,
                    safe=None, check_keys=True, **kwargs):
        if not isinstance(obj, Model):
            raise TypeError("Type of obj should be a subclass of Model class")

        obj['_id'] = self.save(obj, manipulate=manipulate, safe=safe, check_keys=check_keys, **kwargs)
        return obj['_id']

    def insert_objects(self, obj_or_objs, manipulate=True,
                       safe=None, check_keys=True, continue_on_error=False, **kwargs):
        ids = self.insert(obj_or_objs, manipulate=manipulate, safe=safe, check_keys=check_keys, continue_on_error=continue_on_error, **kwargs)

        for obj, id in zip(tuple(obj_or_objs), tuple(ids)):
            obj['_id'] = id

        return ids

    def update_object(self, obj, manipulate=False, safe=None, check_keys=True, **kwargs):
        if '_id' not in obj:
            raise ValueError("Updating object %(object)s doesn't contain _id field. Seems like it wasn't saved before." % {'object': obj})
        # TODO: Currently it update whole document instead of changed fields. In future it should be changed.
        id = obj['_id']
        return self.update({'_id': id}, obj, manipulate=manipulate, safe=safe, check_keys=check_keys, **kwargs)

    def remove_object(self, obj, safe=None, **kwargs):
        if '_id' not in obj:
            raise ValueError("Removing object %(object)s doesn't contain _id field. Seems like it wasn't saved before." % {'object': obj})
        id = obj['_id']
        return self.remove({'_id': id}, safe=safe, **kwargs)

    def find(self, *args, **kwargs):
        """Query the database.

        The `spec` argument is a prototype document that all results
        must match. For example:

        >>> db.test.find({"hello": "world"})

        only matches documents that have a key "hello" with value
        "world".  Matches can have other keys *in addition* to
        "hello". The `fields` argument is used to specify a subset of
        fields that should be included in the result documents. By
        limiting results to a certain subset of fields you can cut
        down on network traffic and decoding time.

        Raises :class:`TypeError` if any of the arguments are of
        improper type. Returns an instance of
        :class:`~pymongo.cursor.Cursor` corresponding to this query.

        :Parameters:
          - `spec` (optional): a SON object specifying elements which
            must be present for a document to be included in the
            result set
          - `fields` (optional): a list of field names that should be
            returned in the result set ("_id" will always be
            included), or a dict specifying the fields to return
          - `skip` (optional): the number of documents to omit (from
            the start of the result set) when returning the results
          - `limit` (optional): the maximum number of results to
            return
          - `timeout` (optional): if True, any returned cursor will be
            subject to the normal timeout behavior of the mongod
            process. Otherwise, the returned cursor will never timeout
            at the server. Care should be taken to ensure that cursors
            with timeout turned off are properly closed.
          - `snapshot` (optional): if True, snapshot mode will be used
            for this query. Snapshot mode assures no duplicates are
            returned, or objects missed, which were present at both
            the start and end of the query's execution. For details,
            see the `snapshot documentation
            <http://dochub.mongodb.org/core/snapshot>`_.
          - `tailable` (optional): the result of this find call will
            be a tailable cursor - tailable cursors aren't closed when
            the last data is retrieved but are kept open and the
            cursors location marks the final document's position. if
            more data is received iteration of the cursor will
            continue from the last document received. For details, see
            the `tailable cursor documentation
            <http://www.mongodb.org/display/DOCS/Tailable+Cursors>`_.
          - `sort` (optional): a list of (key, direction) pairs
            specifying the sort order for this query. See
            :meth:`~pymongo.cursor.Cursor.sort` for details.
          - `max_scan` (optional): limit the number of documents
            examined when performing the query
          - `as_class` (optional): class to use for documents in the
            query result (default is
            :attr:`~pymongo.connection.Connection.document_class`)
          - `slave_okay` (optional): if True, allows this query to
            be run against a replica secondary.
          - `await_data` (optional): if True, the server will block for
            some extra time before returning, waiting for more data to
            return. Ignored if `tailable` is False.
          - `partial` (optional): if True, mongos will return partial
            results if some shards are down instead of returning an error.
          - `manipulate`: (optional): If True (the default), apply any
            outgoing SON manipulators before returning.
          - `network_timeout` (optional): specify a timeout to use for
            this query, which will override the
            :class:`~pymongo.connection.Connection`-level default
          - `read_preference` (optional): The read preference for
            this query.
          - `tag_sets` (optional): The tag sets for this query.
          - `secondary_acceptable_latency_ms` (optional): Any replica-set
            member whose ping time is within secondary_acceptable_latency_ms of
            the nearest member may accept reads. Default 15 milliseconds.

        .. note:: The `manipulate` parameter may default to False in
           a future release.

        .. note:: The `max_scan` parameter requires server
           version **>= 1.5.1**

        .. versionadded:: 2.3
           The `tag_sets` and `secondary_acceptable_latency_ms` parameters.

        .. versionadded:: 1.11+
           The `await_data`, `partial`, and `manipulate` parameters.

        .. versionadded:: 1.8
           The `network_timeout` parameter.

        .. versionadded:: 1.7
           The `sort`, `max_scan` and `as_class` parameters.

        .. versionchanged:: 1.7
           The `fields` parameter can now be a dict or any iterable in
           addition to a list.

        .. versionadded:: 1.1
           The `tailable` parameter.

        .. mongodoc:: find
        """
        if not 'slave_okay' in kwargs:
            kwargs['slave_okay'] = self.slave_okay
        if not 'read_preference' in kwargs:
            kwargs['read_preference'] = self.read_preference
        if not 'tag_sets' in kwargs:
            kwargs['tag_sets'] = self.tag_sets
        if not 'secondary_acceptable_latency_ms' in kwargs:
            kwargs['secondary_acceptable_latency_ms'] = (
                self.secondary_acceptable_latency_ms)
        return Cursor(self, *args, **kwargs)
