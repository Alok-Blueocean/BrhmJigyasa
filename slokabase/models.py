from django.db import models

class Theme(models.Model):
    """Model representing a Theme of Question."""
    name = models.CharField(max_length=100, null=False, unique=True)
    parent = models.ForeignKey('Theme', related_name='ParentTheme', on_delete=models.SET_NULL, null=True,blank=True)

    def __str__(self):
        """String for representing the Model object."""
        return self.name or 'Blank theme'

class Shloka(models.Model):
    """Model representing a verse from any of the books e.g. BG, SB, CC."""
    text = models.TextField()
    source = models.CharField(max_length=20, null=False,default="BG")
    non_chapter  = models.CharField(max_length=10, blank=True, null=True)
    canto = models.IntegerField(null=True,blank=True)
    chapter = models.IntegerField(null=True,blank=True)
    number = models.CharField(max_length=10, null=True,blank=True)
    w2w = models.TextField(null=True,blank=True)
    translation = models.TextField(null=True,blank=True)
    purport = models.TextField(null=True,blank=True)
    referance_text = models.CharField(max_length=20,blank=True, null=True,unique=True)

    def validate_referance(self):
        validatation_flag = False
        if self.source in ['BG','SB']:
            if(self.non_chapter=='' or self.non_chapter== None):
                if self.source=='BG' and self.chapter in range(19):
                    validatation_flag = True
                elif(self.source =='SB' and self.canto in range(13) and self.chapter in range(100)):
                    validatation_flag = True
            else:
                validatation_flag = True

        if(self.source=='CC' and self.non_chapter.lower() in ['adi_lila','madhya_lila','antya_lila'] \
                and self.chapter in range(30)):
                    validatation_flag = True
        return validatation_flag
    
    def bg_check(self):
        if(self.non_chapter=='' or self.non_chapter== None):
            self.referance_text = self.source+" "+str(self.chapter)+"."+str(self.number)
        else:
            self.referance_text = self.source+' '+self.non_chapter
    def sb_check(self):
        if(self.non_chapter=='' or self.non_chapter== None):
            self.referance_text = self.source+" "+str(self.canto)+"."+str(self.chapter)+"."+str(self.number)
        else:
            self.referance_text = self.source+' '+self.non_chapter

    def cc_check(self):
        if(self.chapter and self.number):
            self.referance_text = self.source+" "+self.non_chapter+" "+str(self.chapter)+"."+str(self.number)
        else:
            self.referance_text = self.source+" "+self.non_chapter  

    def save(self, *args, **kwargs):
        if not self.validate_referance():
            return # Yoko shall never have her own blog!
        else:
            if self.source == 'BG':
                self.bg_check()
            elif self.source == 'SB':
                self.sb_check()
            elif self.source == 'CC':
                self.cc_check()
            
            super(Shloka, self).save(*args, **kwargs)
    def __str__(self):
        return self.referance_text

    def get_absolute_url(self):
        return reverse("_detail", kwargs={"pk": self.pk})
    # def __str__(self):
    #     """String for representing the Model object."""
    #     return '{} {}{}.{}'.format(self.source, self.canto or '', self.chapter, self.number)

    # def save(self, *args, **kwargs):
    #     print("save")
    #     super(Shloka, self).save(*args, **kwargs)
    class Meta:
        unique_together = (('source', 'canto', 'chapter', 'number'),)


class Question(models.Model):
    
    question_id  = models.AutoField(primary_key=True)
    question_text = models.TextField()
    answer_text = models.TextField(blank=True, null=True)#models.OneToOneField(Answer, verbose_name='Answer', null=True,on_delete=models.SET_NULL)
    tag = models.ManyToManyField(Theme,blank=True, null=True)
    shloka = models.ForeignKey(Shloka, 
                                null=True,blank=True, on_delete=models.SET_NULL)
    
    def __str__(self):
        return str(self.question_text)

    def get_absolute_url(self):
        return reverse("_detail", kwargs={"pk": self.pk})


