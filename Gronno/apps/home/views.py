from django.shortcuts import render

projects = [
    {
        'title':'Zoe: un chatbot orientado al bullying',
        'author':'Luis Mendez',
        'comments':497,
        'category': 'Inteligencia Artificial',
        'color':'IA',
        'goldmedals': '15.5m',
        'silvermedals': '2',
        'bronzemedals': '345',
    },
]

personal = [
    {
        'title':'Guantes automáticos',
        'link':"#",
        'category': 'Robotica',
        'color':'robotica',
    },
    {
        'title':'Zoe: un chatbot sobre bullying',
        'link':"#",
        'category': 'Inteligencia Artificial',
        'color':'IA',
    }
]

near = [
    {
        'image': 'persona1.jpg',
        'name': 'Aron Soto',
        'dedication': 'Programador de robotica',
        'link':'#',
    },
    {
        'image': 'descarga.jpg',
        'name': 'Lautaro Rodriguez',
        'dedication': 'Entrenador de IA',
        'link':'#',
    }
]

def homepage(request):
    context = {
        'projects':projects,
        'personal_projects':personal,
        'near':near
    }

    return render(request, 'home/home.html', context)