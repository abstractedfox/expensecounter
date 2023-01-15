#ExpenseCounter

This is a lightweight app for counting personal expenses, with a simple hand-coded frontend and an sqlite database. More polishes and little features will be added later, but at this stage all the most important parts seem to work!

Japanese language support is now live. いつでも、自然じゃないの言葉があれば教えて下さい。

'expensecounter' is the root app, with the actual app being 'ExpenseCounterApp'. The proper way to run it for the first time is to initialize the database, with the following commands from the root folder (where 'manage.py' is located):
>py manage.py makemigrations
>py manage.py migrate --run-syncdb
...however now there is an exception handler in the index function (/ExpenseCounterApp/views.py) that does this automatically if an exception is thrown while loading the index. So it should now handle it for you, but if there are problems with it, try doing it manually just in case (and then let me know what issue you had!)

Once it's running, simply navigate to localhost:8000. Have fun!