INSERT INTO breed (name) VALUES
('Британец'),
('Дворняга'),
('Мейкун')
ON CONFLICT DO NOTHING;

INSERT INTO cat (name, age, description, color, breed_id) VALUES
('Барсик', 12, 'Шабутной', 'Серый', 2),
('Василий', 12, 'Величественный', 'Коричневый', 3),
('Чарльз', 78, 'Гордый', 'Серый Королевский', 1)
ON CONFLICT DO NOTHING;