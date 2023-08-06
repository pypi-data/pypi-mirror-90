"""This module includes base services strategies

Notes
-----
Each strategy must be a subclass of `BaseStrategy` class. Each strategy
has a `model` attribute to work with database. Strategies using in
services in `strategy` attribute

"""

from __future__ import annotations

from typing import Any, Union

from django.db.models import Model, QuerySet
from django.forms import Form, ModelForm
from django.shortcuts import get_object_or_404
from django.forms.models import construct_instance, model_to_dict
from django.contrib.auth import get_user_model


User = get_user_model


class BaseStrategy:
    """Base class for strategies

    Attributes
    ----------
    self.model : Model
        Model strategy works with. It's for working with DB

    Examples
    --------
    Strategies must be used in services. All you need is to create
    your strategy subclassing `BaseStrategy` and add it in `strategy_class`
    service attribute:

    >>> class MyStrategy(BaseStrategy):
    ...
    ...     def get_all(self):
    ...         return self.model.objects.all()
    ...
    ...
    ... class MyService(BaseService):
    ...     model = MyModel
    ...     strategy_class = MyStrategy
    ...
    ...     def get_all(self):
    ...         return self.strategy.get_all()
    ...

    """

    def __init__(self, model: Model) -> None:
        self.model = model


class CommonCRUDStrategy(BaseStrategy):
    """Strategy with common CRUD functionality

    Methods
    -------
    get_all()
        Get all model entries
    get_concrete(pk)
        Get a concrete model entry
    create(form_data)
        Create a new model entry
    change(changing_entry, form)
        Change a concrete model entry
    delete(deleting_entry)
        Delete a concrete model entry

    """

    def get_all(self) -> QuerySet:
        """Return all model entries"""
        return self.model.objects.all()

    def get_concrete(self, pk: Any) -> Model:
        """Return a concrete model entry with pk"""
        return get_object_or_404(self.model, pk=pk)

    def create(self, form_data: dict) -> Model:
        """Create a new model entry from form_data"""
        return self.model.objects.create(**form_data)

    def change(self, changing_entry: Model, form: Form) -> Model:
        """Change the changing_entry using form"""
        if isinstance(form, ModelForm):
            opts = form._meta
            changing_entry = construct_instance(
                form, changing_entry, opts.fields, opts.exclude
            )
        else:
            changing_entry = construct_instance(form, changing_entry)

        changing_entry.save()
        return changing_entry

    def delete(self, deleting_entry: Model) -> None:
        """Delete a concrete model entry from deleting_entry parameter"""
        deleting_entry.delete()


class UserCRUDStrategy(CommonCRUDStrategy):
    """Strategy with CRUD functionality using user

    Attributes
    ----------
    self.user_field_name : str
        Name of user field in model. By default it's just user

    Methods
    -------
    get_all(user)
        Get all model entries
    get_concrete(pk, user)
        Get a concrete model entry
    create(form_data, user)
        Create a new model entry

    """

    def __init__(self, model, user_field_name='user'):
        self.user_field_name = user_field_name
        super().__init__(model)

    def get_all(self, user: User) -> QuerySet:
        """Return all user entries"""
        user_kwarg = self._get_user_kwarg(user)
        return self.model.objects.filter(**user_kwarg)

    def get_concrete(self, pk: Any, user: User) -> Model:
        """Return a concrete model entry with pk"""
        user_kwarg = self._get_user_kwarg(user)
        return get_object_or_404(self.model, pk=pk, **user_kwarg)

    def create(self, form_data: dict, user: User) -> Model:
        """Create a new model entry from form_data"""
        user_kwarg = self._get_user_kwarg(user)
        return self.model.objects.create(**form_data, **user_kwarg)

    def _get_user_kwarg(self, user) -> dict:
        return {self.user_field_name: user}
