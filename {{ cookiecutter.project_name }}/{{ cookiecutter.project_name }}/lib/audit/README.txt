====================
django_audited_model
====================

Django middleware to remember the current user (from the session) during a request, and use it to wire up created_by and modified_by fields. Also a pair of abstract models so you don't have to type the field definitions out yourself.

Use
===

Add ``audited_model.middleware.AutoCreatedAndModifiedFields`` to your MIDDLEWARE_CLASSES. Then add suitable fields to any models that need them:

Managed on creation only
------------------------

    created_by = models.ForeignKey(User, related_name='created_%(class)s_set', null=False, blank=True)

You may also like to have a second field to record the creation time:

    created_at = models.DateTimeField(null=False, blank=False, auto_now_add=True)

Managed on any modification
---------------------------

    modified_by = models.ForeignKey(User, related_name='modified_%(class)s_set', null=False, blank=True)

Similarly, a second field to record the modification time may be helpful:

    modified_at = models.DateTimeField(null=False, blank=False, auto_now=True)

"Loose" auditing
================

If modified_by and/or created_by are nullable, by setting null=True, blank=True in the field definition, then if there is no authenticated session user they will be left unset. If they are *not* nullable, Django will raise an exception on save.

Convenience abstract models
===========================

To avoid typing the field definitions in, inherit from AuditedModel or LooselyAuditedModel as required. These contain all four fields above.

Admin
=====

You may prefer to exclude the above fields from the admin interface, for clarity. This is *not* set up automatically by the abstract models; however audited_model.models.exclude is a list of these fields.

Use in the shell and from management commands
=============================================

Middleware is not initialised or run from the ./manage.py shell or from management commands. If you need this behaviour in these cases, make sure you do the following:

----------------------------------------------------------------------------
from audited_model.middleware import set_current_user
----------------------------------------------------------------------------

This will set up the pre-save hook which manages the fields. If you are using strict (non-nullable) fields, you will also need to set the current user:

----------------------------------------------------------------------------
set_current_user(u)
----------------------------------------------------------------------------

For these purposes it is often useful to have a "system" user with a low pk, so you can do something like:

----------------------------------------------------------------------------
from django.contrib.auth.models import User
set_current_user(User.objects.get(pk=1))
----------------------------------------------------------------------------

Other notes
===========

The model shortcuts were originally written by Aaron Sokoloski, with some bugfixes by Andrew Godwin. The whole thing has been created and maintained at <http://devfort.com/>.

James Aylett <http://tartarus.org/james/computers/django/>
