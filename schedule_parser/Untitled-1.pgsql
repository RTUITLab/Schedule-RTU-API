SELECT discipline.name, "group".name 
FROM lesson
JOIn discipline ON  lesson.discipline_id = discipline.id 
JOIn "group" ON  lesson.group_id = "group".id
WHERe room_id = 6520