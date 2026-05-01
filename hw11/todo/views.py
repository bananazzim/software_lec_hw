from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from .models import ToDoList, ToDoItem

class ListListView(ListView):
    model = ToDoList
    template_name = "todo/index.html"

class ItemListView(ListView):
    model = ToDoItem
    template_name = "todo/todo_list.html"

    def get_queryset(self):
        return ToDoItem.objects.filter(
            todo_list_id=self.kwargs["list_id"]
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["todo_list"] = ToDoList.objects.get(
            id=self.kwargs["list_id"]
        )
        return context

class ListCreate(CreateView):
    model = ToDoList
    fields = ["title"]
    template_name = "todo/todolist_form.html"
    success_url = reverse_lazy("index")

class ItemCreate(CreateView):
    model = ToDoItem
    fields = ["todo_list", "title", "description", "due_date"]
    template_name = "todo/todoitem_form.html"

    def get_initial(self):
        initial_data = super().get_initial()
        todo_list = ToDoList.objects.get(id=self.kwargs["list_id"])
        initial_data["todo_list"] = todo_list
        return initial_data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["todo_list"] = ToDoList.objects.get(
            id=self.kwargs["list_id"]
        )
        return context

    def get_success_url(self):
        return reverse("list", args=[self.kwargs["list_id"]])

class ListUpdate(UpdateView):
    model = ToDoList
    fields = ["title"]
    template_name = "todo/todolist_form.html"
    success_url = reverse_lazy("index")

class ItemUpdate(UpdateView):
    model = ToDoItem
    fields = ["todo_list", "title", "description", "due_date"]
    template_name = "todo/todoitem_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["todo_list"] = self.object.todo_list
        return context

    def get_success_url(self):
        return reverse_lazy("list", args=[self.object.todo_list.id])
    

class ListDelete(DeleteView):
    model = ToDoList
    success_url = reverse_lazy("index")

class ItemDelete(DeleteView):
    model = ToDoItem

    def get_success_url(self):
        # 개별 아이템이 삭제되면, 그 아이템이 속해 있던 할 일 목록 페이지로 돌아감
        return reverse_lazy("list", args=[self.kwargs["list_id"]])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 삭제 확인 템플릿(HTML)에서 어떤 목록에 속한 건지 보여주기 위해 context 추가
        context["todo_list"] = self.object.todo_list
        return context