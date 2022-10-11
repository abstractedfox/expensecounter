#ExpenseCounter

This is a lightweight app for counting personal expenses, with a simple hand-coded frontend and an sqlite database. More polishes and little features will be added later, but at this stage all the most important parts seem to work!

Japanese language support was just added as well. いつでも、自然じゃないの言葉があれば教えて下さい。

'expensecounter' is the root app, with the actual app being 'ExpenseCounterApp'. It will be necessary to run this command to initialize the database tables:
	py manage.py migrate --run-syncdb