.. :changelog:

History
-------

0.8.0 (2021-01-05)
--------------------

* Use serializer.instance instead of serializer.data

0.7.0 (2020-11-17)
--------------------

* Add perform_create method in CreateModelMixin

0.6.0 (2018-11-08)
--------------------

* Log full exception traceback in ExceptionMiddleware.
* Allow additional data to be passed to APIView.failure().

0.5.2 (2018-03-05)
--------------------

* Fix PublishExpireManager not being exported by publishable module.

0.5.1 (2018-03-05)
------------------

* Add PublishExpireManager.

0.5.0 (2018-02-06)
------------------

* Add AutoIntVersionSerializer

0.4.0 (2018-01-30)
------------------

* Add json_client fixture.
* Add rest_framework utils

0.3.0 (2018-01-26)
------------------

* Enforce Python 3.4 >= only in setup.py.
* Add PublishExpireMixin and PublishExpireQuerySet.

0.2.1 (2018-01-24)
------------------

* Re-upload to PyPI with an all lowercase name.

0.2.0 (2018-01-24)
------------------

* Add AutoIntVersionAdmin.

0.1.0 (2018-01-22)
------------------

* Add SoftDeletionMixin.
* Add AutoIntVersionMixin and AutoIntVersionField.
* Add CreatedUpdatedMixin, CreatedUpdatedSerializer and CreatedUpdatedAdmin.
* Add exception utils: raise_truthy, raise_falsey, raise_none.
* Add testing.client.JSONClient.

0.0.0 (2018-01-12)
------------------

* Initial commit.
