######
Models
######

.. module:: openclass.models

Workshop
========
.. class:: Workshop

  description

  .. attribute:: MAX_LEN_TITLE

    description

  .. attribute:: MAX_LEN_LOCATION

    description

  .. attribute:: INFINITE_SEATS_NB

    description

  .. attribute:: POL_FIFO

    description

  .. attribute:: POL_MANUAL

    description

  .. attribute:: POLITIC_CHOICES

    description

  .. attribute:: PENDING

    description

  .. attribute:: ACCEPTED

    description

  .. attribute:: REFUSED

    description

  .. attribute:: DONE

    description

  .. attribute:: CANCELED

    description

  .. attribute:: STATUS_CHOICES

    description

  .. attribute:: DEFAULT_PHOTO

    description

  .. attribute:: registered

    description

  .. attribute:: mc_questions

    description

  .. attribute:: animator

    description

  .. attribute:: topics

    description

  .. attribute:: decision_author

    description

  .. attribute:: title

    description

  .. attribute:: description

    description

  .. attribute:: required_materials

    description

  .. attribute:: objectives

    description

  .. attribute:: requirements

    description

  .. attribute:: seats_number

    description

  .. attribute:: submission_date

    description

  .. attribute:: decision_date

    description

  .. attribute:: start_date

    description

  .. attribute:: duration

    description

  .. attribute:: registration_politic

    description

  .. attribute:: location

    description

  .. attribute:: cover_img

    description

  .. attribute:: status

    description

  .. method:: end_date()

    description

    :return: description
    :rtype: datetime

  .. method:: count_registration()

    description

    :return: description
    :rtype: int

  .. method:: register(profile)

    description

    :param Profile profile: description
    :return: description
    :rtype: bool

  .. method:: is_registration_open()

    description

    :return: description
    :rtype: bool

  .. method:: last_registration_date()

    description

    :return: description
    :rtype: datetime

  .. method:: cancel_registration(profile)

    description

    :param Profile profile: description
    :return: description
    :rtype: bool

  .. method:: last_cancel_date()

    description

    :return: description
    :rtype: datetime

  .. method:: accept(profile)

    description

    :param Profile profile: description
    :return: description
    :rtype: bool

  .. method:: refuse(profile)

    description

    :param Profile profile: description
    :return: description
    :rtype: bool

  .. method:: done()

    description

    :return: description
    :rtype: bool

  .. method:: is_accepted()

    description

    :return: description
    :rtype: bool

  .. method:: days_left()

    description

    :return: description
    :rtype: int

  .. method:: check_registration()

    description

    :return: description
    :rtype: dict

  .. method:: is_now()

    description

    :return: description
    :rtype: bool
