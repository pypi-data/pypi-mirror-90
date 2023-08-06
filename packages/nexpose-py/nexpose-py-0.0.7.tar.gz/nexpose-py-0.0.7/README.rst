nexpose-py
==========

Python3 bindings and CLI tools for the Nexpose API version 3.

cli programs
------------

nsc-exporter
~~~~~~~~~~~~

A `Prometheus <https://prometheus.io/>`_ exporter for
`Nexpose <https://www.rapid7.com/products/nexpose/>`_ scan console metrics.

A ``systemd`` service file is provided at
``etc/systemd/system/nexpose-exporter.service``,
and a sample env file at ``etc/defaults/nexpose-exporter.env``.
These will be relative to your virtualenv for a virtualenv install,
relative to ``$HOME/.local`` for a ``pip install --user`` install,
and (probably, depending on your OS) relative to ``/usr/local`` for a
root pip install.

nsc-remove-old-reports
~~~~~~~~~~~~~~~~~~~~~~

nsc-remove-old-sites
~~~~~~~~~~~~~~~~~~~~

library usage
~~~~~~~~~~~~~

Basic usage:

.. code-block:: python

    import nexpose.nexpose as nexpose

    login = nexpose.login(
        base_url='https://localhost:3780',
        user='some_nexpose_user',
        password='secure_nexpose_password',
    )

    nexpose.engines(nlogin=login)

For argument parsing:

.. code-block:: python

    parser = nexposeargs.parser
    parser.description = "My nexpose script"
    parser.add_argument(
        "-f",
        "--foo",
        help="foo argument",
        action="store",
    )

    args = parser.parse_args()

    base_url = ':'.join([args.baseurl, args.port])

    login = nexpose.login(
        base_url=base_url,
        user=args.user,
        password=args.password,
        verify=args.verify,
    )

alternatives
------------

``nexpose`` is the official python binding for Nexpose API versions 1.1 and 1.2

``nexpose-rest`` is unofficial. It is auto-generated and thus far more
comprehensive than ``nexpose-py``.
