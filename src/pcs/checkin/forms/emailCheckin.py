# Checkin form to register their attendance at a contest

from django import forms
from django.core.exceptions import ObjectDoesNotExist
from registration.models import Account
from registration.utility import auth


class emailCheckinForm(forms.Form):
    Email = forms.EmailField(widget=forms.EmailInput(
        attrs={'placeholder': 'Email'}),
        label='Please enter your email address'
    )

    def validUser(self, req):
        errors = {}
        # userExists will check that user is in db
        # if user is in DB they will be marked as checked-in
        # if they don't match or are not in the db an error will
        # display and the user will have to try again.
        try:
            user = Account.objects.get(Email=req['Email'])
            user.isCheckedIn = True
            user.save()
            return True
        except ObjectDoesNotExist:
            errors['Email'] = 'Check-in failed'
            self.add_error(None, errors)
            return False

        if auth.userExists(req):
            # mark user at checked in
            user = auth.getUser(req)
            user.isSignedIn = True
            user.save()
            return True

        else:
            errors['Email'] = 'Check-in failed'
            return False
