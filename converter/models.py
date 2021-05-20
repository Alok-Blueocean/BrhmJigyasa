from django.db import models


# Create your models here.
class Book(models.Model):
    """Model representing a Book e.g. BG, SB, CC."""
    name = models.CharField(max_length=200, help_text='Enter a name of book (e.g. Bhagavad Gita)')
    author = models.CharField(max_length=200, help_text='Enter a name of book (e.g. AC Bhaktivedanta)')

    def __str__(self):
        """String for representing the Model object."""
        return self.name


class Shloka(models.Model):
    """Model representing a verse from any of the books e.g. BG, SB, CC."""
    text = models.CharField(max_length=500, null=False)
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    canto = models.IntegerField(null=True)
    chapter = models.IntegerField(null=False)
    number = models.CharField(max_length=10, null=False)
    w2w = models.CharField(max_length=200, null=False)
    translation = models.CharField(max_length=200, null=False)
    purport = models.ManyToManyField('PurportPara', related_name='PurportPara')

    def __str__(self):
        """String for representing the Model object."""
        return '{} {}{}.{}'.format(self.book, self.canto or '', self.chapter, self.number)

    class Meta:
        unique_together = (('book', 'canto', 'chapter', 'number'),)


class PurportPara(models.Model):
    """Model representing a paragraph of Purport."""
    number = models.IntegerField(null=True)
    shloka = models.ForeignKey('Shloka', on_delete=models.SET_NULL, null=True)
    text = models.CharField(max_length=5000, null=False)

    def __str__(self):
        """String for representing the Model object."""
        return '{} PP#{}'.format(self.shloka, self.number)

    class Meta:
        unique_together = (('shloka', 'number'),)


class Question(models.Model):
    """Model representing a Question belonging to paragraph of purport."""
    number = models.IntegerField(default=1, null=False)  # single PurportPara can have multiple questions
    text = models.CharField(max_length=500, null=False)
    para = models.ForeignKey('PurportPara', on_delete=models.SET_NULL, null=True)
    theme = models.ManyToManyField('Theme', related_name='Theme')

    def __str__(self):
        """String for representing the Model object."""
        return '{} Q#{}'.format(self.para, self.number)

    class Meta:
        unique_together = (('para', 'number'),)


class Theme(models.Model):
    """Model representing a Theme of Question."""
    name = models.CharField(max_length=100, null=False, unique=True)
    parent = models.ForeignKey('Theme', related_name='ParentTheme', on_delete=models.SET_NULL, null=True)
    child = models.ManyToManyField('Theme', related_name='ChildTheme')
    question = models.ManyToManyField('Question', related_name='Question')

    def __str__(self):
        """String for representing the Model object."""
        return self.name or 'Blank theme'
