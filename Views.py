# onlinecourse/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Course, Enrollment, Choice, Submission

def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    if request.method == 'POST':
        # Retrieve the enrollment for the current user
        enrollment = Enrollment.objects.get(user=request.user, course=course)
        
        # Create a new submission
        submission = Submission.objects.create(enrollment=enrollment)
        
        # Check selected choices from the form
        for key, value in request.POST.items():
            if key.startswith('choice_'):
                choice_id = int(value)
                choice = Choice.objects.get(pk=choice_id)
                submission.choices.add(choice)
        
        submission.save()
        return redirect('onlinecourse:show_exam_result', course_id=course.id, submission_id=submission.id)
    
    return render(request, 'onlinecourse/course_detail_bootstrap.html', {'course': course})

def show_exam_result(request, course_id, submission_id):
    course = get_object_or_404(Course, pk=course_id)
    submission = get_object_or_404(Submission, pk=submission_id)
    
    # Calculate score
    total_questions = 0
    correct_answers = 0
    
    for lesson in course.lesson_set.all():
        for question in lesson.question_set.all():
            total_questions += 1
            # Get correct choices for this question
            correct_choices = set(question.choice_set.filter(is_correct=True).values_list('id', flat=True))
            # Get choices submitted by the user for this question
            user_choices = set(submission.choices.filter(question=question).values_list('id', flat=True))
            
            if correct_choices == user_choices:
                correct_answers += 1
                
    score = (correct_answers / total_questions) * 100 if total_questions > 0 else 0
    passed = score >= 80  # Assuming 80% is the passing grade
    
    context = {
        'course': course,
        'score': score,
        'passed': passed,
    }
    return render(request, 'onlinecourse/exam_result_bootstrap.html', context)
