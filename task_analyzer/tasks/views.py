from django.shortcuts import render, redirect
from datetime import date, datetime
from .models import Task
from .utils import calculate_system_score


def home(request):
    selection = request.GET.get("selection", "system")

    tasks = Task.objects.all()

    # -------- SORTING OPTIONS --------
    if selection == "deadline":
        tasks = tasks.order_by("due_date")

    elif selection == "fastest":
        tasks = tasks.order_by("estimated_hours")

    elif selection == "important":
        tasks = tasks.order_by("-importance")

    elif selection == "balance":
        def balance_score(t):
            urgency = 0
            if t.due_date:
                days_left = (t.due_date - date.today()).days
                urgency = max(0, 10 - days_left)
            return (t.importance / max(t.estimated_hours, 1)) - urgency

        tasks = sorted(tasks, key=balance_score, reverse=True)

    else:
        tasks = tasks.order_by("-score")

    return render(request, "home.html", {
        "tasks": tasks,
        "selection": selection
    })


def add_tasks(request):
    if request.method == "POST":

        title = request.POST.get("title")

        due_date_str = request.POST.get("date")
        due_date = None
        if due_date_str:
            due_date = datetime.strptime(due_date_str, "%Y-%m-%d").date()

        hours_raw = request.POST.get("hours")
        estimated_hours = float(hours_raw) if hours_raw else 1

        imp_raw = request.POST.get("importance")
        importance = int(imp_raw) if imp_raw else 1

        dependencies = request.POST.getlist("dependencies")

        new_task = Task.objects.create(
            title=title,
            due_date=due_date,
            estimated_hours=estimated_hours,
            importance=importance,
            score=0
        )

        if dependencies:
            new_task.dependencies.set(dependencies)

        for t in Task.objects.all():
            t.refresh_from_db()
            t.score = calculate_system_score(t)
            t.save()
        return redirect("home")

    tasks = Task.objects.all()
    return render(request, "add_tasks.html", {"tasks": tasks})



def delete_task(request, task_id):
    task = Task.objects.get(id=task_id)
    task.delete()
    return redirect("home")

def edit_task(request, task_id):
    task = Task.objects.get(id=task_id)

    if request.method == "POST":
        task.title = request.POST.get("title")
        task.estimated_hours = float(request.POST.get("hours"))
        task.importance = int(request.POST.get("importance"))

        date_str = request.POST.get("date")
        task.due_date = datetime.strptime(date_str, "%Y-%m-%d").date() if date_str else None

        deps = request.POST.getlist("dependencies")
        task.dependencies.set(deps)

        # recalc score
        for t in Task.objects.all():
            t.refresh_from_db()
            t.score = calculate_system_score(t)
            t.save()

        return redirect("home")

    tasks = Task.objects.all()

    return render(request, "edit_task.html", {
        "task": task,
        "tasks": tasks
    })
