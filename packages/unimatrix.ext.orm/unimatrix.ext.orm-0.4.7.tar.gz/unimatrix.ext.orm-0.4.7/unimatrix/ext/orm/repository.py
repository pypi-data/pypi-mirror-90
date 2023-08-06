"""Declares :class:`RelationalDatabaseRepository`."""
import ioc


class RelationalDatabaseRepository:
    """A repository implementation for use with :mod:`sqlalchemy`."""
    session_factory = 'AsyncSessionFactory'

    @property
    def exists_query(self):
        raise NotImplementedError

    @property
    def factory(self):
        raise NotImplementedError

    @property
    def reconstruct_query(self):
        raise NotImplementedError

    async def get(self, **params):
        """Reconstruct a domain object that is identified by the given
        parameters.
        """
        q = self.get_reconstruct_query(**params)
        return self.factory.fromdao(await self.query(q))

    def get_exists_query(self, *args, **kwargs):
        """Return a boolean indicating if an entity exists. Must return
        a :class:`sqlalchemy.sql.selectable.Exists` instance.
        """
        return self.exists_query(*args, **kwargs)

    def get_reconstruct_query(self, *args, **kwargs):
        """Return a :class:`~unimatrix.ext.orm.query.NamedQuery` instance
        that fetches the data to reconstruct a single domain entity.
        """
        return self.reconstruct_query(*args, **kwargs)

    async def execute_query(self, q):
        return await self.session.execute(q)

    async def exists(self, **params):
        return await self.query(self.get_exists_query(**params))

    async def persist_declarative(self, dao, flush=False, merge=False):
        if merge:
            dao = await self.session.merge(dao)
        else:
            self.session.add(dao)
        if flush:
            await self.session.flush()
        return dao

    async def query(self, q):
        """Run a :class:`~unimatrix.ext.orm.query.Query` and return
        the result(s).
        """
        return await q.run(self.session)

    async def __aenter__(self):
        self._manages_session = False
        if getattr(self, 'session', None) is None:
            if isinstance(self.session_factory, str):
                self.session = ioc.require(self.session_factory)()
            elif callable(self.session_factory):
                self.session = self.session_factory()
            else:
                raise NotImplementedError(
                    'Provide an inversion-of-control key as the session_factory'
                    ' attribute or implement it as a method.'
                )

        self._manages_session = not self.session.sync_session.in_transaction()

        # Determine if there is a transaction running. If a transaction is
        # running, start a savepoint, else begin a new one.
        begin = self.session.begin
        if not self._manages_session:
            begin = self.session.begin_nested
        self.tx = begin()
        await self.tx.__aenter__()
        return self

    async def __aexit__(self, cls, exc, tb):
        try:
            # self.tx is not set if an exception was raised due to
            # improperly configured inversion-of-control.
            if hasattr(self, 'tx'):
                await self.tx.__aexit__(cls, exc, tb)
        finally:
            if self._manages_session:
                await self.session.close()

