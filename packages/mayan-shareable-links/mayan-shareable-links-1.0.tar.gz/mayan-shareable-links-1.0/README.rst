===========
Description
===========

Mayan EDMS app to provide unique links to documents.


=======
License
=======

This project is open sourced under the `Apache 2.0 License`_.

.. _`Apache 2.0 License`: https://gitlab.com/mayan-edms/shareable-links/raw/master/LICENSE


============
Installation
============

#. Install from PyPI in the same ``virtualenv`` where you installed Mayan EDMS.
   Or if using the Docker image, pass ``mayan-shareable-links`` to the
   ``MAYAN_PIP_INSTALLS`` environment variable.

   .. code-block:: console

       pip install mayan-shareable-links

#. Add ``shareable_link`` to the ``COMMON_EXTRA_APPS`` setting, either as an
   environment variable, from a Python settings modules, or from the UI
   via the ``config.yaml`` configuration file.

   Python settings module example:

   .. code-block:: console

       INSTALLED_APPS += (
           'shareable_links',
       )

#. Run the migrations for the app (not required for the Docker image):

   .. code-block:: console

       mayan-edms.py migrate


============
Requirements
============

- **Mayan EDMS version 3.4**
