from django.db import models

class Justice(models.Model):
   JUSTICE_IDS = {
       'A': 'Samuel Alito',
       'AS': 'Antonin Scalia',
       'B': 'Stephen Breyer',
       'D': 'Decree',
       'DS': 'David Souter',
       'EK': 'Elana Kagan',
       'G': 'Ruth Bader Ginsburg',
       'JS': 'John Paul Stephens',
       'K': 'Anthony Kennedy',
       'PC': 'Per Curiam',
       'R': 'John G. Roberts',
       'SS': 'Sonia Sotomayor',
       'T': 'Clarence Thomas',
       'UK': 'UNKNOWN',
   }

   id = models.CharField(max_length=5, primary_key=True)
   name = models.CharField(max_length=50) 
