from django import forms


class NameForm(forms.Form):
    mean_current_demand = forms.IntegerField(label='Ic (mean current demand)')
    design_life = forms.IntegerField(label='tf (design life)')
    utilization_factor = forms.IntegerField(label='u (utilization factor)')
    electrochemical_efficiency = forms.IntegerField(label='e (electrochemical efficiency)')

