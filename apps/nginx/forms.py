from django import forms


class NginxApplyForm(forms.Form):
    YESNO = (
            ( True, 'Yes' ),
            ( False, 'No' ),
            )
    transfer = forms.ChoiceField(widget = forms.RadioSelect(), choices = YESNO, initial = True, label = 'Transfer configuration files')
    network_conf = forms.ChoiceField(widget = forms.RadioSelect(), choices = YESNO, initial = True, label = 'Configure network')
    network_live = forms.ChoiceField(widget = forms.RadioSelect(), choices = YESNO, initial = True, label = 'UP&Run IPs')
    restart_nginx = forms.ChoiceField(widget = forms.RadioSelect(), choices = YESNO, initial = True, label = 'Restart HTTP Frontend service')
