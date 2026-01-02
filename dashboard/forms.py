from django import forms
from .models import Student
from .models import Progress
class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = '__all__'
class ProgressForm(forms.ModelForm):
    class Meta:
        model = Progress
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        subjects = ['mathematics', 'science', 'english']
        for subject in subjects:
            mark = cleaned_data.get(subject)
            if mark is None:
                self.add_error(subject, "This field cannot be empty.")
            elif not (0 <= mark <= 100):
                self.add_error(subject, "Marks must be between 0 and 100.")
        return cleaned_data
class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = '__all__'

# ProgressForm with validation
class ProgressForm(forms.ModelForm):
    class Meta:
        model = Progress
        fields = ['exam_type', 'mathematics', 'science', 'english', 'student']
        widgets = {
            'student': forms.HiddenInput()
        }

    def clean_mathematics(self):
        marks = self.cleaned_data['mathematics']
        if marks < 0 or marks > 100:
            raise forms.ValidationError("Marks must be between 0 and 100")
        return marks

    def clean_science(self):
        marks = self.cleaned_data['science']
        if marks < 0 or marks > 100:
            raise forms.ValidationError("Marks must be between 0 and 100")
        return marks

    def clean_english(self):
        marks = self.cleaned_data['english']
        if marks < 0 or marks > 100:
            raise forms.ValidationError("Marks must be between 0 and 100")
        return marks