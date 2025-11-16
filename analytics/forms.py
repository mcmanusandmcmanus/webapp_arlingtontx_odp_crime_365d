from django import forms

WINDOW_CHOICES = [
    ("7d", "Last 7 days"),
    ("14d", "Last 14 days"),
    ("28d", "Last 28 days"),
    ("91d", "Last 91 days"),
    ("182d", "Last 182 days"),
    ("365d", "Last 365 days"),
]

SEGMENT_CHOICES = [
    ("beat", "Beat"),
    ("district", "District"),
    ("offense_category", "Offense Type"),
    ("day_of_week", "Day of Week"),
    ("time_of_day_label", "Time of Day"),
]


class PasscodeForm(forms.Form):
    passcode = forms.CharField(
        max_length=128,
        widget=forms.PasswordInput(attrs={"class": "form-input"}),
        label="Access passcode",
    )


class SegmentFilterForm(forms.Form):
    window = forms.ChoiceField(
        choices=WINDOW_CHOICES,
        initial="28d",
        widget=forms.Select(attrs={"class": "form-input"}),
    )
    segment_field = forms.ChoiceField(
        choices=SEGMENT_CHOICES,
        initial="beat",
        widget=forms.Select(attrs={"class": "form-input"}),
    )


class ImportUploadForm(forms.Form):
    passcode = forms.CharField(
        max_length=128,
        widget=forms.PasswordInput(attrs={"class": "form-input"}),
        label="Importer passcode",
    )
    data_date = forms.DateField(
        help_text="Date that best represents this batch (usually most recent incident date).",
        widget=forms.DateInput(attrs={"type": "date", "class": "form-input"}),
    )
    data_file = forms.FileField(
        required=False,
        help_text="Upload CSV or Excel file exported from the upstream portal.",
        widget=forms.FileInput(attrs={"class": "form-input"}),
    )
    notes = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 3, "class": "form-input"}),
        required=False,
    )
    pasted_rows = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 6, "class": "form-input"}),
        required=False,
        help_text="Optional: paste tabular rows from upstream application.",
    )

    def clean(self):
        cleaned = super().clean()
        if not cleaned.get("data_file") and not cleaned.get("pasted_rows"):
            raise forms.ValidationError("Provide either a file upload or pasted rows.")
        return cleaned
