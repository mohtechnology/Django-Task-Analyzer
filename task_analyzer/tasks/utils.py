from datetime import date

def calculate_system_score(task):
    importance_weight = 0.30
    importance_score = task.importance / 10 

    urgency_weight = 0.30
    if task.due_date:
        days_left = (task.due_date - date.today()).days

        if days_left < 0:
            urgency_score = 1
        else:
            urgency_score = max(0, 1 - days_left / 30)
    else:
        urgency_score = 0.2

    effort_weight = 0.10
    effort_score = 1 - min(task.estimated_hours, 20) / 20

    depends_weight = 0.10
    depends_count = task.dependencies.count()
    depends_score = min(depends_count / 5, 1)

    influence_weight = 0.20
    influence_count = task.blocked_by.count()
    influence_score = min(influence_count / 5, 1)

    final_raw = (
        importance_weight * importance_score +
        urgency_weight * urgency_score +
        effort_weight * effort_score +
        depends_weight * depends_score +
        influence_weight * influence_score
    )

    return round(final_raw * 10, 2)
