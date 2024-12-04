from django import forms


class VoteForm(forms.Form):
    choice = forms.ChoiceField(choices=[], widget=forms.RadioSelect())

    def __init__(self, data, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['choice'].choices = [*map(lambda x: (x, x), data['choices'])]
