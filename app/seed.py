
from sqlalchemy.orm import Session
from . import models

def insert_initial_recipes(db: Session):
    initial = [
        {
            "title": "Cookies de avena y banana",
            "category": "cookies",
            "ingredients": [
                "2 bananas maduras",
                "1 taza de avena",
                "1 cdita de canela",
                "Chips de chocolate amargo opcional"
            ],
            "steps": "Pisar bananas, mezclar con avena y canela. Agregar chips si querés. Formar cookies y hornear 12-15 min a 180°C.",
        },
        {
            "title": "Brownies fit de cacao",
            "category": "brownies",
            "ingredients": [
                "2 huevos",
                "1/2 taza de cacao amargo",
                "1/3 taza de harina de almendras",
                "2 cdas de miel o edulcorante a gusto",
                "1/4 taza de aceite de coco derretido"
            ],
            "steps": "Batir huevos con miel, sumar cacao, harina y aceite. Hornear 20-22 min a 180°C.",
        },
        {
            "title": "Muffins integrales de arándanos",
            "category": "muffins",
            "ingredients": [
                "1 taza harina integral",
                "1/2 taza yogur natural",
                "1 huevo",
                "1/4 taza aceite",
                "1/2 taza arándanos",
                "1 cdita polvo de hornear"
            ],
            "steps": "Mezclar secos, sumar yogur, huevo y aceite. Integrar arándanos. Hornear 18 min a 180°C.",
        },
    ]
    for r in initial:
        db.add(models.Recipe(
            title=r["title"],
            category=r["category"],
            ingredients=r["ingredients"],
            steps=r["steps"],
            is_healthy=True
        ))
    db.commit()
