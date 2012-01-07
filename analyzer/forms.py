from django import forms

from analyzer.models import Statement

class StatementForm(forms.ModelForm):
    statement_file = forms.FileField()
    
    class Meta:
        model = Statement
        exclude = ('create_dt', 'modify_dt', 'created_by')
