from flask_sqlalchemy import BaseQuery

from app import errors


class BaseQueryJSON(BaseQuery):
    """SQLAlchemy :class:`~sqlalchemy.orm.query.Query` subclass with convenience methods for querying in a web application.

    This is the default :attr:`~Model.query` object used for models, and exposed as :attr:`~SQLAlchemy.Query`.
    Override the query class for an individual model by subclassing this and setting :attr:`~Model.query_class`.
    """

    def get_or_raise(self, ident, description=None):
        """Like :meth:`get` but aborts with 404 if not found instead of returning ``None``."""

        rv = self.get(ident)
        if rv is None:
            # abort(format_error_response(EntityNotFound(self.column_descriptions[0]['name'], ident)))
            raise errors.EntityNotFound(self.column_descriptions[0]['name'], ident)
        return rv

    def first_or_raise(self, description=None):
        """Like :meth:`first` but aborts with 404 if not found instead of returning ``None``."""

        rv = self.first()
        if rv is None:
            # abort(format_error_response(NoDataFound(self.column_descriptions[0]['name'])))
            raise errors.NoDataFound(self.column_descriptions[0]['name'])
        return rv
