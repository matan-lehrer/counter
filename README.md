Things to fix / work on or general notes:

1. Currently, if I open 2 proccesors - 2 tabs, they both modify the db.
   I need to think of how to overcome this.
   1 option is to add a table per process, or add a column for every user.

2. Unit / System / Integration tests.

3. CI / CD.

4. Consider changing column 'function used' to enum.

5. Consider modifying in general the columns to be more relevant.

6. Add consts.py and requirements.txt to backend.

7. Conventions - names of files, typing - use mypy, isort and black for linting.

8. Design question - why not perform all logic in the frontend and only "update" 
   the backend? will increase speed and if we anyways have a "tab per user" layout,
   there are no concurrency issues involved.

9. What is the expected behaviour? When I open a new tab - should it start from zero? or from the last number thats been logged?