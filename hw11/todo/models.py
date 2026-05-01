from django.db import models

class ToDoList(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class ToDoItem(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(null=True, blank=True)
    todo_list = models.ForeignKey(
        ToDoList,
        on_delete=models.CASCADE,
        related_name="item_set"
    )

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["due_date"]