# Repositorio código Indicadores Educativos
* La rama con los cambios más recientes es DESARROLLO *
Main solamente es utilizada para cambios aprobados.
Se debe copiar el repositorio y levantar el contenedor mediante:
"""
docker compose build
dokcer compose up -d
docker compose exec app bash
"""
Para crear la base de datos
"""
cd Sis_Ind_Edu
python manage.py makemigrations
python manage.py migrate
"""
para ejecutar el servidor:
"""
python manage.py runserver 0:8000
"""

y de esta manera el proyecto estará montado y funcionando en cualquiera de las dos ramas.
Dudas y comentarios: 36172712@uaz.edu.mx
