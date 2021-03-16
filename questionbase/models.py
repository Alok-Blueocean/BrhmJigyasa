from django.db import models

# Create your models here.

class Answer(models.Model):
    
    answer_id = models.AutoField(primary_key=True)
    text = models.TextField()

    def __str__(self):
        return str(self.text)

    def __repr__(self):
        return str(self.text)

    def get_absolute_url(self):
        return reverse("_detail", kwargs={"pk": self.pk})

class Tag(models.Model):
    
    tag_id = models.AutoField(primary_key=True)
    text = models.CharField(blank=False, null=False,
        unique=True, max_length=50)

    def __str__(self):
        return self.text

    def get_absolute_url(self):
        return reverse("_detail", kwargs={"pk": self.pk})

class SubTag(models.Model):
    
    subtag_id = models.AutoField(primary_key=True)
    text = models.CharField(blank=False, null=False, unique=True,max_length=50)
    category  = models.ForeignKey(Tag,null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.text

    def get_absolute_url(self):
        return reverse("_detail", kwargs={"pk": self.pk})

class Referance(models.Model):
    referance_id = models.AutoField(primary_key=True)
    source  = models.CharField(max_length=30, blank=True, null=True)
    non_chapter  = models.CharField(max_length=10, blank=True, null=True)
    canto = models.IntegerField(blank=True, null=True)
    chapter = models.IntegerField(blank=True, null=True)
    sloka = models.IntegerField(blank=True, null=True)
    referance_text = models.CharField(max_length=20,blank=True, null=True,unique=True)

    def validate_referance(self):
        validatation_flag = False
        if self.source in ['BG','SB']:
            if(self.non_chapter=='' or self.non_chapter== None):
                if self.source=='BG' and self.chapter in range(19) and self.sloka in range(80):
                    validatation_flag = True
                elif(self.source =='SB' and self.canto in range(13) and self.chapter in range(100) and self.sloka in range(100)):
                    validatation_flag = True
            else:
                validatation_flag = True

        if(self.source=='CC' and self.non_chapter.lower() in ['adi_lila','madhya_lila','antya_lila'] \
                and self.chapter in range(30) and self.sloka in range(300)):
                    validatation_flag = True
        return validatation_flag
    
    def bg_check(self):
        if(self.non_chapter=='' or self.non_chapter== None):
            self.referance_text = self.source+" "+str(self.chapter)+"."+str(self.sloka)
        else:
            self.referance_text = self.source+' '+self.non_chapter
    def sb_check(self):
        if(self.non_chapter=='' or self.non_chapter== None):
            self.referance_text = self.source+" "+str(self.canto)+"."+str(self.chapter)+"."+str(self.sloka)
        else:
            self.referance_text = self.source+' '+self.non_chapter

    def cc_check(self):
        if(self.chapter and self.sloka):
            self.referance_text = self.source+" "+self.non_chapter+" "+str(self.chapter)+"."+str(self.sloka)
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
            
            super(Referance, self).save(*args, **kwargs)
    def __str__(self):
        return self.referance_text

    def get_absolute_url(self):
        return reverse("_detail", kwargs={"pk": self.pk})

class Question(models.Model):
    
    question_id  = models.AutoField(primary_key=True)
    question_text = models.TextField()
    answer_text = models.TextField(blank=True, null=True)#models.OneToOneField(Answer, verbose_name='Answer', null=True,on_delete=models.SET_NULL)
    subtag = models.ManyToManyField(SubTag)
    referance = models.ForeignKey(Referance, 
                                null=True, on_delete=models.SET_NULL)
    
    def __str__(self):
        return str(self.question_text)

    def get_absolute_url(self):
        return reverse("_detail", kwargs={"pk": self.pk})
