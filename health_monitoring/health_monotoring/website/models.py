from django.db import models

# Create your models here.
class BodyBuilder(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length = 50)
    height = models.IntegerField()
    weight = models.FloatField()

    def __str__(self):
        return(f'{self.height} {self.weight}')

class PhysicalIndicators(models.Model):
    id = models.AutoField(primary_key=True)
    bodybuilder = models.ForeignKey(BodyBuilder, on_delete=models.CASCADE)
    pulse = models.IntegerField()
    steps = models.IntegerField()
    distance = models.IntegerField()
    
    def __str__(self):
        return(f'{self.pulse} {self.steps} {self.distance}')

class FitnessBracelet(models.Model):
    id = models.AutoField(primary_key=True)
    physical_indicators = models.ForeignKey(PhysicalIndicators, on_delete=models.CASCADE)
    date = models.DateField()
    
    

