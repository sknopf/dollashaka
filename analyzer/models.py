from django.contrib.auth.models import User
from django.db import models

BOFA, USAA, CITI = 0, 1, 2
institution_choices = (
    (BOFA, "BOFA"),
    (USAA, "USAA"),
    (CITI, "CITI"),
    )

def bofa_clean(line):
    try:
        if not line[1]:
            return (None, None, None)
        else:
            try:                
                line[2] = float(line[2])
            except ValueError:
                return (None, None, None)
            purchase_date, title, amount = line[0], line[1], line[2]
            purchase_date = purchase_date.replace("/", "-")
            purchase_date = purchase_date[-4:] + "-" + purchase_date[:5]
            return (purchase_date, title, amount)
    except IndexError:
        return (None, None, None)

def usaa_clean(line):
    pass

def citi_clean(line):
    pass

institution_clean = {
    BOFA: bofa_clean,
    USAA: usaa_clean,
    CITI: citi_clean,
    }

class StatementManager(models.Manager):
    def statements_for_user(self, user):
        """
        This method returns all of the statements
        for the given user. Later it could return statements that
        have been shared
        """
        return self.filter(created_by=user)


class Statement(models.Model):
    institution = models.IntegerField(choices=institution_choices, default=BOFA)
    comments = models.TextField(null=True, blank=True)

    create_dt = models.DateTimeField(auto_now_add=True)
    modify_dt = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, related_name="statements", null=True, blank=True)

    objects = StatementManager()        


class PurchaseManager(models.Manager):
    def from_file(self, statement_file, statement):    
        for chunk in statement_file.read().split("\n"):
            line = chunk.rstrip().replace('"', '').split(",")
            purchase_date, title, amount  = institution_clean[statement.institution](line)
            if purchase_date:
                self.create(title=title, amount=amount, purchase_date=purchase_date, statement=statement)


class Purchase(models.Model):
    title = models.CharField(max_length=255)
    amount = models.DecimalField(decimal_places=2, max_digits=15)
    purchase_date = models.DateField()
    statement = models.ForeignKey('Statement')
    category = models.ForeignKey('PurchaseCategory', null=True, blank=True)

    objects = PurchaseManager()
        
class PurchaseCategory(models.Model):
    name = models.CharField(max_length=255)
