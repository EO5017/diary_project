from django.db import models

# Create your models here.
class Diary(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    user_id= models.BigIntegerField()
    write_date = models.DateField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # user_idとwrite_dateをuniqueにする
    class Meta:
        models.UniqueConstraint(
            fields=['user_id', 'write_date'],
            name='unique_write_date'
        )

        db_table = 'diary'
    
    def __str__(self):
        return self.title