from django.shortcuts import render

def math_operations(request):
    result = None
    num1 = num2 = ''
    operation = None

    if request.method == 'POST':
        try:
            num1 = float(request.POST.get('num1', 0))
            num2 = float(request.POST.get('num2', 0))
            operation = request.POST.get('operation')

            if operation == 'add':
                result = num1 + num2
            elif operation == 'subtract':
                result = num1 - num2
            elif operation == 'multiply':
                result = num1 * num2
            elif operation == 'divide':
                result = num1 / num2 if num2 != 0 else 'Error (División por cero)'
        except ValueError:
            result = 'Error en los datos'

    return render(request, 'math_app/calculator.html', {
        'result': result,
        'num1': num1,
        'num2': num2,
        'operation': operation
    })