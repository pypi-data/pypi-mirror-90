"""This module includes base services classes

Notes
-----
To use services you need to create `services.py` module in your app and
create `BaseService` subclasses into this. Services must have `model`
attribute and `strategy_class` if it's not setted in service class and if
you want to use strategies in your service

"""

from __future__ import annotations

from typing import Any

from django.forms import Form

from .strategies import CommonCRUDStrategy, UserCRUDStrategy


class BaseService:
    """Base class for all services

    Attributes
    ----------
    strategy_class : BaseStrategy
        A BaseStrategy subclass with mutable functionality
    model : Model
        A model using in service logic
    self.strategy : strategy_class instance
        A BaseStrategy instance created in constructor using
        strategy_class

    Examples
    --------
    To use this service you need to subclass it and set model
    and strategy_class attributes if you want to use strategies in
    your service:

    >>> class MyService(BaseService):
    ...     model = MyModel
    ...     strategy_class = MyStrategy
    ...
    ...     def do_some_logic(self, *args, **kwargs):
    ...         return self.strategy.do_some_logic(*args, **kwargs)
    ...

    If arguments other than `model` must be passed to the constructor
    of your strategy you can add them to the get_strategy_args() method:

    >>> class MyService(BaseService):
    ...     model = MyModel
    ...     strategy_class = MyStrategy
    ...     another_attribute = Something
    ...
    ...     def get_strategy_init_args(self):
    ...         args = (self.another_attribute,)
    ...         return super().get_strategy_init_args() + args
    ...

    Or if you want to use service without strategy you can just define
    model attribute:

    >>> class MyService(BaseService):
    ...     model = MyModel
    ...
    ...     def do_some_logic(self):
    ...         pass
    ...

    """

    strategy_class = None
    model = None

    def __init__(self) -> None:
        if not self.model:
            raise AttributeError("You need to set `model` attribute")

        if self.strategy_class:
            self.strategy = self.strategy_class(
                *self.get_strategy_init_args()
            )

    def get_strategy_init_args(self) -> tuple:
        """Return tuple with arguments for strategy constructor

        Returns
        -------
        Tuple with model attribute value. It's default behavior

        """
        return (self.model,)


class BaseCRUDService(BaseService):
    """Base class for CRUD services

    Attributes
    ----------
    Each CRUD service must define the following attributes:

    strategy_class : BaseStrategy subclass
        Strategy class with CRUD functionality realization
    model : Model
        Django model service works with

    Methods
    -------
    All these methods are default for CRUD strategies. In this service
    all these methods delegate control to strategy methods

    get_all()
        Returns all model entries
    get_concrete()
        Returns a concrete model entry
    create()
        Creates a new model entry
    change()
        Changes a concrete model entry
    delete()
        Deletes a concrete model entry

    Examples
    --------
    If your CRUD strategy doesn't have other than default 5 methods
    you can just subclass this class and define `strategy_class` and
    `model` attributes:

    >>> class MyCRUDService(BaseCRUDService):
    ...     strategy_class = MyCRUDStrategy
    ...     model = MyModel
    ...

    But if your CRUD strategy has other than default methods you need to
    define non-default methods in your service and delegate control to
    strategy in them

    >>> class MyCRUDService(BaseCRUDService):
    ...     strategy_class = MyCRUDStrategy
    ...     model = MyModel
    ...
    ...     def do_some_logic(self, *args, **kwargs):
    ...         return self.strategy.do_some_logic(*args, **kwargs)

    """

    strategy_class = None
    model = None

    def __init__(self) -> None:
        if not self.strategy_class:
            raise AttributeError(
                "You need to set `strategy_class` attribute"
            )

        super().__init__()

    def get_all(self, *args, **kwargs) -> Any:
        return self.strategy.get_all(*args, **kwargs)

    def get_concrete(self, *args, **kwargs) -> Any:
        return self.strategy.get_concrete(*args, **kwargs)

    def create(self, *args, **kwargs) -> Any:
        return self.strategy.create(*args, **kwargs)

    def change(self, *args, **kwargs) -> Any:
        return self.strategy.change(*args, **kwargs)

    def delete(self, *args, **kwargs) -> Any:
        return self.strategy.delete(*args, **kwargs)


class CommonCRUDService(BaseCRUDService):
    """Service with CRUD functionality using CommonCRUDStrategy

    Attributes
    ----------
    strategy_class : CommonCRUDStrategy
        Strategy with CRUD functionality

    Examples
    --------
    To use this services you need to subclass it and set model attribute:

    >>> class MyService(CRUDService):
    ...     model = MyModel
    ...

    After that you can use this service in Django views. For example,
    you can make Django's ListView analog:

    >>> def list_view(request):
    ...     service = MyService()
    ...     entries = service.get_all()
    ...     return render(request, 'entries.html', {'entries': entries})
    ...

    """

    strategy_class = CommonCRUDStrategy


class UserCRUDService(BaseCRUDService):
    """Service with CRUD functionality using UserCRUDStrategy

    Attributes
    ----------
    strategy_class : UserCRUDStrategy
        Strategy with CRUD functionality
    user_field_name : str
        Name of user field in model. By default it's just user

    Examples
    --------
    To use this services you need to subclass it and set model attribute.
    And if your model user field has other than 'user' name you can
    define this name in user_field_name attribute:

    >>> class MyService(CRUDService):
    ...     model = MyModel
    ...     user_field_name = 'author'
    ...

    After that you can use this service in Django views. For example,
    you can make Django's ListView analog:

    >>> def list_view(request):
    ...     service = MyService()
    ...     entries = service.get_all(request.user)
    ...     return render(request, 'entries.html', {'entries': entries})
    ...

    """

    strategy_class = UserCRUDStrategy
    user_field_name = 'user'

    def get_strategy_init_args(self) -> tuple:
        """Extend default init kwargs with user_field_name"""
        return super().get_strategy_init_args() + (self.user_field_name,)
