CREATE TABLE Recipes (
    id SERIAL PRIMARY KEY,
    name TEXT
);

CREATE TABLE Ingredients (
    id SERIAL PRIMARY KEY,
    name TEXT
);

CREATE TABLE RecipeIngredients (
    id SERIAL PRIMARY KEY,
    recipe_id INTEGER REFERENCES Recipes(id),
    ingredient_id INTEGER REFERENCES Ingredients(id),
    quantity TEXT
);

CREATE TABLE Steps (
    id SERIAL PRIMARY KEY,
    recipe_id INTEGER REFERENCES Recipes(id),
    step INTEGER,
    instructions TEXT
);