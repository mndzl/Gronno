from django.shortcuts import render

# Create your views here.

networks = [
    {
        'name':'facebook2',
        'link':'facebook.com',
    },
    {
        'name':'instagram',
        'link':'instagram.com',
    },
    {
        'name':'linkedin',
        'link':'linkedin.com',
    }
]
person = {
    'name':'Luis',
    'extract':"""Mi nombre es Luis, soy un capo y no se la verdad que poner aqui porque estoy
                probando si se ve bien eso del interlineado a ver que tal pero yo creo que se ve bien
                no se tengo que seguir probando y no se cuanto tiempo tengo que seguir escribiendoo
                agunte boquita noma maru asinomae""",
    'networks':networks,
    'email':'mendezgla.56@gmail.com',
    'category':'IA',
}
projects = [
    {
        'title':'Zoe: un chatbot orientado al bullying',
        'comments':497,
        'category': 'IA',
        'description':"""Mi nombre es Luis, soy un capo y no se la verdad que poner aqui porque estoy
                probando si se ve bien eso del interlineado a ver que tal pero yo creo que se ve bien
                no se tengo que seguir probando y no se cuanto tiempo tengo que seguir escribiendoo
                agunte boquita noma maru asinomae""",
        'goldmedals': '15.5m',
        'silvermedals': '2',
        'bronzemedals': '345',
    },
    {
        'title':'Guante Automatico',
        'description':"""Mi nombre es Luis, soy un capo y no se la verdad que poner aqui porque estoy
                probando si se ve bien eso del interlineado a ver que tal pero yo creo que se ve bien
                no se tengo que seguir probando y no se cuanto tiempo tengo que seguir escribiendoo
                agunte boquita noma maru asinomae""",
        'comments':497,
        'category': 'robotica',
        'goldmedals': '15.5m',
        'silvermedals': '2',
        'bronzemedals': '345',
    },
    {
        'title':'Casa Inteligente',
        'description':"""Mi nombre es Luis, soy un capo y no se la verdad que poner aqui porque estoy
                probando si se ve bien eso del interlineado a ver que tal pero yo creo que se ve bien
                no se tengo que seguir probando y no se cuanto tiempo tengo que seguir escribiendoo
                agunte boquita noma maru asinomae""",
        'comments':497,
        'category': 'robotica',
        'goldmedals': '15.5m',
        'silvermedals': '2',
        'bronzemedals': '345',
    },
]


def profile(request):
    context = {
        'user':person,
        'projects':projects,
    }

    return render(request, 'users/users.html', context)